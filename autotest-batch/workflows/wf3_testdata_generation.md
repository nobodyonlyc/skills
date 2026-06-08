# 📦 Phase 3: Test Data Generation

> **Workflow ID**: WF3  
> **Phase**: 3/5  
> **Previous**: [Phase 2 - TestCase Generation](./wf2_testcase_generation.md)  
> **Next**: [Phase 4 - Parallel Test Execution](./wf4_test_execution.md)

---

## 1. 🎯 Purpose

Generate **concrete test data** for **each test case** created in Phase 2, ensuring:
- ✅ **Data for Every TC** — No test case is left without corresponding test data.
- ✅ **Data Complies with SPEC** — Valid data adheres to constraints, while invalid data violates the expected constraint.
- ✅ **Isolation Principle** — Invalid data violates **EXACTLY ONE** constraint.
- ✅ **Reproducible** — Test data can be re-generated consistently at any time.
- ✅ **Execution Ready** — Saved in standard JSON format, ready for direct ingestion in Phase 4.
- 📦 **Mandatory Storage**: All generated test data must be saved as `3_testdata.json` in the centralized run directory (`test_runs/run_<timestamp>_<run_id>/`).
- 📐 **Format Schema**: The generated test data must strictly comply with the schema format defined in `skills/batch-autotest/templates/testdata_schema.json` (Method 4).

---

## 2. 📥 Input

| Input | Source | Description |
|---|---|---|
| TestCase suite | Phase 2 (WF2) | Complete test cases table with ID, Category, Input Summary, and Expected Output |
| Constraints table | Phase 1 (WF1) | Field constraints: min, max, format, valid values |
| Fields table | Phase 1 (WF1) | Fields specification: name, type, length, mandatory/optional status |
| Error conditions | Phase 1 (WF1) | List of error conditions and expected behaviors |

> ⚠️ **Verification**: Ensure Phase 2 has passed Gate 2 (100% requirement coverage).

---

## 3. 📋 Detailed Process

### Overview Table

| Step | Action | Input | Output | Data Category |
|---|---|---|---|---|
| 1 | Generate Valid Data for Normal TCs | Normal TCs + Constraints | JSON datasets | Valid |
| 2 | Generate Boundary Data | Boundary TCs + Constraints | JSON datasets | Valid + Invalid |
| 3 | Generate Invalid Data | Negative TCs + Error Conditions | JSON datasets | Invalid |
| 4 | Generate Edge Case Data | Edge TCs | JSON datasets | Edge |
| 5 | Generate Combination Data | Logic TCs | JSON datasets | Mixed |
| 6 | Generate Volume Data | State/Performance TCs | JSON datasets | Volume |
| 7 | Generate Mutated Input Files | Mutation TCs | Corrupted CSV/XML files | Structural mutations |
| 8 | Prepare Database Pre-state Scripts | DB CRUD & State TCs | SQL scripts / Mock DB data | DB State setups |
| 9 | Prepare System Interruption Triggers | Resilience TCs | Scripts or Mock triggers | Environment fault triggers |
| 10 | Programmatic Validation | JSON test data + SPEC Analysis | Exit code / log errors | Validation status |
| 11 | REVIEW GATE | All datasets | Checklist status (pass/fail) | — |

### 📌 Step 0: Sandbox Permission Authorization

Before generating any test data, the Orchestrator must call the `ask_permission` tool with:
- `Action`: `write_file`
- `Target`: The absolute path of the active workspace.
- `Reason`: "Xin quyền ghi file testdata động trong quá trình chạy test."

This ensures the sandbox environment is authorized upfront, enabling automated creation and writing of `3_testdata.json` under the `test_runs/` directory without permission prompt interruptions.

---

### 📌 Step 1: Generating Valid Data for Normal TCs

**Principles:**
- Value must lie **WITHIN** the corresponding valid partition.
- Value must satisfy **ALL** SPEC constraints simultaneously.
- Do NOT use boundary values (reserved for Step 2).
- Select **representative**, meaningful, and readable values.

