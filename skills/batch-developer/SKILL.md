---
name: batch-developer
description: Guides the agent in developing high-throughput, resilient, and performant batch jobs or data processing pipelines.
---

Develop Batch feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify batch processors, ETL pipelines, and recurring cron tasks.

## Step 1: Establish Pipeline Architecture (Reader-Processor-Writer)
Design the batch processing logic following a structured flow to separate concerns:
1. **Reader (Input)**:
   * Fetch data in chunks/pages (e.g., SQL offset paging, cursor-based streaming) to avoid loading massive datasets into memory at once.
   * Prevent Out-of-Memory (OOM) errors by using streams or generator functions.
2. **Processor (Core)**:
   * Perform validation, filtering, and data transformations.
   * Keep business logic pure and decoupled from data storage APIs.
3. **Writer (Output)**:
   * Commit processed items in batches (e.g., bulk insert/upsert SQL statements) to optimize database network overhead.
   * Set dynamic batch size parameters (e.g., write every 500 or 1000 items).

## Step 2: Fault Tolerance & Resilience
Batch jobs must expect errors and handle them gracefully without crashing mid-way:
1. **Record-Level Error Handling**: Wrap individual record processing in `try-catch` blocks. If one record fails validation or parsing, log the error, increment the failure counter, and continue to the next record.
2. **Skip and DLQ (Dead Letter Queue)**: Write failed records to a separate log file, database table, or queue (DLQ) for manual auditing or re-processing.
3. **Retry Mechanism**: Implement exponential backoff retries for transient external dependencies (e.g., fetching a profile from an external API).
4. **Checkpointing & Restartability**: For long-running batch jobs, save progress periodically (e.g., store the last successfully processed ID). In case of crash, allow the job to resume from the last checkpoint rather than restarting from scratch.

## Step 3: Performance & Resource Management
1. **Concurrency**: Leverage multi-threading or worker pools when processing is CPU-bound (e.g., heavy file decryption or image manipulation), but limit maximum concurrent threads to prevent resource exhaustion.
2. **Resource Cleanup**: Ensure all file handles, database connections, and network sockets are explicitly closed (e.g., using `finally` blocks, `defer`, or `using` patterns).
3. **Transaction Scope**: Keep database transactions small. Do not wrap the entire batch job in a single transaction as it locks tables and degrades DB performance.

## Step 4: Audit Trails & Telemetry
1. **Job Summary Log**: Every execution must log a summary upon exit:
   * Start and End timestamps.
   * Total records read.
   * Total records processed successfully.
   * Total records skipped/failed.
2. **Alerting Thresholds**: Implement check gates to fail the job or alert operators if the failure rate exceeds a certain percentage (e.g., if > 5% of records fail).

## Step 5: Verification (Definition of Done)
1. Write unit tests targeting the **Processor** components with mock inputs.
2. Write integration tests executing the whole pipeline end-to-end with a limited, controlled mock dataset.
3. Verify that the batch job handles empty inputs, malformed records, and database timeouts gracefully.
