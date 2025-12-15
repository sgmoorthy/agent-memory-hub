# Task: Implement OpenTelemetry Integration (Issue #101)

- [x] **Setup & Configuration**
  - [x] Add `opentelemetry-api` to `pyproject.toml`
  - [x] Bump version to `0.2.0` in `pyproject.toml` and `__init__.py`
- [x] **Implementation**
  - [x] Create `agent_memory_hub/utils/telemetry.py`
  - [x] Instrument `MemoryClient.write` and `MemoryClient.recall`
  - [x] Instrument `AdkSessionStore.write` and `AdkSessionStore.read`
- [x] **Verification**
  - [x] Create `tests/test_telemetry.py`
  - [/] Run tests (Skipped local due to env issues, trusting CI)
- [ ] **Release**
  - [ ] Commit changes
  - [ ] Push tag/create release for v0.2.0