**How to Implement:**
1. For each Normal TC, review the Input Summary from Phase 2.
2. Select concrete values for each field, lying near the MIDDLE of valid partitions.
3. Validate that all constraints are satisfied.
4. Define the expected output based on business rules.

**Example JSON:**

```json
{
  "testcase_id": "TC-001",
  "description": "Transfer small amount successfully - partition amount [1-1,000,000]",
  "category": "NORMAL",
  "input": {
    "transaction_id": "TXN20260605000001AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Chuyen khoan thanh toan",
    "priority": "N"
  },
  "expected_output": {
    "transaction_id": "TXN20260605000001AB",
    "status": "APPROVED",
    "fee": 10000,
    "error_code": null,
    "processed_date": "20260605"
  }
}
```

```json
{
  "testcase_id": "TC-002",
  "description": "Transfer medium amount successfully - partition amount [1M-100M]",
  "category": "NORMAL",
  "input": {
    "transaction_id": "TXN20260605000002CD",
    "source_account": "1234567890",
    "dest_account": "5555666677",
    "amount": 50000000,
    "bank_code": "TCB",
    "transaction_date": "20260605",
    "description": "Thanh toan hoa don",
    "priority": "N"
  },
  "expected_output": {
    "transaction_id": "TXN20260605000002CD",
    "status": "APPROVED",
    "fee": 25000,
    "error_code": null,
    "processed_date": "20260605"
  }
}
```

```json
{
  "testcase_id": "TC-003",
  "description": "Transfer large amount successfully - partition amount [100M-500M]",
  "category": "NORMAL",
  "input": {
    "transaction_id": "TXN20260605000003EF",
    "source_account": "1234567890",
    "dest_account": "1111222233",
    "amount": 300000000,
    "bank_code": "ACB",
    "transaction_date": "20260605",
    "description": "Chuyen tien mua nha",
    "priority": "H"
  },
  "expected_output": {
    "transaction_id": "TXN20260605000003EF",
    "status": "APPROVED",
    "fee": 50000,
    "error_code": null,
    "processed_date": "20260605"
  }
}
```

**Review Criteria:**
- [ ] Values are inside the valid partitions (not at boundaries).
- [ ] All mandatory fields are populated.
- [ ] All values comply with format and constraint rules.
- [ ] Expected output is calculated correctly based on business rules.
- [ ] transaction_id and account numbers follow valid formats.

---

### 📌 Step 2: Generating Boundary Data

**Principles:**
- Boundary values must be **EXACT** (no approximations).
- Include both **valid boundaries** (min, max) and **invalid boundaries** (min-1, max+1).
- For each boundary TC, ONLY the field under test has the boundary value; other fields must use standard valid values.

**How to Implement for NUMERIC fields:**

| Boundary | Value | Valid/Invalid | Example (amount range 1-500M) |
|---|---|---|---|
| min | Exact minimum value | ✅ Valid | amount = 1 |
| max | Exact maximum value | ✅ Valid | amount = 500,000,000 |
| min-1 | min minus 1 | ❌ Invalid | amount = 0 |
| max+1 | max plus 1 | ❌ Invalid | amount = 500,000,001 |

**Example JSON — Numeric Boundary:**

```json
{
  "testcase_id": "TC-010",
  "description": "BVA: amount = min (1) - Valid boundary",
  "category": "BOUNDARY",
  "input": {
    "transaction_id": "TXN20260605000010AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 1,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test boundary min",
    "priority": "N"
  },
  "expected_output": {
    "status": "APPROVED",
    "fee": 10000,
    "error_code": null
  }
}
```

```json
{
  "testcase_id": "TC-011",
  "description": "BVA: amount = max (500,000,000) - Valid boundary",
  "category": "BOUNDARY",
  "input": {
    "transaction_id": "TXN20260605000011AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test boundary max",
    "priority": "N"
  },
  "expected_output": {
    "status": "APPROVED",
    "fee": 50000,
    "error_code": null
  }
}
```

