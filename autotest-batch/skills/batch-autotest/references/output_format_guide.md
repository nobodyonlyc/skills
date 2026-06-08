# Guide to Output Format

> This document defines the standard output formats for each phase in the batch autotest process.
> The Agent MUST adhere to these formats to ensure consistency and facilitate report aggregation.

---

## Phase 1 Output: SPEC Analysis Result

### Template

```markdown
# SPEC Analysis Result

**Batch Name**: [Batch Name]
**SPEC Version**: [Version]
**Analyzed Date**: [YYYY-MM-DD HH:mm:ss]
**Analyst**: [Agent ID]

---

## 1. Overview

Brief functional description of the batch process, inputs, and outputs.

---

## 2. Business Rules

| Rule ID | Description | Condition | Expected Action | Type |
|---|---|---|---|---|
| BR-001 | Validate age range | `age < 0 OR age > 150` | Reject record, error: E001 | Validation |
| BR-002 | Calculate VIP discount | `customer_type == "VIP" AND total > 1M` | Apply 10% discount | Calculation |
| BR-003 | Handle duplicates | `customer_id` duplicates | Keep the first record, skip subsequent ones | Transformation |

**Total Business Rules**: N

---

## 3. Input Fields

| # | Field Name | Data Type | Required | Constraints | Default | Description |
|---|---|---|---|---|---|---|
| 1 | customer_id | string | Yes | max 20 chars, pattern: `^[A-Z0-9]+$` | — | Customer identifier |
| 2 | name | string | Yes | max 100 chars | — | Customer name |
| 3 | age | integer | Yes | min: 0, max: 150 | — | Customer age |
| 4 | email | string | No | max 254 chars, RFC 5322 | null | Customer email |
| 5 | order_amount | decimal | Yes | min: 0, max: 999999999.99 | — | Order amount |
| 6 | order_date | date | Yes | format: YYYY-MM-DD, ≤ today | — | Order date |

**Total Input Fields**: N (required: M, optional: K)

---

## 4. Output Fields

| # | Field Name | Data Type | Description |
|---|---|---|---|
| 1 | process_status | string | Processing status: `SUCCESS`, `FAILED`, `SKIPPED` |
| 2 | final_amount | decimal | Final amount after discount |
| 3 | error_code | string | Error code (null if SUCCESS) |
| 4 | error_message | string | Detailed error message |

**Total Output Fields**: N

---

## 5. Constraints & Boundaries

| Field | Min Value | Max Value | Min Length | Max Length | Format/Pattern | Allowed Values | Other Constraints |
|---|---|---|---|---|---|---|---|
| customer_id | — | — | 1 | 20 | `^[A-Z0-9]+$` | — | Unique, Not null |
| age | 0 | 150 | — | — | Integer | — | Not null |
| order_amount | 0 | 999999999.99 | — | — | Decimal(11,2) | — | Not null |
| order_date | — | today | — | — | YYYY-MM-DD | — | Not null |
| status | — | — | — | — | — | A, I, D | Not null |

---

## 6. Equivalence Partitions

| Field | Partition ID | Type | Description | Representative Value | Expected Result |
|---|---|---|---|---|---|
| age | EP-AGE-V1 | Valid | Valid age (1-149) | 30 | SUCCESS |
| age | EP-AGE-V2 | Valid | Age = 0 | 0 | SUCCESS |
| age | EP-AGE-V3 | Valid | Age = 150 | 150 | SUCCESS |
| age | EP-AGE-I1 | Invalid | Negative age | -5 | ERROR |
| age | EP-AGE-I2 | Invalid | Age > 150 | 200 | ERROR |
| age | EP-AGE-I3 | Invalid | Non-numeric | "abc" | ERROR |
| age | EP-AGE-I4 | Invalid | Null value | null | ERROR |

---

## 7. Error Conditions

| Error ID | Type | Condition | Expected Behavior | SPEC Reference |
|---|---|---|---|---|
| VE-001 | Validation | Required field is null/empty | Reject record | Section 3.1 |
| VE-002 | Validation | Field exceeds max length | Reject record | Section 3.2 |
| VE-003 | Validation | Invalid format | Reject record | Section 3.3 |
| VE-004 | Validation | Value out of range | Reject record | Section 3.4 |
| BE-001 | Business | Duplicate customer_id | Skip, log warning | Section 4.1 |
| BE-002 | Business | Referenced entity not found | Reject, log error | Section 4.2 |
| SE-001 | System | Input file not found | Abort batch | Section 5.1 |
| SE-002 | System | Input file empty | Complete, 0 records | Section 5.2 |
| DF-001 | Format | Invalid file format | Abort batch | Section 6.1 |

**Total Error Conditions**: N (Validation: A, Business: B, System: C, Format: D)

---

## 8. Traceability Table

| SPEC Requirement | Ref Section | Extracted Items | Coverage |
|---|---|---|---|
| REQ-001 | Section 3 | BR-001, EP-AGE-V1~I4, VE-004 | ✅ Covered |
| REQ-002 | Section 4 | BR-002, EP-DISC-V1 | ✅ Covered |
| REQ-003 | Section 5 | BR-003, BE-001 | ✅ Covered |

**Coverage**: N/N requirements covered (100%)
```

