# Multi-Region Memory Architecture

`agent-memory-hub` excels in scenarios where data sovereignty is paramount. This guide explains how to set up strict region governance.

## The Concept

In a global application, you might have users in Europe (GDPR) and the US. You want to ensure:

- European user data **never** leaves the EU region (`europe-west1`).
- US user data stays in the US (`us-central1`).

## Configuration

You can enforce this at the client level using the `region_restricted=True` flag.

### European Agent

```python
eu_memory = MemoryClient(
    agent_id="eu_support_bot",
    region="europe-west1",
    region_restricted=True
)
```

If this client attempts to write to a bucket that is NOT in `europe-west1`, the operation will fail with a `RegionViolationError`.

### US Agent

```python
us_memory = MemoryClient(
    agent_id="us_support_bot",
    region="us-central1",
    region_restricted=True
)
```

## Storage Backend Setup

Ensure your underlying storage is correctly provisioned:

- **Google Cloud Storage**: Create buckets named `memory-hub-europe-west1-prod` and `memory-hub-us-central1-prod`.
- **AlloyDB**: Provision instances in the respective regions.

The `MemoryClient` expects the backend resource to verify its own location. For GCS, we check the bucket's location metadata.