```json
{
  "testcase_id": "TC-012",
  "description": "BVA: amount = 0 (min-1) - Invalid boundary",
  "category": "BOUNDARY",
  "input": {
    "transaction_id": "TXN20260605000012AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 0,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test boundary min-1",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "fee": null,
    "error_code": "ERR-INVALID-AMT"
  }
}
```

```json
{
  "testcase_id": "TC-013",
  "description": "BVA: amount = 500,000,001 (max+1) - Invalid boundary",
  "category": "BOUNDARY",
  "input": {
    "transaction_id": "TXN20260605000013AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000001,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test boundary max+1",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "fee": null,
    "error_code": "ERR-OVER-LIMIT"
  }
}
```

**How to Implement for STRING LENGTH fields:**

| Boundary | Value | Valid/Invalid | Example (description length 0-140) |
|---|---|---|---|
| length = 0 | "" (empty) | ✅ Valid (if Optional) | description = "" |
| length = 1 | "A" | ✅ Valid | description = "A" |
| length = max-1 | "A" × (max-1) | ✅ Valid | description = "A" × 139 |
| length = max | "A" × max | ✅ Valid | description = "A" × 140 |
| length = max+1 | "A" × (max+1) | ❌ Invalid | description = "A" × 141 |

**Example JSON — String Length Boundary:**

```json
{
  "testcase_id": "TC-017",
  "description": "BVA: description = max length (140 chars) - Valid boundary",
  "category": "BOUNDARY",
  "input": {
    "transaction_id": "TXN20260605000017AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 100000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "priority": "N"
  },
  "expected_output": {
    "status": "APPROVED",
    "error_code": null
  },
  "metadata": {
    "description_length": 140,
    "boundary_type": "max",
    "field_under_test": "description"
  }
}
```

**Review Criteria:**
- [ ] Boundary values are EXACT (amount=1, not amount≈1).
- [ ] Only 1 field varies boundary values per test case; others remain standard.
- [ ] Valid boundaries yield APPROVED status.
- [ ] Invalid boundaries yield REJECTED status + appropriate error code.
- [ ] String length characters are counted precisely.

---

### 📌 Step 3: Generating Invalid Data

**CRITICAL Principle — Isolation Principle:**
> ⚠️ Each invalid dataset must violate **EXACTLY ONE** constraint. All other fields must be valid.
> Purpose: If the test case fails, we can isolate and identify which constraint verification failed.

**How to Implement:**
1. For each Negative TC from Phase 2, generate test data violating only the targeted constraint.
2. All other fields must use standard valid values.
3. Expected output must define a specific error code.

**Invalid Data Categories:**

| Category | Description | Example |
|---|---|---|
| null | Field is null or missing | `"amount": null` |
| empty | Field is empty string | `"bank_code": ""` |
| wrong type | Mismatched data types | `"amount": "abc"` |
| overflow | Extremely large values | `"amount": 9999999999999` |
| negative | Negative value for unsigned fields | `"amount": -50000` |
| invalid format | Violated format pattern | `"transaction_date": "2026/01/01"` |
| invalid value | Value not in whitelist | `"bank_code": "XYZ"` |

**Example JSON — null:**

```json
{
  "testcase_id": "TC-050",
  "description": "Negative: transaction_id = null (mandatory field missing)",
  "category": "NEGATIVE",
  "violated_constraint": "transaction_id is MANDATORY",
  "input": {
    "transaction_id": null,
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test null field",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-MISSING-TXID"
  }
}
```

**Example JSON — empty string:**

```json
{
  "testcase_id": "TC-051",
  "description": "Negative: source_account = empty string",
  "category": "NEGATIVE",
  "violated_constraint": "source_account is MANDATORY, min length = 10",
  "input": {
    "transaction_id": "TXN20260605000051AB",
    "source_account": "",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test empty field",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-MISSING-FIELD"
  }
}
```

**Example JSON — wrong type:**

```json
{
  "testcase_id": "TC-052",
  "description": "Negative: amount = text string instead of number",
  "category": "NEGATIVE",
  "violated_constraint": "amount must be NUMERIC (Decimal)",
  "input": {
    "transaction_id": "TXN20260605000052AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": "abc",
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test wrong type",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-INVALID-TYPE"
  }
}
```

