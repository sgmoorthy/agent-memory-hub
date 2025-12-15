import logging

from agent_memory_hub import MemoryClient
from agent_memory_hub.config.regions import REGION_ASIA_SOUTH1

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

def main():
    print("Initializing Memory Client...")
    
    # In a real scenario, this would connect to GCS. 
    # Ensure you have credentials or mock it.
    
    try:
        memory = MemoryClient(
            agent_id="travel_agent",
            session_id="sess_001",
            region=REGION_ASIA_SOUTH1,
            region_restricted=True
        )

        print(f" writing memory to {REGION_ASIA_SOUTH1}...")
        memory.write("User prefers vegetarian food", "episodic")
        
        print("Recalling memory...")
        result = memory.recall("episodic")
        print(f"Recall result: {result}")

    except Exception as e:
        print(f"An error occurred (expected if no GCS creds/mock): {e}")

if __name__ == "__main__":
    main()
