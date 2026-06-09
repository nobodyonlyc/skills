# Technical Specification (SPEC) - Batch Import User CSV

> **Batch Name:** Batch Import User CSV
> **Batch Code:** IMP_USER_CSV
> **Version:** 1.0
> **Author:** Nguyen Van A
> **Creation Date:** 2026-06-01
> **Update Date:** 2026-06-01
> **Status:** Approved
> **Approver:** Tran Thi B (Tech Lead)

---

## 1. Purpose and Scope

### 1.1 Purpose

The Batch Import User CSV (`IMP_USER_CSV`) is designed to import user data from a CSV file into the database. The batch processes the CSV file, validates each record against business rules, inserts valid records into the `t_user` table in the database, and logs invalid records to an error log file.

### 1.2 Scope

- **In Scope:**
  - Reading the input CSV file.
  - Validating each record against business rules.
  - Inserting valid records into the database (`t_user` table).
  - Logging invalid records with line numbers and reasons.
  - Generating a summary report after execution.

- **Out of Scope:**
  - Updating existing records in the database.
  - Deleting records from the database.
  - Sending email notifications.
  - Handling file formats other than CSV.

### 1.3 Execution Frequency

- On-demand execution.
- Can be scheduled daily at 02:00 AM.

---

## 2. Input Specification

### 2.1 File Format

| Property | Value |
|---|---|
| Format | CSV (Comma-Separated Values) |
| Encoding | UTF-8 |
| Delimiter | Comma (`,`) |
| Has Header | Yes (the first row is the header) |
| Line Terminator | `\n` or `\r\n` |
| File Name Pattern | `users_import_YYYYMMDD.csv` |
| Input Directory | `/data/import/users/` |

### 2.2 Header Structure

```
id,name,email,age,role
```

### 2.3 Field Definitions

| # | Field | Data Type | Required | Constraints | Description |
|---|---|---|---|---|---|
| 1 | `id` | Integer | Yes | Positive integer, > 0, unique in file | User unique identifier |
| 2 | `name` | String | Yes | 1-100 characters. Only letters (including Unicode) and spaces are allowed. No special characters allowed. | User's full name |
| 3 | `email` | String | Yes | Must be in valid email format `xxx@xxx.xxx`. Must contain `@` and a dot `.` after `@`. | Email address |
| 4 | `age` | Integer | No | If provided: integer from 0 to 150. If blank: allowed, stored as NULL. | User's age |
| 5 | `role` | String | Yes | Must be one of: `admin`, `user`, `viewer` (case-sensitive). | User's role |

### 2.4 Valid CSV File Example

```csv
id,name,email,age,role
1,Nguyen Van A,nguyenvana@email.com,25,user
2,Tran Thi B,tranthib@email.com,30,admin
3,Le Van C,levanc@email.com,,viewer
```

---

## 3. Processing Logic

### 3.1 Main Processing Flow

```
Start
  │
  ├─ Step 1: Check if input file exists
  │   ├─ Does not exist → Log fatal error, exit (EXIT_CODE = 1)
  │   └─ Exists → Continue
  │
  ├─ Step 2: Check if file has data (not empty, has at least header + 1 data row)
  │   ├─ Empty or only header → Log warning, exit (EXIT_CODE = 2)
  │   └─ Has data → Continue
  │
  ├─ Step 3: Check record count limit
  │   ├─ > 100,000 records → Log error, exit (EXIT_CODE = 3)
  │   └─ ≤ 100,000 records → Continue
  │
  ├─ Step 4: Validate header
  │   ├─ Header format invalid → Log error, exit (EXIT_CODE = 4)
  │   └─ Header valid → Continue
  │
  ├─ Step 5: Process each record (from line 2 onwards)
  │   │
  │   ├─ 5.1: Parse CSV line into fields
  │   ├─ 5.2: Validate each field against rules (see Section 3.2)
  │   ├─ 5.3: Check for duplicate IDs within the file
  │   │
  │   ├─ If record is valid:
  │   │   ├─ Insert into t_user table
  │   │   └─ Increment success counter
  │   │
  │   └─ If record is invalid:
  │       ├─ Write to error log (line_number, field, error_message)
  │       └─ Increment error counter
  │
  ├─ Step 6: Generate summary report
  │   ├─ Total records read
  │   ├─ Successfully inserted records
  │   ├─ Error records count
  │   └─ Execution duration
  │
  └─ End (EXIT_CODE = 0)
```

### 3.2 Detailed Validation Rules

| # | Field | Rule | Validation Order | Error Code |
|---|---|---|---|---|
| 1 | `id` | Must not be null or empty | 1 | ERR_ID_REQUIRED |
| 2 | `id` | Must be an integer | 2 | ERR_ID_NOT_INTEGER |
| 3 | `id` | Must be > 0 | 3 | ERR_ID_NOT_POSITIVE |
| 4 | `id` | Must be unique within the file | 4 | ERR_ID_DUPLICATE |
| 5 | `name` | Must not be null or empty | 5 | ERR_NAME_REQUIRED |
| 6 | `name` | Length between 1 and 100 characters | 6 | ERR_NAME_LENGTH |
| 7 | `name` | Only contains letters (including Unicode) and spaces | 7 | ERR_NAME_INVALID_CHARS |
| 8 | `email` | Must not be null or empty | 8 | ERR_EMAIL_REQUIRED |
| 9 | `email` | Must be in valid format `xxx@xxx.xxx` | 9 | ERR_EMAIL_FORMAT |
| 10 | `age` | If provided, must be an integer | 10 | ERR_AGE_NOT_INTEGER |
| 11 | `age` | If provided, must be between 0 and 150 | 11 | ERR_AGE_RANGE |
| 12 | `role` | Must not be null or empty | 12 | ERR_ROLE_REQUIRED |
| 13 | `role` | Must be one of: admin, user, viewer (case-sensitive) | 13 | ERR_ROLE_INVALID |