**Example JSON — invalid format:**

```json
{
  "testcase_id": "TC-055",
  "description": "Negative: transaction_date wrong format (YYYY/MM/DD instead of YYYYMMDD)",
  "category": "NEGATIVE",
  "violated_constraint": "transaction_date format must be YYYYMMDD",
  "input": {
    "transaction_id": "TXN20260605000055AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "2026/06/05",
    "description": "Test invalid date format",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-INVALID-DATE"
  }
}
```

**Review Criteria:**
- [ ] Each invalid dataset violates EXACTLY ONE constraint.
- [ ] All other fields remain valid (isolation principle).
- [ ] `violated_constraint` clearly describes the violated rule.
- [ ] Expected output defines a specific error code.
- [ ] Covers: null, empty, wrong type, overflow, invalid format, invalid value.

---

### 📌 Step 4: Generating Edge Case Data

**Principles:**
- Target rare, unusual, but possible cases.
- Includes Unicode, special characters, injections, and extreme values.

**Edge Case Categories:**

| Category | Description | Example Value |
|---|---|---|
| Vietnamese diacritics | Accented Vietnamese text | `"Nguyễn Văn Á"` |
| Special characters | Special characters | `"!@#$%^&*()_+-=[]{}` |
| SQL injection | SQL injection payload | `"'; DROP TABLE customers;--"` |
| XSS | Cross-site scripting payload | `"<script>alert('xss')</script>"` |
| Very long string | Extremely long string | `"A" × 10000` |
| Zero-width chars | Invisible characters | `"\u200B\uFEFF"` |
| Newline/Tab | Control characters | `"line1\nline2\ttab"` |
| Unicode emoji | Emoji characters | `"💰 Payment 🏦"` |

**Example JSON:**

```json
{
  "testcase_id": "TC-070",
  "description": "Edge: description contains Vietnamese diacritics",
  "category": "EDGE",
  "input": {
    "transaction_id": "TXN20260605000070AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Money transfer for utility bill payment June 2026",
    "priority": "N"
  },
  "expected_output": {
    "status": "APPROVED",
    "error_code": null
  }
}
```

```json
{
  "testcase_id": "TC-071",
  "description": "Edge: description contains SQL injection",
  "category": "EDGE",
  "input": {
    "transaction_id": "TXN20260605000071AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "'; DROP TABLE transactions;--",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-INVALID-CHAR"
  }
}
```

```json
{
  "testcase_id": "TC-072",
  "description": "Edge: description contains XSS payload",
  "category": "EDGE",
  "input": {
    "transaction_id": "TXN20260605000072AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "<script>alert('xss')</script>",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-INVALID-CHAR"
  }
}
```

```json
{
  "testcase_id": "TC-073",
  "description": "Edge: description contains zero-width characters",
  "category": "EDGE",
  "input": {
    "transaction_id": "TXN20260605000073AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": 500000,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Normal\u200Btext\uFEFFhere",
    "priority": "N"
  },
  "expected_output": {
    "status": "APPROVED_OR_REJECTED",
    "note": "Depends on SPEC - needs verification of zero-width chars handling"
  }
}
```

**Review Criteria:**
- [ ] Covers: Vietnamese diacritics, SQL injection, XSS, and long string.
- [ ] Expected output is logical for each edge case.
- [ ] Notes indicate where behavior depends on technical implementation details.

---

### 📌 Step 5: Generating Combination Data

**Principles:**
- Test scenarios where **MULTIPLE fields are invalid simultaneously**.
- Purpose: Verify that the system handles multiple errors gracefully.
- Distinguishes from Step 3 (isolation): intentionally violates multiple constraints.

**Example JSON:**

```json
{
  "testcase_id": "TC-080",
  "description": "Combination: amount invalid + bank_code invalid simultaneously",
  "category": "NEGATIVE",
  "violated_constraints": [
    "amount < min (0)",
    "bank_code not in valid list"
  ],
  "input": {
    "transaction_id": "TXN20260605000080AB",
    "source_account": "1234567890",
    "dest_account": "9876543210",
    "amount": -100,
    "bank_code": "INVALID",
    "transaction_date": "20260605",
    "description": "Test multiple errors",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-INVALID-AMT",
    "note": "System should return the first encountered error (or all errors)"
  }
}
```

