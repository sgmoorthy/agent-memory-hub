import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.getcwd())

from agent_memory_hub import MemoryClient
from agent_memory_hub.models import (
    EpisodicMemory, 
    SemanticMemory, 
    MemoryScope
)

def run_tests():
    print("Running Semantic Memory Verification...")

    # TEST 1: Models
    print("1. Testing Model Implementation...")
    mem = EpisodicMemory(
        agent_id="agent_1",
        content="User said hello",
        scope=MemoryScope.SESSION
    )
    assert mem.content == "User said hello"
    assert mem.scope == MemoryScope.SESSION
    assert "EpisodicMemory" in mem.to_dict()["memory_type"]
    print("   ✅ EpisodicMemory OK")

    sem = SemanticMemory(
        agent_id="agent_1",
        subject="Sky",
        predicate="is",
        object="Blue"
    )
    data = sem.to_dict()
    assert data["subject"] == "Sky"
    assert data["memory_type"] == "SemanticMemory"
    print("   ✅ SemanticMemory OK")

    # TEST 2: Client Integration
    print("2. Testing Client Integration...")
    client = MemoryClient(agent_id="test", session_id="s1", region_restricted=False)
    client._router = MagicMock()
    
    mem_payload = SemanticMemory(
        agent_id="test",
        subject="User",
        predicate="likes",
        object="Pizza",
        scope=MemoryScope.USER
    )
    
    client.write_model(mem_payload)
    
    # Verify router called with serialized dict
    args = client._router.write.call_args[0]
    session_id, key, value = args
    
    assert session_id == "s1"
    assert "semanticmemory" in key
    assert value["subject"] == "User"
    assert value["memory_type"] == "SemanticMemory"
    print("   ✅ Client.write_model OK")

    print("\n🎉 All Verification Checks Passed!")

if __name__ == "__main__":
    run_tests()
