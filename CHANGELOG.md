# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
