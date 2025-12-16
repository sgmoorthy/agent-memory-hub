"""
Example: Using Firestore backend with agent-memory-hub.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_memory_hub import MemoryClient

def main():
    print("--- Initializing Client with Firestore Backend ---")
    try:
        # Note: Expects GOOGLE_APPLICATION_CREDENTIALS to be set
        client = MemoryClient(
            agent_id="firestore-agent",
            session_id="fs-session-1",
            region="us-central1", 
            backend="firestore",
            ttl_seconds=3600
        )
        
        print("Writing to Firestore...")
        client.write("Stored in Firestore doc", key="persistent_fact")
        
        print("Reading from Firestore...")
        val = client.recall(key="persistent_fact")
        print(f"Recalled: {val}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
