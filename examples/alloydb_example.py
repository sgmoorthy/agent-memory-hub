"""
AlloyDB Integration Examples for Agent Memory Hub.

This script demonstrates three ways to connect to AlloyDB:
1. Production: Using the Google Cloud SQL Connector (recommended).
2. Development: Using a direct Connection URL (e.g., via Auth Proxy or TCP).
3. Environment Variables: Configuring the client via environment.
"""

from agent_memory_hub import MemoryClient
from agent_memory_hub.config.alloydb_config import AlloyDBConfig

# ==============================================================================
# OPTION 1: Production (Cloud SQL Connector)
# ==============================================================================
# This method uses the 'google-cloud-alloydb-connector' to securely connect
# using the instance connection name. It handles IAM auth automatically.
# ------------------------------------------------------------------------------
print("\n--- Option 1: Cloud SQL Connector (Production) ---")

prod_config = AlloyDBConfig(
    # Format: project:region:cluster-instance
    instance_connection_name="my-project:us-central1:my-instance",
    database="memory_db",
    user="memory_user",
    # In production, fetch this from Secret Manager!
    password="secure_password",  # noqa: S106
    region="us-central1",
    pool_size=5,
)

# Instantiate client
# This will try to connect (and fail if not actually running against real AlloyDB)
try:
    prod_client = MemoryClient(
        agent_id="agent-prod",
        session_id="session-001",
        region="us-central1",
        backend="alloydb",
        alloydb_config=prod_config
    )
    print("Client configured for Cloud SQL Connector execution.")
except Exception as e:
    print(f"Prod client init skipped (expected without real DB): {e}")


# ==============================================================================
# OPTION 2: Direct Connection String (Development / Proxy)
# ==============================================================================
# This method uses 'db_url' to bypass the connector. 
# Useful for:
# - Connecting to instances via TCP/IP (e.g., Auth Proxy running locally on 5432)
# - Connecting to a local PostgreSQL container for testing
# ------------------------------------------------------------------------------
print("\n--- Option 2: Direct Connection URL (Dev/Proxy) ---")

dev_config = AlloyDBConfig(
    # Full SQLAlchemy connection string
    # Syntax: postgresql+psycopg2://user:password@host:port/dbname
    db_url="postgresql+psycopg2://postgres:secret@127.0.0.1:5432/memory_db",
    
    # These fields are required by the class type hint but IGNORED when db_url is set.
    # You can leave them empty or provide dummies.
    instance_connection_name="", 
    database="", 
    user="", 
    password="", 
    region="us-central1"
)

try:
    dev_client = MemoryClient(
        agent_id="agent-dev",
        session_id="session-002",
        region="us-central1",
        backend="alloydb",
        alloydb_config=dev_config
    )
    print("Client configured for Direct URL execution.")
    
    # Functional Verification
    print(">> Testing Write...")
    test_content = "This is a test memory entry for AlloyDB verification."
    dev_client.write(test_content, "verification_key")
    print("   Write successful.")

    print(">> Testing Read...")
    retrieved = dev_client.recall("verification_key")
    print(f"   Retrieved: {retrieved}")
    
    if retrieved == test_content:
        print(">> ✅ VERIFICATION SUCCESS: Data retrieved matches written content.")
    else:
        print(f">> ❌ VERIFICATION FAILED: Expected '{test_content}', got '{retrieved}'")

except Exception as e:
    print(f"Dev client verification skipped/failed: {e}")


# ==============================================================================
# OPTION 3: Environment Variables
# ==============================================================================
# Ideal for 12-factor apps. 
# Set the following environment variables before running:
#
# export ALLOYDB_INSTANCE="my-project:us-central1:my-instance"
# export ALLOYDB_DATABASE="memory_db"
# export ALLOYDB_USER="memory_user"
# export ALLOYDB_PASSWORD="secure_password"
# export ALLOYDB_REGION="us-central1"
#
# OR for URL override:
# export ALLOYDB_DB_URL="postgresql+psycopg2://..."
# ------------------------------------------------------------------------------
print("\n--- Option 3: Environment Variables ---")

# Automatically loads from env vars
env_config = AlloyDBConfig.from_env()

# Note: This will raise KeyError if env vars are missing
print("Config loaded from env (if vars were set).")