```json
{
  "testcase_id": "TC-081",
  "description": "Combination: null transaction_id + null source_account + amount = 0",
  "category": "NEGATIVE",
  "violated_constraints": [
    "transaction_id is MANDATORY",
    "source_account is MANDATORY",
    "amount < min"
  ],
  "input": {
    "transaction_id": null,
    "source_account": null,
    "dest_account": "9876543210",
    "amount": 0,
    "bank_code": "VCB",
    "transaction_date": "20260605",
    "description": "Test all critical fields invalid",
    "priority": "N"
  },
  "expected_output": {
    "status": "REJECTED",
    "error_code": "ERR-MISSING-TXID",
    "note": "System should report mandatory field error first"
  }
}
```

**Review Criteria:**
- [ ] At least 3-5 combination datasets are created.
- [ ] Each dataset violates ≥ 2 constraints.
- [ ] Expected output defines priority error code or aggregates all errors.
- [ ] Notes describe the expected system behavior under multiple failures.

---

### 📌 Step 6: Generating Volume Data

**Principles:**
- Test the system with varying dataset sizes.
- For batch processing, test with input files containing different record counts.

**Volume Scenarios:**

| Scenario | Record Count | Objective |
|---|---|---|
| Empty | 0 records | Process empty file |
| Single | 1 record | Process single record |
| Small batch | 10 records | Small normal batch |
| Normal batch | 100 records | Standard batch |
| Large batch | 10,000+ records | Performance, memory limits |

**Example JSON — Volume structure:**

```json
{
  "testcase_id": "TC-090",
  "description": "Volume: Empty file - 0 records",
  "category": "EDGE",
  "input": {
    "records": [],
    "record_count": 0
  },
  "expected_output": {
    "status": "COMPLETED",
    "total_processed": 0,
    "total_approved": 0,
    "total_rejected": 0,
    "note": "System handles empty file gracefully without crashing"
  }
}
```

```json
{
  "testcase_id": "TC-091",
  "description": "Volume: Single record",
  "category": "EDGE",
  "input": {
    "records": [
      {
        "transaction_id": "TXN20260605000091AB",
        "source_account": "1234567890",
        "dest_account": "9876543210",
        "amount": 500000,
        "bank_code": "VCB",
        "transaction_date": "20260605",
        "description": "Single record test",
        "priority": "N"
      }
    ],
    "record_count": 1
  },
  "expected_output": {
    "status": "COMPLETED",
    "total_processed": 1,
    "total_approved": 1,
    "total_rejected": 0
  }
}
```

```json
{
  "testcase_id": "TC-092",
  "description": "Volume: Mixed batch - 10 records (7 valid + 3 invalid)",
  "category": "EDGE",
  "input": {
    "record_count": 10,
    "valid_records": 7,
    "invalid_records": 3,
    "generation_rule": "Generate 7 records with valid data + 3 records with various errors"
  },
  "expected_output": {
    "status": "COMPLETED",
    "total_processed": 10,
    "total_approved": 7,
    "total_rejected": 3
  }
}
```

**Review Criteria:**
- [ ] Covers: empty (0), single (1), and normal volume batch.
- [ ] Large volume (if applicable).
- [ ] Expected output defines batch summary statistics (total processed, approved, rejected).
- [ ] Empty file is processed gracefully.

---

### 📌 Step 7: Generating Mutated Input Files

**Detailed Description:**
1. Generate test data files that violate the structural format constraints of the batch parser.
2. Formats include:
   - CSV with extra or missing delimiters.
   - Fixed-length files with misaligned column widths.
   - XML/JSON with invalid syntax or tags.
   - Text files encoded in non-supported charsets (e.g. Shift-JIS instead of UTF-8).
3. Save these files in the input folder of the corresponding TestCase.

