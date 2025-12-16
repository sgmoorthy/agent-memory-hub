# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.6] - 2025-12-16

### Fixed

- **AlloyDB Driver**: Switched from `psycopg2` to `pg8000` for native AlloyDB Connector support, as `psycopg2` is not supported by the connector's helper method.

## [0.3.5] - 2025-12-16

### Added

- **Native AlloyDB Connector Support**: integrated `google-cloud-alloydb-connector` in `AlloyDBSessionStore`. Now, if `db_url` is not provided, the client will automatically establish a secure, authenticated connection to AlloyDB without needing a local Auth Proxy binary or Unix sockets.

## [0.3.4] - 2025-12-16

### Changed

- **AlloyDB Backend Re-architecture**: Replaced `google-adk` dependency with a direct SQLAlchemy implementation for the AlloyDB session store. This resolves API compatibility issues and provides better control over schema and query performance. The underlying table is now explicitly managed as `sessions (session_id TEXT PK, data JSONB)`.

## [0.3.3] - 2025-12-16

### Fixed

- **AlloyDB Usage**: Corrected argument name in `AlloyDBSessionStore` to pass `db_url` instead of `database_uri` to the underlying ADK `DatabaseSessionService`.

## [0.3.2] - 2025-12-16

### Added

- **AlloyDB Configurations**: Added `db_url` support to `AlloyDBConfig` and `AlloyDBSessionStore` to allow explicit connection strings (e.g., for TCP/Auth Proxy connections), overriding the default Cloud SQL Unix socket construction.
- **Benchmark Tool**: Added `--db-url` argument to `benchmark_db.py`.

## [0.3.1] - 2025-12-16

### Fixed

- **CI/Test Robustness**: Updated `test_firestore_store.py` and `test_redis_store.py` to correctly skip tests if optional dependencies (`redis`, `google-cloud-firestore`) are missing.
- **Linting**: Resolved minor line-length and unused import issues in test suite.
- **Client Validation**: Added non-empty checks for `agent_id` and `session_id` in `MemoryClient`.

## [0.3.0] - 2025-12-16

### Added

- **Region Governance**: New `RegionGuard` control plane to enforce data residency (GDPR/Compliance).
- **AlloyDB Backend**: Added `AlloyDBSessionStore` adapter for Google Cloud AlloyDB (PostgreSQL) support.
- **TTL Management**: Added Time-To-Live (TTL) support for memory entries to auto-expire sensitive data.
- **Semantic Models**: Introduced Pydantic models (`EpisodicMemory`, `SemanticMemory`, `ProcedureMemory`) for structured data.
- **Telemetry**: integrated OpenTelemetry for tracing `read`, `write`, and `recall` operations.
- **Documentation**: Complete overhaul with unique SEO-optimized README and new MkDocs-based documentation site.
- **Examples**:
  - `openai_agents_integration.py`: OpenAI API integration pattern.
  - `multi_region_memory_architecture.py`: Demonstration of region-restricted storage.
  - `rag_agent_with_region_memory.py`: RAG pipeline with memory caching.

### Changed

- Refactored `MemoryClient` to support `backend` selection ("adk", "alloydb", "redis", "firestore").
- Updated strict linting rules and security checks in specific CI pipelines.

## [0.2.0] - 2025-12-15

### Added

- **Redis Backend**: Experimental support for Redis-based session storage.
- **Firestore Backend**: Adapter for Google Cloud Firestore.

## [0.1.0] - 2025-12-14

### Added

- Initial release of `agent-memory-hub`.
- Basic `MemoryClient` with GCS (Google Cloud Storage) adapter (`AdkSessionStore`).
- Abstract `SessionStore` interface.
