# RAG Agent with Stateful Memory

Retrieval-Augmented Generation (RAG) combines search with generation. `agent-memory-hub` adds a third pillar: **State**.

## Why State in RAG?

Standard RAG retrieves documents based on the query. However, it often forgets:

1.  **What was retrieved previously**: Avoiding redundant searches.
2.  **User preferences**: If a user said "I prefer technical docs" 3 turns ago, the RAG retrieval should bias towards that.
3.  **Conversation history**: Multi-turn context.

## Integration Flow

1.  **User Query**: "How do I configure Redis?"
2.  **Memory Check**: Agent checks `memory.recall()` for "Redis configuration" in recent conversational items.
3.  **Retrieval**: If not sufficiently answered in memory, search the vector DB / knowledge base.
4.  **Synthesis**: Generate answer.
5.  **Write Back**: Store the **Result** and the **Source/Context** in `agent-memory-hub`.

```python
# Pseudo-code flow
query = "How do I configure Redis?"

# Check Memory
memories = memory.recall(query=query) # Semantic search over memory
if not memories:
    docs = vector_db.search(query)
    memory.write(f"Retrieved docs for {query}: {docs[0].summary}")
    answer = llm.generate(query, context=docs)
else:
    answer = llm.generate(query, context=memories)

memory.write(f"User asked {query}, Answered: {answer}")
```

See `examples/rag_agent_with_region_memory.py` for a runnable example.