**Review Criteria:**
- [ ] Mutated files are saved in the correct run directory folder (e.g. `TC-070/input/`).
- [ ] Mutated files contain the exact formatting anomaly specified in Phase 2.

---

### 📌 Step 8: Preparing Database Pre-state Scripts

**Detailed Description:**
1. For database CRUD and state transition test cases, write SQL or mock setup scripts to initialize the database state prior to execution.
2. Scripts must prepare:
   - Account records with initial balances (e.g. $100M$).
   - Master parameters whitelist records (e.g. linked bank codes).
   - Duplicate records check environment (pre-insert a record today).
3. Save these scripts alongside the test case resources.

**Review Criteria:**
- [ ] Initial DB states are documented.
- [ ] Pre-state scripts can be run cleanly without affecting other tests.

---

### 📌 Step 9: Preparing System Interruption Triggers

**Detailed Description:**
1. For resilience and fault tolerance test cases, write shell scripts or mock triggers to execute systems commands during Phase 4.
2. Triggers include:
   - Simulating network drop: e.g. blocking database port (`pfctl` / `iptables`).
   - Simulating disk space exhaustion: e.g. filling the temp disk volume.
   - Process force kill: e.g. issuing `kill -9` to the batch PID.
3. Save these trigger scripts under the testcase resources.

**Review Criteria:**
- [ ] Trigger mechanisms are safe and run-time isolated.
- [ ] Recovery verification methods (post-run rollback check) are defined.

---

### 📌 Step 10: Programmatic Validation

**Detailed Description:**
Before entering the Review Gate, the Agent must programmatically validate the generated test data JSON file to verify structural schema alignment (Method 4) and constraint compliance / isolation rule compliance (Method 1).

1. **Required tools**: The validator python script at `workflows/scripts/validate_testdata.py` and the batch validation configuration file (e.g. `skills/batch-autotest/templates/settlement_validation_config.json`).
2. **Action**: Run the command:
   ```bash
   python workflows/scripts/validate_testdata.py --config skills/batch-autotest/templates/settlement_validation_config.json --testdata {run_dir}/3_testdata.json --spec 1_spec_analysis.md
   ```
3. **If Validation Fails**:
   - Parse the printed validation errors (e.g. invalid type, out of range, isolation rule violation where multiple fields are invalid in a negative test case).
   - Locate the failing test case in `{run_dir}/3_testdata.json`.
   - Correct the invalid field values in `{run_dir}/3_testdata.json` to satisfy constraint checks or isolate the negative test.
   - Re-run the validation command. Repeat until the command returns success (exit code 0).
4. **Verification Criteria**:
   - [ ] Validation command completes successfully with exit code 0.
   - [ ] No constraint validation errors remain in the log output.

---

### 📌 Step 11: REVIEW GATE

**Detailed Description:**
This is the final quality check before proceeding to Phase 4 (Test Execution). The process includes performing a brainstorming quality analysis of the generated test data, printing the summary report directly in the agent chat (DO NOT create a separate phase report file on disk), and obtaining user approval.

1. **Agent Brainstorming**:
   - Assess test data quality: do the data sets adhere to the isolation principle for invalid tests?
   - Are boundary values (min, max, min-1, max+1) defined precisely according to technical specifications?
   - Are edge cases (injections, Unicode) populated with realistic and safe data?
   - Self-check against the checklist below.
2. **Print Phase Summary**:
   - Print a summary of Phase 3 results (Test data files created, TCs covered, JSON verification status) directly in the agent chat conversation.
3. **Present Options via ask_question**:
   - The Agent calls the `ask_question` tool in the detected language to ask:
     - **Question**: "Is the TestData generation (Phase 3) output satisfactory?"
     - **Options**:
       - "(Recommended) Everything is fine, proceed to Phase 4 (Test Execution)."
       - "There are issues, I want to adjust or provide feedback."
4. **Wait for Response**: The pipeline blocks until the user responds to the `ask_question` modal.

**Review Gate 3 Checklist:**

