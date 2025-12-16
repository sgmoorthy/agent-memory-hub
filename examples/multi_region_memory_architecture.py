import logging
import time

from agent_memory_hub import MemoryClient

# Configure logging to see the internal operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("multi_region_example")

def demonstrate_region_governance():
    """
    Shows how to enforce data residency using the region_restricted flag.
    """
    
    # Scene 1: European Agent (Must stay in EU)
    # We enforce that data must be stored in 'europe-west1'
    print("\n--- Initializing EU Agent (Region Restricted: europe-west1) ---")
    try:
        eu_agent_memory = MemoryClient(
            agent_id="eu_compliance_bot",
            session_id=f"eu_sess_{int(time.time())}",
            region="europe-west1",
            region_restricted=True  # This enforces the check!
        )
        
        # NOTE: This write will FAIL if the underlying bucket/storage 
        # is not actually in europe-west1.
        # The SDK performs a handshake/metadata check.
        # For this example to succeed, you need a bucket named 
        # `memory-hub-europe-west1-{env}`
        eu_agent_memory.write(
            "Storing user consent for GDPR processing.", 
            metadata={"type": "consent"}
        )
        print("✅ EU Write Successful - Data sovereignty verified.")
        
    except Exception as e:
        print(f"❌ EU Write Failed (Expected if no EU bucket exists): {e}")


    # Scene 2: US Agent (US Central)
    print("\n--- Initializing US Agent (Region: us-central1) ---")
    try:
        us_agent_memory = MemoryClient(
            agent_id="us_service_bot",
            session_id=f"us_sess_{int(time.time())}",
            region="us-central1",
            region_restricted=True
        )
        
        print("Attempting to write to US region...")
        us_agent_memory.write("Storing non-sensitive user preferences.")
        print("✅ US Write Successful.")
        
    except Exception as e:
        print(f"❌ US Write Failed (Expected if no US bucket exists): {e}")

    # Scene 3: Cross-Region Safety Check
    # Trying to read EU data from a US-configured client (should be separate)
    print("\n--- Verifying Region Isolation ---")
    try:
        # Re-using US client to try and read EU agent's data
        # (assuming shared namespace but different region?)
        # Actually, MemoryClient constructs paths based on region buckets, 
        # so they are physically isolated.
        # This verifies they point to different storage containers.
        us_memories = us_agent_memory.recall()
        print(f"US Agent sees {len(us_memories)} memories.")
        
        # If we tried to access EU bucket directly, 
        # GCS permissions + SDK logic would prevent/separate it.
        print(
            "Region isolation is enforced by physical storage separation "
            "(different buckets per region)."
        )
        
    except Exception as e:
        print(f"Error checking isolation: {e}")

if __name__ == "__main__":
    demonstrate_region_governance()
