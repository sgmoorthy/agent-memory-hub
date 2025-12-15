# Agent Memory Hub Architecture

This document describes the high-level architecture and data flow of the `agent-memory-hub` package.

## High-Level Architecture

The `agent-memory-hub` is designed with a layered architecture to ensure separation of concerns between public API, governance (region enforcement), and data persistence.

```mermaid
graph TD
    Agent["Agent (LLM)"] --> Client["MemoryClient"]

    subgraph "Agent Memory Hub"
        Client --> Router["MemoryRouter"]

        Router --> Guard["RegionGuard"]
        Router --> Factory["StoreFactory"]

        Factory --> Store["SessionStore (Interface)"]
    end

    subgraph "Data Plane"
        Store -.->|Implements| ADK["AdkSessionStore"]
        ADK --> GCS[("Google Cloud Storage")]
    end

    classDef component fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef storage fill:#fff3e0,stroke:#ff6f00,stroke-width:2px;

    class Client,Router,Guard,Factory,Store component;
    class ADK,GCS storage;
```

## Component Overview

### 1. Client Layer (`MemoryClient`)

The entry point for the application. It initializes the session context (Agent ID, Session ID) and configures the region requirements.

- **Responsibility**: Public API, Session Context management.

### 2. Routing Layer (`MemoryRouter`)

Acts as the central coordinator. It receives requests from the client and ensures they are routed to the correct data store while enforcing governance rules.

- **Responsibility**: Coordination, Enforcing interaction between Guard and Store.

### 3. Control Plane (`RegionGuard`)

The governance engine. It validates that operations are permitted in the requested region.

- **Responsibility**: Data Sovereignty enforcement, Region validation.

### 4. Data Plane (`StoreFactory` & `SessionStore`)

Manages the physical persistence of data.

- **StoreFactory**: Abstraction to create the correct store backend based on configuration (e.g., ADK/GCS).
- **SessionStore**: Abstract interface for CRUD operations.
- **AdkSessionStore**: Concrete implementation using Google Cloud Storage.

## Data Flow

### Write Operation Flow

This sequence diagram illustrates how a memory write operation is governed and verified before reaching storage.

```mermaid
sequenceDiagram
    participant Agent
    participant Client as MemoryClient
    participant Router as MemoryRouter
    participant Guard as RegionGuard
    participant Store as AdkSessionStore

    Agent->>Client: write(key, value)
    Client->>Router: write(session_id, key, value)

    rect rgb(240, 248, 255)
        note right of Router: Region Governance Check
        Router->>Guard: check_residency(current_region)
        Guard-->>Router: OK (or Raise Error)
    end

    Router->>Store: write(session_id, key, value)
    Store->>Store: _get_bucket()
    Store->>GoogleCloud: upload_blob()
    GoogleCloud-->>Store: Success
    Store-->>Router: Success
    Router-->>Client: Success
    Client-->>Agent: Success
```

### Read Operation Flow

Reading follows a similar governed path to ensure data is retrieved from the expected region.

```mermaid
sequenceDiagram
    participant Agent
    participant Client as MemoryClient
    participant Router as MemoryRouter
    participant Store as AdkSessionStore

    Agent->>Client: recall(key)
    Client->>Router: read(session_id, key)

    Router->>Router: RegionGuard.check_residency()

    Router->>Store: read(session_id, key)
    Store->>GoogleCloud: download_blob()
    GoogleCloud-->>Store: JSON Data
    Store-->>Router: Value
    Router-->>Client: Value
    Client-->>Agent: Value
```

## Security & Governance Model

1.  **Strict Region Check**: The `RegionGuard` is initialized with a specific region. Any operation routed through the `MemoryRouter` triggers a check against this guard. If the context of the operation does not match the locked region, a `RuntimeError` is raised immediately, preventing cross-region data leaks.
2.  **No Credentials in Code**: The `AdkSessionStore` uses `google.auth.default()`, ensuring that no secrets are handled by the library itself. Identity is managed via IAM roles attached to the compute environment.

## Agent Integration Pattern

This section visualizes how an Autonomous Agent (e.g., a ReAct loop) integrates with the Memory Hub. The Agent uses the Hub as its long-term memory store between reasoning steps.

```mermaid
sequenceDiagram
    participant LLM as LLM Model
    participant Agent as Agent Loop
    participant Tools as Tool Executor
    participant Memory as MemoryClient

    Note over Agent: New Task Received

    Agent->>Memory: recall("task_history")
    Memory-->>Agent: Previous context/learnings

    Agent->>LLM: Prompt (Context + New Task)
    LLM-->>Agent: "Thought: I need to use Tool A..."

    Agent->>Tools: Execute Tool A
    Tools-->>Agent: Tool Output

    Agent->>Memory: write("intermediate_step", Tool Output)
    Memory-->>Agent: Acknowledged

    Agent->>LLM: Prompt (Update with Tool Output)
    LLM-->>Agent: "Final Answer: ..."

    Agent->>Memory: write("final_result", Answer)
```

The `MemoryClient` serves as the state persistence layer for the Agent, allowing it to remain stateless itself while maintaining continuity across complex, multi-step execution flows.
