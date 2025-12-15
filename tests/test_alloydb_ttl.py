import pytest
# Ensure ADK import check is bypassed for testing
from typing import Dict, Any
from typing import Dict, Any, Optional

from agent_memory_hub.data_plane.alloydb_session_store import AlloyDBSessionStore, ADK_AVAILABLE
from agent_memory_hub.config.alloydb_config import AlloyDBConfig

# Force ADK_AVAILABLE to True for test environment
global ADK_AVAILABLE
ADK_AVAILABLE = True

# Simple in‑memory mock for the ADK DatabaseSessionService
class MockSession:
    def __init__(self, session_id: str):
        self.id = session_id
        self.state: Dict[str, Any] = {}

class MockSessionService:
    def __init__(self):
        self.sessions: Dict[str, MockSession] = {}

    def get_session(self, session_id: str) -> MockSession:
        return self.sessions[session_id]

    def create_session(self, session: MockSession) -> None:
        self.sessions[session.id] = session

    def update_session(self, session: MockSession) -> None:
        # In a real service this would persist; here we just keep the dict reference.
        self.sessions[session.id] = session

@pytest.fixture
def store():
    # Minimal config – values are not used by the mock service
    cfg = AlloyDBConfig(
        user="test",
        password="test",
        database="testdb",
        instance_connection_name="proj:region:inst",
        pool_size=1,
        max_overflow=0,
    )
    s = AlloyDBSessionStore(config=cfg, ttl_seconds=1)
    # Replace the real ADK service with our mock
    s.session_service = MockSessionService()
    return s

def test_write_and_read_within_ttl(store):
    store.write("sess1", "key1", "value1")
    assert store.read("sess1", "key1") == "value1"

def test_expiry_after_ttl(store):
    store.write("sess2", "key2", "value2")
    # Wait longer than the 1‑second TTL
    import time
    time.sleep(1.5)
    assert store.read("sess2", "key2") is None