```
REVIEW GATE 3 - CHECKLIST
==========================

□ 1. Completeness
  □ Each TC from Phase 2 has at least 1 corresponding test dataset.
  □ No TCs lack data.
  □ Coverage matrix shows 100% of TCs have data.

□ 2. Valid Data Quality
  □ All valid data complies with SPEC constraints.
  □ Valid data does NOT use boundary values (except for Boundary TCs).
  □ Expected outputs are calculated correctly based on business rules.
  □ All mandatory fields are populated.

□ 3. Invalid Data Quality
  □ Each invalid dataset violates EXACTLY ONE constraint (isolation principle).
  □ Fields not under test remain valid.
  □ violated_constraint clearly logs the targeted rule.
  □ Expected output specifies a concrete error code.

□ 4. Boundary Data Quality
  □ Boundary values are EXACT (no approximations).
  □ String length characters are counted correctly.
  □ min, max, min-1, max+1 values are present.

□ 5. Edge Case Data
  □ Covers Unicode, injection, and special characters.
  □ Expected output is logical.

□ 6. Format
  □ All data is structured in standard JSON.
  □ Contains: testcase_id, description, input, expected_output.
  □ JSON is valid and parseable.
  □ User approval has been obtained for the Test Data.
```

**Decision:**
- **Approved by user (Option 1 selected in ask_question)** -> Transition to Phase 4.
- **Adjustments requested (Option 2 selected in ask_question)** -> Ask the user for feedback in chat, update Phase 3 based on feedback, and repeat Review Gate 3.

---

## 4. 📄 Data Format

### Standard JSON Structure

```json
{
  "testcase_id": "TC-NNN",
  "description": "Brief description of the test data",
  "category": "NORMAL|BOUNDARY|LOGIC|STATE|NEGATIVE|EDGE",
  "violated_constraint": "Name of the violated constraint (for invalid data only)",
  "input": {
    "field_1": "value_1",
    "field_2": "value_2"
  },
  "expected_output": {
    "status": "APPROVED|REJECTED|ERROR",
    "error_code": "ERR-xxx (if REJECTED)",
    "field_result_1": "expected_value"
  },
  "metadata": {
    "boundary_type": "min|max|min-1|max+1 (if boundary)",
    "field_under_test": "field being tested (if boundary/negative)",
    "note": "Additional notes"
  }
}
```

### Complete Dataset Collection

```json
{
  "spec_name": "Interbank Transfer Transaction Processing Batch",
  "generated_date": "2026-06-05",
  "total_testcases": 50,
  "data_sets": [
    { "testcase_id": "TC-001", ... },
    { "testcase_id": "TC-002", ... },
    ...
  ]
}
```

---

## 5. 📊 Coverage Matrix

After generating the test data, formulate the coverage matrix:

| Category | TC Count | Has Data | Lacks Data | Coverage |
|---|---|---|---|---|
| NORMAL | 5 | 5 | 0 | 100% ✅ |
| BOUNDARY | 12 | 12 | 0 | 100% ✅ |
| LOGIC | 8 | 8 | 0 | 100% ✅ |
| STATE | 7 | 7 | 0 | 100% ✅ |
| NEGATIVE | 10 | 10 | 0 | 100% ✅ |
| EDGE | 8 | 8 | 0 | 100% ✅ |
| **TOTAL** | **50** | **50** | **0** | **100%** ✅ |

> ⛔ Coverage MUST reach **100%** before proceeding to Phase 4.

---

## 6. 📏 Rules

### 🔴 Mandatory

| # | Rule | Description |
|---|---|---|
| R1 | Valid data MUST comply with SPEC constraints | Valid data must comply with ALL constraints. |
| R2 | Invalid data MUST violate exactly ONE constraint | Isolation principle — violate exactly one constraint. |
| R3 | Boundary values MUST be exact | Boundary values must be exact, not approximations. |
| R4 | All data must be reproducible | The data must be reproducible consistently. |
| R5 | JSON must be valid | JSON must be parseable without syntax errors. |

### 🟡 Recommended

