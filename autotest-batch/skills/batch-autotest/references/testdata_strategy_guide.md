# Guide to Test Data Generation Strategy

> This document guides the agent on how to generate complete, correct, and comprehensive test data sets to achieve full coverage for all test cases.

---

## 1. Classification of Test Data

### 1.1 Normal/Valid Data

Data representing **standard processing paths** (happy path). Each valid equivalence class needs at least 1 corresponding dataset.

**Principles:**
- Complies with ALL constraints specified in the SPEC.
- Uses **representative** values — not boundary values, and not extreme edge values.
- Covers all valid partitions identified in Phase 1.

**Example:**

```json
{
  "testcase_id": "TC-001",
  "description": "Valid basic input - all required fields are valid",
  "category": "NORMAL",
  "input": {
    "customer_id": "CUST001",
    "name": "Nguyen Van A",
    "age": 30,
    "email": "nguyen.a@example.com",
    "order_amount": 500000,
    "order_date": "2024-06-15"
  },
  "expected_output": {
    "status": "SUCCESS",
    "process_status": "COMPLETED",
    "final_amount": 500000,
    "error_code": null,
    "error_message": null
  }
}
```

### 1.2 Boundary Data

Data targeting **boundary values** — where defects are typically concentrated.

**Principles:**
- Test EXACT boundary values (not approximations).
- Test both sides: min, min-1, min+1, max, max-1, max+1.
- Applies to both ranges (numeric values) and lengths (string character counts).

**Example: `age` field (0-150)**

```json
[
  {
    "testcase_id": "TC-010",
    "description": "Boundary - age = min (0)",
    "category": "BOUNDARY",
    "input": { "customer_id": "CUST010", "name": "Test User", "age": 0, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "SUCCESS", "process_status": "COMPLETED" }
  },
  {
    "testcase_id": "TC-011",
    "description": "Boundary - age = max (150)",
    "category": "BOUNDARY",
    "input": { "customer_id": "CUST011", "name": "Test User", "age": 150, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "SUCCESS", "process_status": "COMPLETED" }
  },
  {
    "testcase_id": "TC-012",
    "description": "Boundary - age = min - 1 (-1)",
    "category": "BOUNDARY",
    "input": { "customer_id": "CUST012", "name": "Test User", "age": -1, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "ERROR", "error_code": "E001", "error_message": "Age out of range" }
  },
  {
    "testcase_id": "TC-013",
    "description": "Boundary - age = max + 1 (151)",
    "category": "BOUNDARY",
    "input": { "customer_id": "CUST013", "name": "Test User", "age": 151, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "ERROR", "error_code": "E001", "error_message": "Age out of range" }
  }
]
```

### 1.3 Invalid Data

Data **violating constraints** — each test case violates **exactly one constraint** (isolation principle).

**Principles:**
- Each invalid test case modifies **only one field** to an invalid value.
- All other fields retain **valid values**.
- This ensures that if the test fails, you know precisely which field caused the failure.

**Example:**

```json
[
  {
    "testcase_id": "TC-040",
    "description": "Negative - customer_id is null (required field)",
    "category": "NEGATIVE",
    "input": { "customer_id": null, "name": "Test User", "age": 30, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "ERROR", "error_code": "VE-001", "error_message": "customer_id is required" }
  },
  {
    "testcase_id": "TC-041",
    "description": "Negative - name is empty string",
    "category": "NEGATIVE",
    "input": { "customer_id": "CUST041", "name": "", "age": 30, "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "ERROR", "error_code": "VE-001", "error_message": "name is required" }
  },
  {
    "testcase_id": "TC-042",
    "description": "Negative - age is string instead of integer",
    "category": "NEGATIVE",
    "input": { "customer_id": "CUST042", "name": "Test User", "age": "twenty", "order_amount": 100000, "order_date": "2024-01-01" },
    "expected_output": { "status": "ERROR", "error_code": "VE-003", "error_message": "Invalid type for age" }
  }
]
```

### 1.4 Edge Case Data

Data representing **unusual but valid** scenarios or **triggering unexpected system behavior**.

#### Unicode and Internationalization
- Japanese characters: `"田中太郎"`
- Arabic characters: `"محمد أحمد"`
- Emojis: `"John 🎉 Doe"`

#### Injection Attacks
- SQL injection: `"''; DROP TABLE users; --"`
- XSS payload: `"<script>alert('xss')</script>"`

#### Extreme Values
- Very long strings (10,000+ characters).
- Zero-width characters: `"CU\u200BST056"`.
- Negative zero values.

### 1.5 Volume Data

