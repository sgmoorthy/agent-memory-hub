"""
Example: Using Redis backend with agent-memory-hub.
"""
import os
import sys

# Ensure we can run this from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_memory_hub import MemoryClient
from agent_memory_hub.config.redis_config import RedisConfig


def main():
    # Configure Redis (using local default or env)
    redis_config = RedisConfig(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379"))
    )

    print("--- Initializing Client with Redis Backend ---")
    try:
        client = MemoryClient(
            agent_id="redis-agent",
            session_id="redis-session-1",
            region="us-central1", # Still required for RegionGuard
            backend="redis",
            ttl_seconds=300,
            redis_config=redis_config
        )
        
        print("Writing to Redis...")
        client.write("Hello Redis!", key="greeting")
        
        print("Reading from Redis...")
        val = client.recall(key="greeting")
        print(f"Recalled: {val}")

    except Exception as e:
        print(f"Error (probably incomplete implementation): {e}")

if __name__ == "__main__":
    main()
