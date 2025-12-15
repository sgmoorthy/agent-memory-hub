"""
Example: Using TTL (Time-To-Live) with agent-memory-hub.

This example demonstrates how to use TTL to automatically expire memory entries.
"""

from agent_memory_hub import MemoryClient

# Example 1: Memory with 1-hour TTL
client = MemoryClient(
    agent_id="agent-123",
    session_id="session-456",
    region="us-central1",
    ttl_seconds=3600,  # 1 hour = 3600 seconds
)

# Write some data
client.write("Important meeting notes", "episodic")
client.write("User preferences", "semantic")

# Read immediately - works fine
notes = client.recall("episodic")
print(f"Notes: {notes}")

# After 1 hour, the data will automatically expire
# client.recall("episodic") would return None


# Example 2: No TTL (permanent storage)
permanent_client = MemoryClient(
    agent_id="agent-789",
    session_id="session-101",
    region="us-central1",
    ttl_seconds=None,  # No expiry
)

permanent_client.write("Long-term knowledge", "semantic")
# This data never expires


# Example 3: Short TTL for temporary sessions (5 minutes)
temp_client = MemoryClient(
    agent_id="agent-temp",
    session_id="temp-session",
    region="us-central1",
    ttl_seconds=300,  # 5 minutes
)

temp_client.write("Temporary conversation context", "context")