Testing the behavior of the batch process under **varying data volumes** to detect memory leaks, performance bottlenecks, and timeout issues.
- **Empty file**: 0 records (Verify if batch ends gracefully or rejects).
- **Single record**: 1 record (Verify if boundary logic handles 1 record correctly without array index issues).
- **Normal batch**: 100 - 1,000 records.
- **Large volume**: 10,000 - 100,000+ records (Simulate to test execution time limits, buffer size, DB bulk inserts, and transaction sizes).
- **Stress/Scale volume**: 1,000,000+ records (For performance verification).

### 1.6 Combination Data

Testing when **multiple fields are invalid simultaneously**.
- Used after evaluating each field in isolation.
- Verifies if the batch process reports all errors (error log aggregation) or only the first encountered error (fail-fast behavior).

### 1.7 Record State Anomalies

Batch processes must handle record-level structure and state anomalies robustly.
- **Duplicate Keys**: Input files containing records with identical unique keys (e.g., two records for the same transaction ID). Verify if system rejects duplicates, updates, or throws error.
- **Sort Order Violations**: If the SPEC requires input files to be pre-sorted (e.g., by account number or timestamp for control break processing), provide unsorted data to test order check validations.
- **Truncated / Malformed Records**: Files containing lines with missing delimiters, lines that end abruptly (truncated fixed-length rows), or lines that are too long.

### 1.8 Multi-step Consistency Data

For multi-step batch jobs (AJS/JP1 jobnets where output of Step A is input to Step B):
- Test data must be chained. The output file generated by Step A (which contains both successful records and rejected records) must be fed directly into Step B.
- Verify that Step B processes only the valid output of Step A and ignores/handles invalid data correctly.

### 1.9 Rerun & Recovery (Idempotency) Data

Verify batch behavior when a run fails midway and is restarted (rerun).
- **Pre-execution DB State**: Setup database with half-processed data (simulating a crash mid-run).
- **Idempotency verification**: Rerun the batch with the exact same input file. Verify that:
  - Already-processed records are NOT inserted/processed again (no double inserts).
  - Unprocessed records are completed successfully.
  - Financial balances and accumulators are NOT double-counted.

---

## 2. Rules for Generating Test Data

### 2.1 Core Principles

- **Respect SPEC constraints**: Valid data must satisfy all specified constraints.
- **Isolation principle**: Invalid data must violate exactly one constraint per test case.
- **Exact boundaries**: Boundary data must use precise bounds, not approximations.
- **Complete datasets**: Every test case must include both inputs and expected outputs.
- **Deterministic**: The same input must always produce the same expected output.
- **Independent**: Each test case must be executable independently of others.
- **Traceable**: Every dataset must map back to a TestCase ID.

### 2.2 Generation Checklist

For ALL required fields:
- [ ] Representative valid value.
- [ ] Null.
- [ ] Empty string (zero length).
- [ ] Whitespace-only string (spaces padding check).
- [ ] Mismatched data type (e.g., non-numeric in zoned decimal).
- [ ] Exact min boundary value.
- [ ] Exact max boundary value.
- [ ] Value below min (min - 1).
- [ ] Value above max (max + 1).

For ALL optional fields:
- [ ] Missing field.
- [ ] Null.
- [ ] Valid representative value.
- [ ] Invalid value (out of range/type).

For Batch-level Scenarios:
- [ ] Empty input file (0 records).
- [ ] Single record input file (1 record).
- [ ] Large volume input file (test buffers & chunk sizes).
- [ ] Duplicate key records in input file.
- [ ] Out-of-order records in input file (if sorting required).
- [ ] Truncated lines/records in input file.
- [ ] Pre-state database setup for Rerun/Recovery check.
- [ ] Mid-run crash DB setup (Idempotency verification).

---

## 3. Data Format

### 3.1 JSON Structure per TestCase

```json
{
  "testcase_id": "TC-NNN",
  "description": "Short description of the test case",
  "category": "NORMAL|BOUNDARY|NEGATIVE|EDGE|LOGIC|STATE",
  "priority": "CRITICAL|HIGH|MEDIUM|LOW",
  "requirement_refs": ["REQ-001", "REQ-003"],
  "input": {
    "field1": "value1",
    "field2": 123
  },
  "expected_output": {
    "status": "SUCCESS|ERROR",
    "process_status": "COMPLETED|FAILED|SKIPPED",
    "result": {},
    "error_code": null,
    "error_message": null
  }
}
```

---

## 4. Coverage Matrix

Every dataset must cover its designated TestCase ID. The coverage matrix tracks:
- [ ] Every designed TestCase has a corresponding dataset.
- [ ] Every data category (valid, boundary, invalid, edge, combination, volume) is represented.
- [ ] All datasets contain both input and expected outputs.
- [ ] Valid data matches constraints, and invalid data isolates a single constraint.