---

## Phase 2 Output: TestCase Suite

### Template

```markdown
# TestCase Suite

**Batch Name**: [Batch Name]
**Generated Date**: [YYYY-MM-DD HH:mm:ss]
**Based on SPEC Analysis**: [Reference to Phase 1 output]
**Total TestCases**: N

---

## 1. Summary

| Category | Count | Percentage |
|---|---|---|
| NORMAL | 5 | 13% |
| BOUNDARY | 12 | 32% |
| LOGIC | 8 | 21% |
| STATE | 4 | 11% |
| NEGATIVE | 6 | 16% |
| EDGE | 3 | 8% |
| **Total** | **38** | **100%** |

| Priority | Count | Percentage |
|---|---|---|
| CRITICAL | 8 | 21% |
| HIGH | 15 | 39% |
| MEDIUM | 10 | 26% |
| LOW | 5 | 13% |
| **Total** | **38** | **100%** |

---

## 2. TestCases

| ID | Name | Category | Priority | Description | Precondition | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-001 | NORMAL_valid_basic_input | NORMAL | CRITICAL | Input valid with all required fields | Batch ready, DB connected | All required fields valid | SUCCESS, record processed |
| TC-002 | NORMAL_valid_with_optional | NORMAL | HIGH | Input valid including optional fields | Batch ready, DB connected | All fields valid incl. optional | SUCCESS, record processed |
| TC-010 | BOUNDARY_age_min_0 | BOUNDARY | HIGH | Age = 0 (lower bound) | Batch ready | age = 0 | SUCCESS |
| TC-011 | BOUNDARY_age_max_150 | BOUNDARY | HIGH | Age = 150 (upper bound) | Batch ready | age = 150 | SUCCESS |
| TC-012 | BOUNDARY_age_below_min | BOUNDARY | HIGH | Age = -1 (below bound) | Batch ready | age = -1 | ERROR: VE-004 |
| TC-020 | LOGIC_vip_discount | LOGIC | CRITICAL | VIP discount 10% | VIP customer exists | VIP + order > 1M | final_amount = 90% |
| TC-030 | STATE_new_to_validated | STATE | HIGH | Record NEW → VALIDATED | Record in NEW state | Valid data | Status = VALIDATED |
| TC-040 | NEGATIVE_null_customer_id | NEGATIVE | HIGH | customer_id = null | Batch ready | customer_id = null | ERROR: VE-001 |
| TC-050 | EDGE_unicode_name | EDGE | LOW | Name contains Unicode characters | Batch ready | name = "田中太郎" | SUCCESS |

---

## 3. TestCase Detail Example

### TC-001: NORMAL_valid_basic_input

| Attribute | Value |
|---|---|
| **ID** | TC-001 |
| **Name** | NORMAL_valid_basic_input |
| **Category** | NORMAL |
| **Priority** | CRITICAL |
| **Description** | Check if batch processes correctly with valid input containing all required fields |
| **Precondition** | Batch ready, database connected, input file exists |
| **Input** | `{"customer_id": "CUST001", "name": "Nguyen Van A", "age": 30, "order_amount": 500000, "order_date": "2024-06-15"}` |
| **Expected Output** | `{"status": "SUCCESS", "process_status": "COMPLETED", "final_amount": 500000}` |
| **Requirement Refs** | REQ-001, REQ-002 |
| **Notes** | Happy path — must PASS; if FAIL, critical bug |

---

## 4. Traceability Matrix

| Requirement ID | Description | TestCase IDs | Coverage Status |
|---|---|---|---|
| REQ-001 | Validate customer_id | TC-001, TC-010, TC-040 | ✅ Full |
| REQ-002 | Validate age range | TC-010, TC-011, TC-012, TC-013 | ✅ Full |
| REQ-003 | VIP discount | TC-020, TC-022 | ✅ Full |
| REQ-004 | Handle duplicates | TC-025 | ✅ Full |
| REQ-005 | File error handling | TC-045, TC-046 | ✅ Full |

**Coverage Summary**: N/N requirements covered (100%)
```

---

## Phase 3 Output: Test Data Sets

### Template

Each testcase group creates a JSON file:

```json
{
  "metadata": {
    "batch_name": "BatchXYZ",
    "generated_at": "2024-06-15T10:30:00Z",
    "spec_version": "1.0",
    "total_testcases": 38,
    "categories": {
      "NORMAL": 5,
      "BOUNDARY": 12,
      "NEGATIVE": 8,
      "EDGE": 6,
      "LOGIC": 4,
      "STATE": 3
    }
  },
  "testcases": [
    {
      "testcase_id": "TC-001",
      "description": "Valid basic input - all required fields",
      "category": "NORMAL",
      "priority": "CRITICAL",
      "requirement_refs": ["REQ-001", "REQ-002"],
      "input": {
        "customer_id": "CUST001",
        "name": "Nguyen Van A",
        "age": 30,
        "email": null,
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
  ]
}
```

---

