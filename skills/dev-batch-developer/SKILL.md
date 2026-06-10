---
name: dev-batch-developer
description: Guides the agent in developing high-throughput, resilient, and performant batch jobs or data processing pipelines.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Data Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


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

## Step 2: Enterprise Fault Tolerance & State Management
Batch jobs must expect errors and handle them gracefully without crashing mid-way, and must support safe reruns (idempotency).
1. **Idempotent Data Writes**: Use `INSERT OVERWRITE` for partitioned data, or `UPSERT`/`MERGE` for record-level updates. Never blindly append (`INSERT`) without deduplication checks.
2. **Managed Checkpointing**: Do NOT store batch progress in local memory or temporary files. Always use an externalized Control Table (e.g., `batch_job_runs`) to record `last_processed_id` or timestamp.
3. **Record-Level Error Handling**: Wrap individual record processing in `try-catch`. If one record fails, write it to a Dead Letter Queue (DLQ) table and continue to the next.
4. **Retry Mechanism**: Implement exponential backoff retries for transient external API calls.

## Step 3: Performance & Resource Management
1. **Concurrency**: Leverage multi-threading or worker pools when processing is CPU-bound (e.g., heavy file decryption or image manipulation), but limit maximum concurrent threads to prevent resource exhaustion.
2. **Resource Cleanup**: Ensure all file handles, database connections, and network sockets are explicitly closed (e.g., using `finally` blocks, `defer`, or `using` patterns).
3. **Transaction Scope**: Keep database transactions small. Do not wrap the entire batch job in a single transaction as it locks tables and degrades DB performance.

## Step 4: Audit Trails & Data Reconciliation
1. **Automated Reconciliation (Crucial)**: At the end of the job, the pipeline MUST compare the count of records read vs. records written. Alert immediately if `read != written + failed`.
2. **Job Summary Log**: Every execution must log a summary upon exit with Start/End timestamps and exact row counts.
3. **Alerting Thresholds**: Implement check gates to fail the job if the failure/DLQ rate exceeds a threshold (e.g., > 5%).

## Step 5: Code Conventions & Documentation
Instead of hardcoded rules, you MUST apply the specific conventions based on the project's language and framework. Before writing code, consult the appropriate convention file:
- TypeScript/Node.js (Backend): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
- TypeScript/React (Frontend): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
- Rust: [`rust.md`](../../resources/conventions/rust.md)
- Python: [`python.md`](../../resources/conventions/python.md)
- Go: [`go.md`](../../resources/conventions/go.md)

1. **Naming Conventions**: Follow the file suffix rules defined in the convention file.
2. **Business Logic Comments**: Follow the 'Why over How' rule.
3. **Module-level README**: Every newly created module must contain a local `README.md` as mandated by the convention guidelines.

## Step 6: Verification (Definition of Done)
**CRITICAL RULE**: Code is NOT considered "DONE" until it is fully covered by Unit Tests. You must write and verify unit tests before reporting completion.

1. Write unit tests targeting the **Processor** components with mock inputs.
2. Write integration tests executing the whole pipeline end-to-end with a limited, controlled mock dataset.
3. Verify that the batch job handles empty inputs, malformed records, and database timeouts gracefully.
