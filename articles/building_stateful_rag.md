# Building Stateful RAG Agents with Python: A Practical Guide

_Target Audience: Python Developers, AI Engineers_

Most RAG (Retrieval-Augmented Generation) tutorials show you a single loop:
`Query -> Vector Search -> LLM -> Answer`.

But real users don't talk in single loops. They have conversations.
"Show me the pricing." -> "Is that per month?" -> "What about for enterprise?"

If your RAG system is stateless, the second question fails because "that" has no reference.

## adding State to the Loop

Let's build a stateful RAG agent using `agent-memory-hub` and OpenAI.

### Step 1: The Stack

- **LLM**: OpenAI GPT-4
- **Vector DB**: (Any)
- **Memory**: `agent-memory-hub`

### Step 2: The Memory Client

First, install the library:
`pip install agent-memory-hub`

Now, initialize it for your user session:

```python
from agent_memory_hub import MemoryClient
memory = MemoryClient(agent_id="rag_bot", session_id="user_123")
```

### Step 3: The Augmented Loop

Instead of just retrieving documents, we first retrieve _memories_.

```python
def ask(query):
    # 1. Fetch recent conversation history
    history = memory.recall(limit=5)

    # 2. Search docs (if needed)
    docs = vector_store.search(query)

    # 3. Construct Prompt
    prompt = f"""
    Context from previous turns: {history}

    Relevant Documents: {docs}

    User Question: {query}
    """

    # 4. Generate
    response = openai.chat.completions.create(..., messages=[{"role": "user", "content": prompt}])

    # 5. SAVE STATE!
    memory.write(f"User: {query} | Assistant: {response.content}")

    return response.content
```

### Why this is better than `st.session_state`

If you are just building a Streamlit app, local state is fine. But what if your agent runs on a serverless function? Or inside a container that restarts?

`agent-memory-hub` persists this state to distinct backends (GCS, Redis, Postgres) so your agent is robust and scalable.

### Try it out

We've open-sourced the library to help standardize how agents remember.
Check out the [examples folder](https://github.com/sgmoorthy/agent-memory-hub/tree/main/examples) for a full runnable script.
