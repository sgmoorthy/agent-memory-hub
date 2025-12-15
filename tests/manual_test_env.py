from agent_memory_hub.client.memory_client import MemoryClient
from agent_memory_hub.data_plane.adk_session_store import AdkSessionStore
from agent_memory_hub.data_plane.store_factory import StoreFactory
from agent_memory_hub.routing.memory_router import MemoryRouter


def test_store_factory():
    print("Testing StoreFactory...")
    store = StoreFactory.get_store(
        backend="adk",
        region="us-central1",
        bucket_prefix="my-prefix",
        environment="staging"
    )
    
    assert isinstance(store, AdkSessionStore)
    print(f"Bucket Name: {store.bucket_name}")
    assert store.bucket_name == "my-prefix-us-central1-staging"
    print("StoreFactory Test Passed!")

def test_memory_client():
    print("Testing MemoryClient propagation...")
    client = MemoryClient(
        agent_id="test_agent",
        session_id="test_session",
        region="asia-south1",
        environment="dev"
    )
    
    assert client.environment == "dev"
    
    # Check internal router
    router = client._router
    assert isinstance(router, MemoryRouter)
    assert router.environment == "dev"
    
    # Check internal store
    store = router.store
    assert isinstance(store, AdkSessionStore)
    print(f"Client Store Bucket: {store.bucket_name}")
    assert store.bucket_name == "memory-hub-asia-south1-dev"
    print("MemoryClient Test Passed!")

if __name__ == "__main__":
    try:
        test_store_factory()
        test_memory_client()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"FAILED: {e}")
        exit(1)
