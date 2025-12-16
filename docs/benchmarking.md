# Agent Memory Hub Benchmarking Guide

This guide describes how to use the `benchmark_db.py` script to evaluate the performance (latency and payload handling) of different memory backends supported by Agent Memory Hub.

## Overview

The benchmarking script (`benchmark_db.py`) performs a series of Write and Read operations with varying payload sizes (1KB, 10KB, 100KB, 500KB) to measure:

1.  **Write Latency**: Time taken to persist data.
2.  **Read Latency**: Time taken to retrieve data.
3.  **Data Integrity**: Verifies that retrieved data matches the stored payload.

## Prerequisites

Before running the benchmark, ensure you have:

1.  **Installed Dependencies**: The package and its dependencies must be installed.
    ```bash
    pip install .
    ```
2.  **Cloud Credentials**:
    - For **GCS (ADK)**: Ensure you have active Google Cloud credentials (e.g., via `gcloud auth application-default login`).
    - For **AlloyDB**: You need the AlloyDB instance connection name, database user, password, and database name. Also ensure you have the `alloydb` extras installed:
    ```bash
    pip install ".[alloydb]"
    ```

## Running the Benchmark

### 1. Google Cloud Storage (ADK) Backend

To benchmark the default Google Cloud Storage backend:

```bash
python benchmark_db.py --backend adk --region us-central1 --env dev
```

**Parameters:**

- `--backend`: Set to `adk` (default).
- `--region`: GCP Region (default: `us-central1`).
- `--env`: Environment tag used in bucket naming (default: `dev`).

### 2. AlloyDB Backend

To benchmark the AlloyDB backend, you must provide connection details:

```bash
python benchmark_db.py \
  --backend alloydb \
  --region us-central1 \
  --env dev \
  --db-user <YOUR_DB_USER> \
  --db-pass <YOUR_DB_PASSWORD> \
  --db-name <YOUR_DB_NAME> \
  --db-conn <PROJECT:REGION:INSTANCE>
```

**Parameters:**

- `--backend`: Set to `alloydb`.
- `--db-user`: Your database username.
- `--db-pass`: Your database password.
- `--db-name`: The name of the database to use.
- `--db-conn`: The AlloyDB Instance Connection Name (e.g., `my-project:us-central1:my-instance`).
- Note: This requires the `alloydb` extra: `pip install ".[alloydb]"`

### 3. Redis (Memorystore) Backend

To benchmark Redis:

```bash
python benchmark_db.py --backend redis --region us-central1 --redis-host <HOST> --redis-port <PORT>
```

**Parameters:**

- `--backend`: Set to `redis`.
- `--redis-host`: Hostname or IP of the Redis instance.
- `--redis-port`: Port (default: 6379).
- Note: This requires the `redis` extra: `pip install ".[redis]"`

### 4. Firestore Backend

To benchmark Firestore:

```bash
# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
python benchmark_db.py --backend firestore --region us-central1
```

**Parameters:**

- `--backend`: Set to `firestore`.
- Note: This requires the `firestore` extra: `pip install ".[firestore]"`
- Note: Firestore credentials are usually inferred from the environment.

## Interpreting Results

The script outputs a table similar to this:

```text
==================================================
BENCHMARK RESULTS: ADK
==================================================
Size (KB)  | Write (s)  | Read (s)   | Status
--------------------------------------------------
1          | 0.0452     | 0.0321     | SUCCESS
10         | 0.0510     | 0.0385     | SUCCESS
100        | 0.1250     | 0.0910     | SUCCESS
500        | 0.4502     | 0.3801     | SUCCESS
==================================================
```

- **Low Latency**: Smaller numbers are better.
- **Scalability**: Observe how latency increases as payload size increases.
- **Status**: Should always be `SUCCESS`. `DATA MISMATCH` indicates data corruption, and `ERROR`/`FAIL` indicates connection or storage issues.
