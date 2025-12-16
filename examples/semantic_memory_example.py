"""
Example script demonstrating Semantic Memory Models.
"""
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from agent_memory_hub import MemoryClient
from agent_memory_hub.config.redis_config import RedisConfig
from agent_memory_hub.models import (
    EntityMemory,
    EpisodicMemory,
    MemoryScope,
    SemanticMemory,
)


def main():
    print("--- Semantic Memory Example ---")
    
    # 1. Initialize Client (using Redis fallback to local if available)
    # Note: For this example to actually persist, you need a backend. 
    # We will assume Redis is running locally for demonstration, 
    # or default to ADK (which needs auth).
    
    # Let's try to use Redis if available, else standard
    client = MemoryClient(
        agent_id="researcher_gpt",
        session_id="session_101",
        region="us-central1",
        region_restricted=False,  # Relax for local test
        backend="redis",
        redis_config=RedisConfig(host="localhost", port=6379),
        environment="dev"
    )

    print("Client initialized.")

    # 2. Create an Entit Profile (The User)
    user_profile = EntityMemory(
        agent_id="system", # Created by system
        entity_id="user_john_doe",
        entity_type="user",
        attributes={
            "name": "John Doe",
            "subscription": "premium",
            "preferences": {"theme": "dark"}
        },
        scope=MemoryScope.GLOBAL
    )
    
    print(f"\nWriting Entity: {user_profile.entity_id}")
    try:
        client.write_model(user_profile)
        print("Success.")
    except Exception as e:
        print(f"Write failed (backend likely not reachable): {e}")

    # 3. Create a Semantic Fact
    fact = SemanticMemory(
        agent_id="researcher_gpt",
        subject="Python",
        predicate="created_by",
        object="Guido van Rossum",
        tags=["programming", "history"],
        confidence=0.99
    )
    
    print(f"\nWriting Fact: {fact.subject} {fact.predicate} {fact.object}")
    try:
        client.write_model(fact)
        print("Success.")
    except Exception as e:
        print(f"Write failed: {e}")

    # 4. Create an Episode
    episode = EpisodicMemory(
        agent_id="researcher_gpt",
        content="User John asked about the history of Python.",
        source="chat_interface",
        participants=["user_john_doe", "researcher_gpt"],
        scope=MemoryScope.SESSION
    )
    
    print(f"\nWriting Episode: {episode.content}")
    try:
        client.write_model(episode)
        print("Success.")
    except Exception as e:
        print(f"Write failed: {e}")

    # 5. Read back (Manually constructing key for demo)
    # In a real app, you'd use a retrieval engine or search
    key = f"semanticmemory/{fact.id}"
    print(f"\nReading back fact via key: {key}")
    try:
        data = client.recall(key)
        if data:
            print(f"Recovered Data: {data}")
            print(f"Memory Type: {data.get('memory_type')}")
        else:
            print("Not found.")
    except Exception as e:
        print(f"Read failed: {e}")

if __name__ == "__main__":
    main()
