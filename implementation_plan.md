# Implementation Plan - OpenTelemetry Integration (Issue #101)

## Goal Description

Implement OpenTelemetry observability to trace `read()` and `write()` operations. This will allow users to visualize latency, errors, and call graphs across the `MemoryClient`, `MemoryRouter`, and `SessionStore` layers.

## User Review Required

> [!IMPORTANT]
> This change adds `opentelemetry-api` as a core dependency.
> Users will need to configure an OTel exporter (e.g., to Jaeger, Zipkin, or Google Cloud Trace) in their application to actually see the traces, though the library itself will be agnostic.

## Proposed Changes

### Dependencies

#### [MODIFY] [pyproject.toml](file:///d:/projects/agentmemoryhub/pyproject.toml)

- Add `opentelemetry-api>=1.20.0` to `dependencies`.

### Core Telemetry

#### [NEW] [telemetry.py](file:///d:/projects/agentmemoryhub/agent_memory_hub/utils/telemetry.py)

- Create a utility module to get a configured `Tracer`.
- Define constants for attribute names (e.g., `agent.id`, `session.id`, `region`).

### Client Layer

#### [MODIFY] [memory_client.py](file:///d:/projects/agentmemoryhub/agent_memory_hub/client/memory_client.py)

- Add `@trace_span` or manual `tracer.start_as_current_span` context managers to `write()` and `recall()`.
- Record attributes: `agent.id`, `session.id`, `region`.

### Data Plane Layer

#### [MODIFY] [adk_session_store.py](file:///d:/projects/agentmemoryhub/agent_memory_hub/data_plane/adk_session_store.py)

- Instrument `write()` and `read()` to show the actual latency of the storage backend calls.
- Record attributes: `bucket.name`, `object.key`.

## Verification Plan

### Automated Tests

- Create a new test file `tests/test_telemetry.py`.
- Use `opentelemetry.sdk.trace.InMemorySpanExporter` to capture spans generated during test execution.
- Assert that:
  - Spans are created with correct names (e.g., `MemoryClient.write`).
  - Spans contain expected attributes (`agent_id`, `session_id`).
  - Spans are properly nested (Client calls -> Router calls -> Store calls).

### Manual Verification

- Run a script that performs memory operations and check console/debug output if a console exporter is configured (optional).