## Phase 4 Output: Execution Results

### SubAgent Output Format

Each subagent returns results in a Markdown table:

```markdown
# Execution Results — SubAgent [N]

**Executed**: [YYYY-MM-DD HH:mm:ss]
**TestCases**: [From TC-XXX to TC-YYY]
**Total**: N | **Passed**: P | **Failed**: F | **Skipped**: S

## Results

| ID | Name | Status | Input | Expected | Actual | Error |
|---|---|---|---|---|---|---|
| TC-001 | NORMAL_valid_basic_input | ✅ PASS | `{"customer_id":"CUST001","name":"Nguyen Van A","age":30}` | `{"status":"SUCCESS","final_amount":500000}` | `{"status":"SUCCESS","final_amount":500000}` | — |
| TC-012 | BOUNDARY_age_below_min | ✅ PASS | `{"customer_id":"CUST012","age":-1}` | `{"status":"ERROR","error_code":"VE-004"}` | `{"status":"ERROR","error_code":"VE-004"}` | — |
| TC-020 | LOGIC_vip_discount | ❌ FAIL | `{"customer_id":"VIP001","type":"VIP","amount":2000000}` | `{"discount":10,"final":1800000}` | `{"discount":5,"final":1900000}` | Discount calculated as 5% instead of 10% for VIP |
| TC-045 | NEGATIVE_file_not_found | ⏭️ SKIP | N/A | Abort batch | — | Cannot simulate: no file system access in test env |
```

---

## Phase 5 Output: Final Report

### Template

```markdown
# Test Report

**Batch Name**: [Batch Name]
**SPEC Version**: [Version]
**Report Date**: [YYYY-MM-DD HH:mm:ss]
**Environment**: [Test/Staging/Production]

---

## 1. Executive Summary

| Metric | Value |
|---|---|
| Total TestCases | 38 |
| ✅ Passed | 33 |
| ❌ Failed | 3 |
| ⏭️ Skipped | 2 |
| **Pass Rate** | **86.8%** |
| **Pass Rate (excl. skipped)** | **91.7%** |

### Conclusion
[Summary of results: whether the batch meets requirements, critical issues if any]

---

## 2. Results by Category

| Category | Total | Passed | Failed | Skipped | Pass Rate |
|---|---|---|---|---|---|
| NORMAL | 5 | 5 | 0 | 0 | 100% |
| BOUNDARY | 12 | 11 | 1 | 0 | 91.7% |
| LOGIC | 8 | 6 | 2 | 0 | 75.0% |

---

## 3. Results by Priority

| Priority | Total | Passed | Failed | Skipped | Pass Rate |
|---|---|---|---|---|---|
| CRITICAL | 8 | 7 | 1 | 0 | 87.5% |
| HIGH | 15 | 14 | 1 | 0 | 93.3% |

---

## 4. Detailed Results

| ID | Name | Status | Input | Expected | Actual | Error |
|---|---|---|---|---|---|---|
| TC-001 | NORMAL_valid_basic_input | ✅ PASS | `{...}` | `{...}` | `{...}` | — |
| TC-020 | LOGIC_vip_discount | ❌ FAIL | `{...}` | `{...}` | `{...}` | Discount 5% instead of 10% |

---

## 5. Failed TestCases Analysis

### TC-020: LOGIC_vip_discount — ❌ FAIL

| Attribute | Value |
|---|---|
| **Category** | LOGIC |
| **Priority** | CRITICAL |
| **SPEC Reference** | REQ-003, BR-002 |
| **Input** | `{"customer_id":"VIP001","type":"VIP","amount":2000000}` |
| **Expected** | Discount 10%, final_amount = 1,800,000 |
| **Actual** | Discount 5%, final_amount = 1,900,000 |
| **Root Cause** | Business rule BR-002 not implemented correctly. VIP discount applied 5% instead of 10% |
| **Severity** | 🔴 CRITICAL — affects all VIP orders |
| **Recommendation** | Fix discount calculation logic in `calculateDiscount()`. Check business rule BR-002 |

---

## 6. General Rules for All Outputs

### 1. Encoding
- Use **UTF-8** for all output files.
- Full Unicode support for multiple languages and emojis.

### 2. Markdown Formatting
- Use **GitHub Flavored Markdown** (GFM).
- Tables must have header rows and separator rows.
- Code blocks use triple backticks with language identifiers.

### 3. JSON Formatting
- Use 2-space indentation.
- Keys must use `snake_case`.

### 4. File Naming
- Phase 1: `1_spec_analysis.md`
- Phase 2: `2_testcases.md`
- Phase 3: `3_testdata.json`
- Phase 4: `4_execution_results.json` and `4_execution_log.txt`
- Phase 5: `5_final_report.md` and `5_report_raw.json`

### 5. Status Icons
- ✅ = PASS / Covered / Ready / Completed
- ❌ = FAIL / Not Covered / Error
- ⚠️ = Warning / Partial / Need Review
- ⏭️ = SKIP
- 🔴 = Critical severity
- 🟡 = High severity
- 🟢 = Low severity
- ⬜ = Pending / Not started
```
