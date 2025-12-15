# Feature Roadmap & Contributor Guide

This document tracks the feature status of **Agent Memory Hub**. We welcome contributions for all items in the roadmap!

## 🚀 Completed Features (v0.1.0)

- [x] **Session-based Memory**: Core CRUD operations for storing and retrieving agent memory sessions (JSON).
- [x] **Region Governance**: `RegionGuard` implementation to enforce data sovereignty and verify region compliance.
- [x] **Google Cloud Storage Backend**: `AdkSessionStore` adapter for persisting data to GCS buckets.
- [x] **Backend Agnostic Interfaces**: Abstract base classes (`SessionStore`) to allow easy swapping of storage backends.
- [x] **Secure Configuration**: No hardcoded secrets; fully reliant on IAM and environment variables.

---

## 🛠️ Pending Features (Roadmap)

Please check off these items as they are completed!

### Observability & Monitoring

- [ ] **OpenTelemetry Integration** (Issue #101)
  - _Goal_: Add tracing spans to `read()` and `write()` operations to visualize latency and errors.
  - _Priority_: 🔥 High
- [ ] **Structured Logging** (Issue #102)
  - _Goal_: Implement a structured logger (JSON format) for better ingestion by Cloud Logging/Splunk.
  - _Priority_: High
- [ ] **Prometheus Metrics** (Issue #103)
  - _Goal_: Expose metrics: `memory_write_count`, `memory_read_latencies`, `region_violation_count`.
  - _Priority_: Medium

### Enhanced Storage Backends

- [ ] **AWS S3 Adapter** (Issue #201)
  - _Goal_: Implement `S3SessionStore` using `boto3` to support AWS-based deployments.
  - _Priority_: 🔥 High
- [ ] **Redis / Memcached Adapter** (Issue #202)
  - _Goal_: Add a caching layer or a purely in-memory store for high-speed, ephemeral memory.
  - _Priority_: Medium
- [ ] **Azure Blob Storage** (Issue #203)
  - _Goal_: Adapter for Azure Blob Storage support.
  - _Priority_: Low

### Advanced Memory Features

- [ ] **Vector Search Injection** (Issue #301)
  - _Goal_: Integrate with vector databases (Pinecone, Weaviate) to enable semantic search on memory.
  - _Priority_: 🔥 High
- [ ] **Memory Expiry (TTL)** (Issue #302)
  - _Goal_: Allow setting a Time-To-Live for temporary sessions that auto-delete after X hours.
  - _Priority_: Medium
- [ ] **Encryption at Rest** (Issue #303)
  - _Goal_: Add client-side encryption options (AES-256) before sending data to the backend.
  - _Priority_: High

---

## How to Contribute

1. **Pick an Issue**: Choose an item from the "Pending" list above.
2. **Comment**: Let us know you're working on it.
3. **Fork & Branch**: Create a branch like `feature/101-opentelemetry`.
4. **Implement**: Follow our `CONTRIBUTING.md` guide and add tests.
5. **PR**: Open a Pull Request referencing the Issue ID (e.g., "Closes #101").

Happy coding! 🤖🧠
