# Agent Memory Hub

**Enterprise-grade agent memory management solution with region governance.**

`agent-memory-hub` provides a standardized, secure, and compliant way for AI agents to store and recall memories. It enforces region residency requirements (data sovereignty) and provides a clean abstraction over storage backends, defaulting to Google Cloud.

## Features

- **Session-based Memory**: Isolate memory by agent and session ID.
- **Region Governance**: Enforce data residency (e.g., `us-central1`, `europe-west1`).
- **Backend Agnostic**: Adapter pattern supports multiple backends (Default: Google ADK/GCS).
- **Enterprise Security**: No hardcoded secrets, strictly typed, and compliance-ready.

## Installation

```bash
pip install agent-memory-hub
```

## Quick Start

```python
from agent_memory_hub import MemoryClient

# Initialize the client with strict region requirements
memory = MemoryClient(
    agent_id="travel_agent",
    session_id="sess_001",
    region="asia-south1",
    region_restricted=True
)

# Store a memory (will fail if backend is not in asia-south1)
memory.write("User prefers vegetarian food", "episodic")

# Recall memory
print(memory.recall("episodic"))
```
