# OpenAI Agents Integration

This guide demonstrates how to integrate `agent-memory-hub` with direct OpenAI API calls to create stateful agents.

## Overview

Stateless models like GPT-4 do not remember previous interactions. By using `agent-memory-hub`, you can fetch relevant context from previous sessions and inject it into the `system` prompt of your current generation.

## Implementation

The core pattern involves:

1.  **Recall**: Fetch relevant memories before calling the LLM.
2.  **Augment**: Add these memories to the conversation history or system prompt.
3.  **Generate**: Call the OpenAI API.
4.  **Store**: Save the new interaction (user query + agent response) back to memory.

## Code Example

Below is a simplified snippets from our `examples/openai_agents_integration.py` script.

```python
import openai
from agent_memory_hub import MemoryClient

# 1. Initialize Memory
memory = MemoryClient(agent_id="my_agent", session_id="session_1")

# 2. Recall Context
recent_memories = memory.recall(limit=5)
context_str = "\n".join([m['content'] for m in recent_memories])

# 3. Augment System Prompt
system_prompt = f"""
You are a helpful assistant.
Here is what you know about the user:
{context_str}
"""

# 4. Call OpenAI
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Book me a flight to my usual destination."}
    ]
)
```

## Best Practices

- **Summarization**: If memory grows too large, consider having a background process summarize older memories into concise facts.
- **Metadata**: Store metadata like `topic` or `sentiment` to filter memories later during recall.