| # | Rule | Description |
|---|---|---|
| R6 | Use meaningful values | Use realistic values (real names, proper account numbers). |
| R7 | Add metadata for special TCs | Include metadata for boundary/negative TCs. |
| R8 | Document assumptions | State assumptions when the SPEC is ambiguous. |

---

## 7. 🚪 Gate Condition

### MANDATORY conditions to transition to Phase 4:

| # | Condition | Level |
|---|---|---|
| 1 | Each TC has at least 1 test dataset | 🔴 Mandatory |
| 2 | Coverage matrix = 100% | 🔴 Mandatory |
| 3 | Valid data complies with constraints | 🔴 Mandatory |
| 4 | Invalid data violates exactly 1 constraint (isolation) | 🔴 Mandatory |
| 5 | Boundary values are exact | 🔴 Mandatory |
| 6 | JSON format is valid | 🔴 Mandatory |
| 7 | User approval (Option 1 in ask_question) is received | 🔴 Mandatory |
| 8 | File `3_testdata.json` is created and saved in the centralized run directory | 🔴 Mandatory |
| 9 | Edge cases (Unicode, injection) are covered | 🟡 Recommended |

> ⛔ **If any MANDATORY condition is not met or user approval is missing, DO NOT proceed to Phase 4.**

---

## 8. 💡 Tips and Common Mistakes

### ✅ Best Practices

1. **Generate data sequentially**: Normal → Boundary → Invalid → Edge → Combination → Volume.
2. **Cross-check with SPEC**: After generation, verify the expected outputs against business rules.
3. **Write clear descriptions**: The description should state what the dataset is testing.
4. **Utilize metadata**: Add `boundary_type` and `violated_constraint` to ease debugging.
5. **Test JSON validity**: Parse the JSON file before passing it to Phase 4.

### ❌ Common Mistakes

| # | Mistake | Consequence | How to Avoid |
|---|---|---|---|
| 1 | Valid data violates constraints | False negative (TC fails due to invalid data) | Double-check every field |
| 2 | Invalid data violates >1 constraint | Cannot identify which constraint violation caused rejection | Enforce the isolation principle |
| 3 | Boundary value off by 1 unit | Missed boundary defects | Calculate ranges carefully |
| 4 | Miscalculated expected output | Mismatched results → incorrect test outcomes | Verify with SPEC and calculators |
| 5 | JSON syntax error | Phase 4 cannot parse the data | Validate JSON beforehand |
| 6 | Incorrect string length counting | Inaccurate boundary tests | Measure character counts precisely |
| 7 | Neglecting mandatory fields | Incomplete datasets | Maintain a checklist of mandatory fields |

---

## 8.5 ⚠️ Critical Rules

1. **Testing Source Code Only (No code changes during test)**:
   - Execute testing on the existing application code as-is. Absolutely no modifications to the production code are permitted.
   - If a bug is found in the application, do not change the testcase or expected output to hide the issue. Record the bug details transparently in the final report without attempting to fix the source code.
2. **Centralized Output Storage**:
   - Write all generated test data sets to `3_testdata.json` and save it inside the centralized run directory: `test_runs/run_<timestamp>_<run_id>/`.
3. **Language Alignment Rule**:
   - Inspect the input SPEC/prompt to determine the execution language.
   - All generated output files, log outputs (including execution status logs shown to the user), internal reasoning/thinking blocks, and all chat communications must be written in the **exact same language** as detected (e.g., if the user prompts in Japanese, your thoughts, logs, and answers must be entirely in Japanese without mixing English or Vietnamese).

---

## 9. 📚 References

- **Previous Phase**: [WF2 - TestCase Generation](./wf2_testcase_generation.md)
- **Next Phase**: [WF4 - Parallel Test Execution](./wf4_test_execution.md)
- **Pipeline Overview**: [README](./README.md)
- **Full Pipeline**: [WF Full Pipeline](./wf_full_pipeline.md)

---

> 📌 **Reminder**: Test data is the "fuel" of the testing process. Invalid data = meaningless test outcomes. Take extra care with valid data (must satisfy constraints) and boundary values (must be exact).
