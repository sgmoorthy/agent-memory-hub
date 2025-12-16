# Feature Roadmap & Contributor Guide

This document tracks the feature status of **Agent Memory Hub**. We welcome contributions for all items in the roadmap!

## 🚀 Completed Features (v0.3.0)

- [x] **Session-based Memory**: Core CRUD operations for storing and retrieving agent memory sessions (JSON).
- [x] **Region Governance**: `RegionGuard` implementation to enforce data sovereignty and verify region compliance.
- [x] **Google Cloud Storage Backend**: `AdkSessionStore` adapter for persisting data to GCS buckets.
- [x] **Backend Agnostic Interfaces**: Abstract base classes (`SessionStore`) to allow easy swapping of storage backends.
- [x] **Secure Configuration**: No hardcoded secrets; fully reliant on IAM and environment variables.
- [x] **Memory Expiry (TTL)**: Configurable Time-To-Live for ephemeral sessions.
- [x] **AlloyDB Backend**: PostgreSQL-compatible backend for high-performance structured memory.
- [x] **Redis Backend**: Low-latency backend using Redis/Memorystore.
- [x] **Firestore Backend**: Serverless document store backend.
- [x] **OpenTelemetry Integration**: Tracing spans for `read()` and `write()` operations.
- [x] **Benchmarking Suite**: Script to evaluate latency across backends.

---

## 🔮 Platform Vision: Self-Managed Agent Memory

The following is a comprehensive list of capabilities required to evolve Agent Memory Hub into a fully self-managed agent memory platform.

### Semantic Model & Schemas

- [ ] **First-class Memory Types**: Define types for user profile, session, agent, episodic, task/goal, preference, constraint, skill/knowledge, and team memory.
- [ ] **Multi-level Scopes**: Support identity-scoped (user_id), session/thread, agent_id, tenant/project, and shared/team scopes with precedence rules.
- [ ] **Relationships**: Add graph-style relationships between memories (parent/child, supersedes, related_to, depends_on) and tagging.

### Extraction & Consolidation Pipelines

- [ ] **Memory Generation Pipeline**: Turn conversation history, tool traces, and events into structured memories at configurable intervals.
- [ ] **Dual Write Modes**:
  - Automatic extraction (background job) using LLMs.
  - Explicit "Memory-as-a-tool" functions for agents.
- [ ] **Consolidation Engine**: Merge new info into existing memories, handle conflicts (old vs new preference), and summarize threads.
- [ ] **Configurable Extraction Policies**: Topic filters, few-shot examples, importance thresholds, and per-type rules.
- [ ] **Multimodal Extraction**: Process text, images, and documents into textual memories.

### Retrieval, Ranking & Context Shaping

- [ ] **Pluggable Semantic Retrieval**: Vector embeddings + hybrid (keyword + vector) search, scoped by identity/session/type/time.
- [ ] **Ranking Strategies**: Tunable weights for relevance, recency, importance, and frequency.
- [ ] **Short vs Long-term Memory**: Whiteboard-style "working set" memory vs persistent long-term store.
- [ ] **Context Compaction**: Summarizers to compress retrieved memories and history into model-ready prompts.

### Lifecycle, TTL & Governance

- [ ] **Granular TTL**: Per-memory and per-type TTL configuration with automatic garbage collection.
- [ ] **Retention Policies**: Project/tenant level retention (e.g., legal holds, "forget after N days unless pinned").
- [ ] **Right-to-be-Forgotten APIs**: Explicit APIs to delete by user, type, or time range (GDPR compliance).
- [ ] **Memory Versioning**: Full change history and diff inspection (source trace, author, timestamp).
- [ ] **Policy Engine**: RBAC/ABAC policies controlling which agents can read/write which memory scopes.

### Agent & Runtime Integration

- [ ] **Framework Adapters**: Native tools for LangGraph, Semantic Kernel, AutoGen, CrewAI, etc.
- [ ] **Declarative Integration**: Config-level toggles (e.g., "attach long_term_memory: true").
- [ ] **Auto-hooks**: Middleware for automatic memory storage after turns and retrieval before steps.
- [ ] **Multi-agent Patterns**: Handoffs between agents with memory-aware baton passing.

### Identity, Tenancy & Portability

- [ ] **Strong Identity Model**: Support for user_id, device_id, org_id, agent_id, and composite keys.
- [ ] **Multi-tenant Isolation**: Per-tenant quotas, throughput limits, and dedicated/shared backends honoring data residency.
- [ ] **Import/Export APIs**: Migration schemas for moving memories between providers.

### Ops, Observability & Tooling

- [ ] **Rich Metrics**: Hit rates, extraction volume, TTL expirations, and per-tenant dashboards (Prometheus/Grafana).
- [ ] **End-to-End Tracing**: Provenance tracking (which memories influenced an agent response).
- [ ] **Structured Logging**: JSON logging for pipelines and operations.
- [ ] **Admin Console**: UI to browse, search, edit, redact, and export memories.
- [ ] **Environment Awareness**: Tooling for dev/stage/prod migrations and seeding.

### Safety, Privacy & Compliance

- [ ] **PII Protection**: Detect, mask, or encrypt sensitive fields during extraction/storage.
- [ ] **Redaction Policies**: Configurable redaction before write and retrieval.
- [ ] **Audit Logging**: Comprehensive compliance exports for legal/security.
- [ ] **Guardrails**: Limits on memory type access based on agent purpose.

### Performance & Scalability

- [ ] **Async Pipelines**: Background processing for extraction/consolidation to avoid blocking real-time turns.
- [ ] **Hybrid Storage**: Configurable mix of Vector + KV + Relational + Graph storage.
- [ ] **Sharding**: Strategies for large tenants and high-volume workloads.
- [ ] **Backpressure & Rate Limiting**: Protection for downstream vector stores and LLMs.

### Infrastructure Adapters (Backlog)

- [ ] **AWS S3 Backend**: Adapter for AWS S3.
- [ ] **Azure Blob Backend**: Adapter for Azure Blob Storage.
- [ ] **Encryption at Rest**: Client-side encryption integration.

---

## How to Contribute

1. **Pick an Issue**: Choose an item from the lists above.
2. **Comment**: Let us know you're working on it.
3. **Fork & Branch**: Create a branch.
4. **Implement**: Follow `CONTRIBUTING.md`.
5. **PR**: Open a Pull Request.

Happy coding! 🤖🧠
