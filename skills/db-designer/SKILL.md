---
name: db-designer
description: Guides the agent in designing database schemas, ensuring data integrity with constraints, defining indexes, and managing migrations.
---

Design database schema/migration for: $ARGUMENTS

Follow these guidelines to plan, implement, and verify database tables, relationships, and schema migrations.

## Step 1: Relational Schema Design
1. **Identify Entities & Relationships**: Define tables and establish clear mappings:
   * **One-to-One (1:1)**: Link using a shared primary key or a unique foreign key constraint.
   * **One-to-Many (1:N)**: Include a foreign key in the child table.
   * **Many-to-Many (N:M)**: Establish a junction table containing foreign keys referencing both entities, with a composite primary key.
2. **Database Normalization**: Apply normalization up to Third Normal Form (3NF) to minimize data redundancy. De-normalize intentionally only for critical performance reads, and document the trade-offs.
3. **Optimized Data Types**: Choose appropriate column types (e.g., use `uuid` or `bigint` for auto-incrementing primary keys, `varchar(N)` instead of unlimited `text` when lengths are constrained, and `timestamptz` for date-times).

## Step 2: Strict Integrity Constraints
Use database-level constraints to guarantee data consistency, avoiding reliance solely on application-level validations:
1. **Not Null**: Explicitly set columns as `NOT NULL` unless they are truly optional.
2. **Foreign Key Integrity**: Define relational behaviors (e.g., `ON DELETE CASCADE` or `ON DELETE SET NULL`) for all foreign keys to prevent orphaned records.
3. **Unique Constraints**: Apply `UNIQUE` constraints for columns that must not duplicate (e.g., email, slug).
4. **Check Constraints**: Enforce specific value ranges or rules directly in SQL (e.g., `CHECK(status IN ('pending', 'completed'))` or `CHECK(amount >= 0)`).

## Step 3: Migration Workflow
All database schema changes must follow a strict, versioned migration protocol:
1. **Versioned Scripts**: Write migrations as sequential files (e.g., `0001_create_users.sql`, `0002_add_email_to_users.sql`) containing both `UP` (apply change) and `DOWN` (revert change) scripts.
2. **Idempotence**: Write migration scripts defensively so they do not error if run multiple times (e.g., use `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`).
3. **Zero-Downtime Design**: When modifying existing schemas (e.g., renaming columns, adding NOT NULL to existing columns), write multi-step migrations to avoid table locks or application downtime.

## Step 4: Indexing Strategies
Optimize database performance for high-volume queries:
1. **Primary & Foreign Keys**: Ensure all foreign key columns are indexed, as databases do not always index foreign keys automatically.
2. **Where & Join Clauses**: Add indexes (B-tree) on columns that are frequently used in `WHERE`, `JOIN`, or `ORDER BY` statements.
3. **Composite Indexes**: When queries filter by multiple columns, create a composite index. Order the columns in the index from most selective to least selective.
4. **Index Overhead**: Limit the number of indexes on tables with heavy write operations (`INSERT`/`UPDATE`/`DELETE`), as every index degrades write performance.

## Step 5: Verification (Definition of Done)
1. Run the database migrations against a test/development database and verify the schema matches the design.
2. Write unit/integration tests that interact with the database and assert:
   * Successful insertion of valid data.
   * Rejection of invalid data (e.g., verifying that violating `CHECK` or `UNIQUE` constraints throws a database error).
   * Successful execution and rollback of migration steps.
