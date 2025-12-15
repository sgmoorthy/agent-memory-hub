import os

import agent_memory_hub
from agent_memory_hub import MemoryClient

print(
    f"✅ Successfully imported agent-memory-hub version: "
    f"{agent_memory_hub.__version__}"
)
print(f"📍 Loaded from: {agent_memory_hub.__file__}")

# Check if running from site-packages
if (
    "site-packages" in agent_memory_hub.__file__
    or "dist-packages" in agent_memory_hub.__file__
):
    print(
        "🎉 Confirmed: Loading from installed system interpreter "
        "(PyPI installation)."
    )
else:
    print(
        f"⚠️  WARNING: It looks like you are loading from: "
        f"{agent_memory_hub.__file__}"
    )
    print("    This might be a local editable install, NOT the PyPI version.")

print("\n--- Attempting Client Initialization ---")
try:
    # Initialize client
    client = MemoryClient(
        agent_id="pypi-test-agent", 
        session_id="test-session-001", 
        region="us-central1",
        region_restricted=True
    )
    print("✅ MemoryClient initialized successfully.")
    
    print("\n[Optional] Testing GCS Connection...")
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "ℹ️  Skipping actual GCS calls because "
            "GOOGLE_APPLICATION_CREDENTIALS is not set."
        )
        print(
            "    (This is expected if you haven't set up auth "
            "for this test environment)"
        )
    else:
        try:
            client.read("test_key")  # Assuming read is safer/easier
            print("✅ GCS Connection Successful!")
        except Exception as e:
            print(f"❌ GCS Connection Failed: {e}")
            print(
                "    (This logic implies the code works, but cloud "
                "auth/permissions failed.)"
            )

except Exception as e:
    print(f"❌ Client Initialization Failed: {e}")
