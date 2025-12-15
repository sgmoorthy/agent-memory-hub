"""
AlloyDB (PostgreSQL) session store implementation.
"""
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from agent_memory_hub.config.alloydb_config import AlloyDBConfig
from agent_memory_hub.data_plane.adk_session_store import SessionStore
from agent_memory_hub.utils.telemetry import get_tracer
from agent_memory_hub.utils.ttl_manager import get_current_timestamp

Base = declarative_base()


class MemorySession(Base):
    """SQLAlchemy model for memory sessions."""

    __tablename__ = "memory_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False, index=True)
    key = Column(String(255), nullable=False, index=True)
    value = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_current_timestamp)
    expires_at = Column(DateTime, nullable=True, index=True)
    region = Column(String(50), nullable=False)

    __table_args__ = (
        {"schema": "public"},
    )


class AlloyDBSessionStore(SessionStore):
    """
    AlloyDB (PostgreSQL) session store implementation.
    Uses SQLAlchemy for database operations with connection pooling.
    """

    def __init__(
        self,
        config: AlloyDBConfig,
        ttl_seconds: Optional[int] = None,
    ):
        """
        Initialize AlloyDB session store.

        Args:
            config: AlloyDB connection configuration
            ttl_seconds: Default TTL for entries (None = no expiry)
        """
        self.config = config
        self.ttl_seconds = ttl_seconds
        self._tracer = get_tracer()

        # Create engine with connection pooling
        self.engine = create_engine(
            config.get_connection_string(),
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_pre_ping=True,  # Verify connections before using
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)

    def write(self, session_id: str, key: str, value: Any) -> None:
        """
        Write a value to AlloyDB.

        Args:
            session_id: Session identifier
            key: Memory key
            value: Value to store
        """
        with self._tracer.start_as_current_span("AlloyDBSessionStore.write") as span:
            span.set_attribute("session.id", session_id)
            span.set_attribute("memory.key", key)
            span.set_attribute("database", self.config.database)

            db: Session = self.SessionLocal()
            try:
                # Calculate expiry if TTL is set
                expires_at = None
                if self.ttl_seconds is not None:
                    from agent_memory_hub.utils.ttl_manager import (
                        get_expiry_timestamp,
                    )

                    expires_at = get_expiry_timestamp(self.ttl_seconds)

                # Check if entry exists
                stmt = select(MemorySession).where(
                    MemorySession.session_id == session_id,
                    MemorySession.key == key,
                )
                existing = db.execute(stmt).scalar_one_or_none()

                if existing:
                    # Update existing entry
                    existing.value = value
                    existing.created_at = get_current_timestamp()
                    existing.expires_at = expires_at
                else:
                    # Insert new entry
                    entry = MemorySession(
                        session_id=session_id,
                        key=key,
                        value=value,
                        created_at=get_current_timestamp(),
                        expires_at=expires_at,
                        region=self.config.region,
                    )
                    db.add(entry)

                db.commit()
            finally:
                db.close()

    def read(self, session_id: str, key: str) -> Optional[Any]:
        """
        Read a value from AlloyDB.

        Args:
            session_id: Session identifier
            key: Memory key

        Returns:
            Stored value or None if not found/expired
        """
        with self._tracer.start_as_current_span("AlloyDBSessionStore.read") as span:
            span.set_attribute("session.id", session_id)
            span.set_attribute("memory.key", key)
            span.set_attribute("database", self.config.database)

            db: Session = self.SessionLocal()
            try:
                stmt = select(MemorySession).where(
                    MemorySession.session_id == session_id,
                    MemorySession.key == key,
                )
                entry = db.execute(stmt).scalar_one_or_none()

                if not entry:
                    return None

                # Check if expired
                if entry.expires_at and datetime.now() > entry.expires_at:
                    # Delete expired entry
                    db.delete(entry)
                    db.commit()
                    return None

                return entry.value
            finally:
                db.close()

    def cleanup_expired(self, session_id: Optional[str] = None) -> int:
        """
        Manually cleanup expired entries.

        Args:
            session_id: Optional session ID to limit cleanup scope

        Returns:
            Number of entries deleted
        """
        db: Session = self.SessionLocal()
        try:
            stmt = select(MemorySession).where(
                MemorySession.expires_at.isnot(None),
                MemorySession.expires_at < datetime.now(),
            )

            if session_id:
                stmt = stmt.where(MemorySession.session_id == session_id)

            expired_entries = db.execute(stmt).scalars().all()
            count = len(expired_entries)

            for entry in expired_entries:
                db.delete(entry)

            db.commit()
            return count
        finally:
            db.close()
