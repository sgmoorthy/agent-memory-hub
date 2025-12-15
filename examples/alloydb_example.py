"""
Example: Using AlloyDB backend with agent-memory-hub.

This example demonstrates how to use AlloyDB (PostgreSQL) as the storage backend.
"""

from agent_memory_hub import MemoryClient
from agent_memory_hub.config.alloydb_config import AlloyDBConfig

# Configure AlloyDB connection
alloydb_config = AlloyDBConfig(
    instance_connection_name="my-project:us-central1:my-instance",
    database="memory_db",
    user="memory_user",
    password="secure_password",  # Use Secret Manager in production!
    region="us-central1",
    pool_size=5,
    max_overflow=10,
)

# Create client with AlloyDB backend
client = MemoryClient(
    agent_id="agent-123",
    session_id="session-456",
    region="us-central1",
    backend="alloydb",  # Use AlloyDB instead of GCS
    alloydb_config=alloydb_config,
    ttl_seconds=3600,  # Optional: 1-hour TTL
)

# Use exactly like the GCS backend
client.write("Meeting notes from AlloyDB", "episodic")
notes = client.recall("episodic")
print(f"Retrieved from AlloyDB: {notes}")


# Alternative: Load config from environment variables
# Set these environment variables:
# - ALLOYDB_INSTANCE=my-project:us-central1:my-instance
# - ALLOYDB_DATABASE=memory_db
# - ALLOYDB_USER=memory_user
# - ALLOYDB_PASSWORD=secure_password
# - ALLOYDB_REGION=us-central1

config_from_env = AlloyDBConfig.from_env()

client_env = MemoryClient(
    agent_id="agent-789",
    session_id="session-101",
    region="us-central1",
    backend="alloydb",
    alloydb_config=config_from_env,
)

client_env.write("Data from env config", "semantic")
