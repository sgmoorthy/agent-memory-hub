import sys

try:
    import agent_memory_hub  # noqa: F401
    from agent_memory_hub import MemoryClient  # noqa: F401
except ImportError:
    print("❌ Failed to import agent_memory_hub")
    sys.exit(1)

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

print("\n--- Checking Extras imports ---")

# Check AlloyDB
try:
    from agent_memory_hub.config.alloydb_config import AlloyDBConfig  # noqa: F401
    print("✅ AlloyDB module importable.")
except ImportError:
    print("ℹ️  AlloyDB modules not importable (extra not installed?)")

# Check Redis
try:
    from agent_memory_hub.config.redis_config import RedisConfig  # noqa: F401
    print("✅ Redis module importable.")
except ImportError:
    print("ℹ️  Redis modules not importable (extra not installed?)")

# Check Semantic Models
try:
    from agent_memory_hub.models import BaseMemory, SemanticMemory  # noqa: F401
    print("✅ Semantic Memory Models importable.")
except ImportError:
    print("❌ Semantic Memory Models FAILED to import.")


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
    
    # Try importing newly added stores directly to verify structural integrity
    try:
        from agent_memory_hub.data_plane.store_factory import StoreFactory  # noqa: F401
        print("✅ StoreFactory importable")
    except ImportError as e:
        print(f"❌ Failed to import StoreFactory: {e}")

except Exception as e:
    print(f"❌ Client Initialization Failed: {e}")

print("\nVerification Complete.")