### 3.3 Email Validation Rules

A valid email must satisfy the following conditions:
1. Contains exactly one `@` character.
2. The local part (before `@`) is not empty.
3. The domain part (after `@`) is not empty.
4. The domain part contains at least one dot `.`.
5. The top-level domain (after the last dot `.`) has at least one character.

Valid examples: `user@example.com`, `a@b.c`, `user.name@sub.domain.com`
Invalid examples: `userexample.com` (missing @), `user@` (missing domain), `user@example` (missing TLD)

---

## 4. Output Specification

### 4.1 Database - `t_user` Table

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| `id` | INT | NOT NULL | Primary Key, user identifier |
| `name` | VARCHAR(100) | NOT NULL | Full name |
| `email` | VARCHAR(255) | NOT NULL | Email address |
| `age` | INT | NULL | Age |
| `role` | VARCHAR(20) | NOT NULL | Role |
| `created_at` | TIMESTAMP | NOT NULL | Creation time (automatically set to insertion time) |
| `created_by` | VARCHAR(50) | NOT NULL | Creator user (defaults to 'BATCH_IMP_USER_CSV') |

### 4.2 Error Log File

| Property | Value |
|---|---|
| File Name Pattern | `error_IMP_USER_CSV_YYYYMMDD_HHMMSS.log` |
| Output Directory | `/data/import/users/logs/` |
| Encoding | UTF-8 |

**Error Log Line Format:**
```
[YYYY-MM-DD HH:MM:SS] [ERROR] Line {line_number}: Field [{field_name}] - {error_message} (Code: {error_code}) | Data: {raw_csv_line}
```

**Example:**
```
[2026-06-01 02:15:30] [ERROR] Line 5: Field [email] - Invalid email format (Code: ERR_EMAIL_FORMAT) | Data: 4,Pham Van D,phamvandemail.com,28,user
[2026-06-01 02:15:30] [ERROR] Line 8: Field [id] - ID must be a positive integer (Code: ERR_ID_NOT_POSITIVE) | Data: -1,Le Thi E,lethie@email.com,35,admin
```

### 4.3 Summary Report

After the batch completes, create a summary report file:

| Property | Value |
|---|---|
| File Name Pattern | `summary_IMP_USER_CSV_YYYYMMDD_HHMMSS.txt` |
| Output Directory | `/data/import/users/logs/` |

**Summary Report Content:**
```
=== BATCH IMPORT USER CSV - SUMMARY ===
Execution Date : {YYYY-MM-DD HH:MM:SS}
Input File     : {file_path}
Total Records  : {total_count}
Success        : {success_count}
Failed         : {failed_count}
Skipped        : {skipped_count}
Duration       : {duration_seconds}s
Exit Code      : {exit_code}
Error Log      : {error_log_path}
========================================
```

---

## 5. Error Handling

### 5.1 Batch-level Errors

| Error Code | Condition | Behavior | Exit Code |
|---|---|---|---|
| BATCH_ERR_001 | Input file does not exist | Log FATAL, terminate batch | 1 |
| BATCH_ERR_002 | File is empty or only contains header | Log WARNING, terminate batch | 2 |
| BATCH_ERR_003 | Record count exceeds 100,000 | Log ERROR, terminate batch without processing any records | 3 |
| BATCH_ERR_004 | Header format is invalid | Log ERROR, terminate batch | 4 |
| BATCH_ERR_005 | Cannot connect to database | Log FATAL, terminate batch | 5 |
| BATCH_ERR_006 | Error writing to error log file | Log WARNING, continue processing | 0 |

### 5.2 Record-level Errors

| Principle | Description |
|---|---|
| Process each record | Record errors do NOT affect other records |
| Log details | Each invalid record must log: line number, field name, error message, and error code |
| First error wins | Each record only logs the first error encountered (according to validation order) |
| Skip and continue | Invalid records are skipped, and the batch continues processing the next record |

### 5.3 Rollback

- **No automatic rollback supported:** If the batch is interrupted, successfully inserted records will remain in the database.
- **Manual Rollback:** Use the summary report to find the count of inserted records, then delete them based on `created_by` value.

---

## 6. Performance Requirements

| Requirement | Value | Notes |
|---|---|---|
| Max Record Count | 100,000 records | Exceeding will trigger rejection |
| Max Processing Duration | 30 minutes (for 100,000 records) | Approximately 55 records/second |
| Max Memory | 512 MB | Do not read the entire file into memory |
| Batch size (DB commit) | 1,000 records/commit | Commit every 1,000 records to avoid large transactions |

---

## 7. Constraints & Assumptions

### 7.1 Constraints

1. CSV file must be UTF-8 encoded.
2. CSV file must have header in the correct format.
3. Each data row must contain exactly 5 columns (corresponding to 4 commas).
4. The batch only supports INSERT; no UPDATE or UPSERT.
5. ID must be unique within the file, but is NOT checked against the database (the database will reject if duplicate PK exists).
6. Role values must be lowercase; values like `Admin`, `USER`, etc., are not accepted.

### 7.2 Assumptions

1. The database table `t_user` has been created with the schema described in Section 4.1.
2. The batch has permissions to read the CSV file and write to the error log.
3. The batch has INSERT permissions on the `t_user` table.
4. The error log directory already exists.
5. No other batches are running concurrently on the same CSV file.

---

## 8. Change History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 1.0 | 2026-06-01 | Nguyen Van A | Initial SPEC creation |
