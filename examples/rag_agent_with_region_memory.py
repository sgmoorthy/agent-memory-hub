import time

from agent_memory_hub import MemoryClient

# removed unused typing import

class MockRAGSystem:
    """
    A simple mock of a RAG system to demonstrate where Agent Memory Hub fits in.
    """
    def __init__(self):
        self.knowledge_base = {
            "agent_memory_hub": (
                "Agent Memory Hub is a python library for managing AI agent memories "
                "with region governance."
            ),
            "regions": (
                "It supports us-central1, europe-west1, and asia-south1 by default."
            ),
            "backend": (
                "It uses an adapter pattern to support GCS, AlloyDB, Redis, etc."
            )
        }

    def retrieve(self, query: str) -> str:
        # Simple keyword matching for demo
        for key, value in self.knowledge_base.items():
            if key in query.lower():
                return value
        return "No specific knowledge found."

    def generate(self, query: str, context: str) -> str:
        return f"Based on [{context}], the answer to '{query}' is derived."


def run_rag_with_memory():
    # 1. Setup Persistent Memory for the RAG Agent
    # This memory persists across different query sessions for the same user
    memory = MemoryClient(
        agent_id="rag_assistant_01",
        session_id=f"chat_{int(time.time())}",
        region="us-central1"
    )

    rag = MockRAGSystem()
    
    user_queries = [
        "What is agent_memory_hub?",
        "Does it support multiple regions?",
        # "Redis" isn't in our mock KB, but maybe we learned it?
        "Can I use it with Redis?"  
    ]

    print("Starting RAG Session Loops with Memory...\n")

    for i, query in enumerate(user_queries):
        print(f"Process Query {i+1}: '{query}'")
        
        # Step A: Check Memory first (Cache / Short-term memory)
        # We look if we have answered something similar recently 
        # (naive check for this demo)
        previous_memories = memory.recall(limit=5)
        # found_in_memory = False  # Unused variable removed
        
        # Very naive semantic check mock
        for mem in previous_memories:
            if "Redis" in query and "Redis" in mem['content']:
                print(f"  -> Found relevant info in memory: {mem['content']}")
                # found_in_memory = True # In a real system, we might skip retrieval
        
        # Step B: Retrieve from Documents
        retrieved_context = rag.retrieve(query)
        print(f"  -> Retrieved Context: {retrieved_context}")

        # Step C: Update Memory with the Retrieval (for citation or future context)
        # We store what we found so the agent 'statelessly' remembers what it read
        memory.write(
            f"Retrieved for '{query}': {retrieved_context}",
            metadata={"source": "knowledge_base", "query": query}
        )

        # Step D: Generate Answer
        answer = rag.generate(query, retrieved_context)
        print(f"  -> Agent Answer: {answer}")
        
        # Step E: Store the Interaction
        memory.write(
            f"User asked '{query}'. Answered: {answer}",
            metadata={"type": "conversation_history"}
        )
        print("  -> Memory updated.\n")

    print("Session Complete. Memory Trace:")
    for mem in memory.recall(limit=10):
        print(
            f"- [{mem.get('metadata', {}).get('type', 'unknown')}] "
            f"{mem['content'][:50]}..."
        )

if __name__ == "__main__":
    run_rag_with_memory()
