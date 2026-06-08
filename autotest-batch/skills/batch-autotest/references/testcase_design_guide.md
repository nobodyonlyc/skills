# Guide to TestCase Design

> This document guides the agent on standard test case design techniques, ensuring maximum coverage and effective defect detection.

---

## 1. Equivalence Partitioning (EP)

### 1.1 Concept

Equivalence Partitioning divides the input domain into **equivalence classes** (partitions). The core principles are:
- All values in the same class produce the **same behavior** during processing.
- You only need to test **1 representative value** for each class.
- You must cover both **valid classes** and **invalid classes**.

### 1.2 Application Steps

**Step 1**: Identify the input field and its domain (valid values).
**Step 2**: Divide into valid equivalence classes.
**Step 3**: Divide into invalid equivalence classes.
**Step 4**: Select 1 representative value for each class.
**Step 5**: Create 1 testcase for each class.

### 1.3 Example: `age` field (integer, 0-150, required)

| Class ID | Type | Description | Representative Value | Expected Result |
|---|---|---|---|---|
| EP-AGE-V1 | Valid | Age in valid range (1-149) | 25 | SUCCESS |
| EP-AGE-V2 | Valid | Age = 0 (lower bound) | 0 | SUCCESS |
| EP-AGE-V3 | Valid | Age = 150 (upper bound) | 150 | SUCCESS |
| EP-AGE-I1 | Invalid | Negative age | -5 | ERROR: Out of range |
| EP-AGE-I2 | Invalid | Age exceeds max | 200 | ERROR: Out of range |
| EP-AGE-I3 | Invalid | Non-numeric string | "abc" | ERROR: Invalid type |
| EP-AGE-I4 | Invalid | Null value | null | ERROR: Required field |
| EP-AGE-I5 | Invalid | Decimal value | 25.5 | ERROR: Invalid type |
| EP-AGE-I6 | Invalid | Empty string | "" | ERROR: Required field |

### 1.4 Example: `email` field (string, optional, format RFC 5322)

| Class ID | Type | Description | Representative Value | Expected Result |
|---|---|---|---|---|
| EP-EMAIL-V1 | Valid | Valid standard email | user@example.com | SUCCESS |
| EP-EMAIL-V2 | Valid | Email with subdomain | user@mail.example.com | SUCCESS |
| EP-EMAIL-V3 | Valid | Null (optional field) | null | SUCCESS |
| EP-EMAIL-I1 | Invalid | Missing @ | userexample.com | ERROR: Invalid format |
| EP-EMAIL-I2 | Invalid | Missing domain | user@ | ERROR: Invalid format |
| EP-EMAIL-I3 | Invalid | Missing local part | @example.com | ERROR: Invalid format |
| EP-EMAIL-I4 | Invalid | Contains spaces | user @example.com | ERROR: Invalid format |
| EP-EMAIL-I5 | Invalid | Exceeds max length (254) | "a"×250@b.com | ERROR: Exceeds max length |

### 1.5 Critical Rules

- **Every field** must have at least 1 valid class and 1 invalid class.
- **Required fields**: null and empty values MUST be designated as separate invalid classes.
- **Enum fields**: each valid enum value is 1 valid class; values outside the enum are invalid.
- **Do not forget** type mismatches: sending a string for an integer field, or a number for a date field.

---

## 2. Boundary Value Analysis (BVA)

### 2.1 Concept

Defects are frequently concentrated at the **boundaries** between equivalence classes. BVA tests:
- **min**: The minimum valid value.
- **min - 1**: Just below the minimum (invalid).
- **min + 1**: Just above the minimum (valid).
- **max**: The maximum valid value.
- **max - 1**: Just below the maximum (valid).
- **max + 1**: Just above the maximum (invalid).

### 2.2 Application Steps

For each field with a range or length constraint, generate 6 testcases:

### 2.3 Example: `age` field (integer, 0-150)

| TC ID | Boundary Type | Value | Expected Result | Description |
|---|---|---|---|---|
| BVA-AGE-01 | min - 1 | -1 | ERROR | Just below lower bound |
| BVA-AGE-02 | min | 0 | SUCCESS | Lower bound (valid) |
| BVA-AGE-03 | min + 1 | 1 | SUCCESS | Just above lower bound |
| BVA-AGE-04 | max - 1 | 149 | SUCCESS | Just below upper bound |
| BVA-AGE-05 | max | 150 | SUCCESS | Upper bound (valid) |
| BVA-AGE-06 | max + 1 | 151 | ERROR | Just above upper bound |

### 2.4 Example: `name` field (string, length 1-100)

| TC ID | Boundary Type | Value | Expected Result | Description |
|---|---|---|---|---|
| BVA-NAME-01 | min - 1 | "" (0 chars) | ERROR | Empty string |
| BVA-NAME-02 | min | "a" (1 char) | SUCCESS | Minimum length |
| BVA-NAME-03 | min + 1 | "ab" (2 chars) | SUCCESS | Min + 1 |
| BVA-NAME-04 | max - 1 | "a"×99 | SUCCESS | Max - 1 |
| BVA-NAME-05 | max | "a"×100 | SUCCESS | Maximum length |
| BVA-NAME-06 | max + 1 | "a"×101 | ERROR | Exceeds max length |

### 2.5 BVA for Date Fields

| TC ID | Category | Value | Expected Result | Description |
|---|---|---|---|---|
| BVA-DATE-01 | Valid date | 2024-06-15 | SUCCESS | Regular date |
| BVA-DATE-02 | Leap year end | 2024-02-29 | SUCCESS | Leap year |
| BVA-DATE-03 | Non-leap year end | 2023-02-29 | ERROR | Non-existent date |
| BVA-DATE-04 | Day 0 | 2024-01-00 | ERROR | Invalid day |
| BVA-DATE-05 | Month 13 | 2024-13-01 | ERROR | Month exceeds max |
| BVA-DATE-06 | April 31st | 2024-04-31 | ERROR | April has only 30 days |

### 2.6 Critical Rules

- **Range-constrained fields**: MUST have 6 boundary testcases.
- **Length-constrained fields**: MUST have 6 boundary testcases.
- **Date fields**: test leap years, month-ends, and year boundaries.
- **Decimal fields**: pay attention to precision boundaries (e.g., maximum 2 decimal places).

---

## 3. Decision Table Testing

### 3.1 Concept

Decision Table Testing evaluates all **combinations of conditions** and their corresponding actions. This is suitable when a batch process has multiple interacting business rules.

### 3.2 Application Steps

**Step 1**: List all **conditions** — each condition evaluates to True/False.
**Step 2**: List all **actions** (expected outcomes).
**Step 3**: Create a matrix mapping combinations of conditions to actions.
**Step 4**: Each combination translates to 1 test case.

### 3.3 Example: Order Processing Batch

**Conditions:**
- C1: File exists? (T/F)
- C2: Format valid? (T/F)
- C3: Data valid? (T/F)

**Decision Table:**

| Rule | C1: File exists | C2: Format valid | C3: Data valid | Expected Action |
|---|---|---|---|---|
| R1 | T | T | T | Process successfully |
| R2 | T | T | F | Reject record, log error |
| R3 | T | F | — | Abort batch, error: Invalid format |
| R4 | F | — | — | Abort batch, error: File not found |

> **Note**: The dash `—` denotes a "don't care" condition.
> If C1 = F, there is no need to evaluate C2 or C3.

### 3.4 VIP Discount Calculation Example

**Conditions:**
- C1: Customer is VIP? (T/F)
- C2: Order amount > 10M? (T/F)
- C3: Coupon code applied? (T/F)

| Rule | C1: VIP | C2: >10M | C3: Coupon | Discount | Action |
|---|---|---|---|---|---|
| R1 | T | T | T | 15% + Coupon | Apply max combined discount |
| R2 | T | T | F | 15% | VIP + Large Order discount |
| R3 | T | F | T | 10% + Coupon | VIP + Coupon discount |
| R4 | T | F | F | 10% | VIP discount |
| R5 | F | T | T | 5% + Coupon | Large Order + Coupon discount |
| R6 | F | T | F | 5% | Large Order discount |
| R7 | F | F | T | Coupon only | Coupon discount only |
| R8 | F | F | F | 0% | No discount |

---

## 4. State Transition Testing

### 4.1 Concept

State Transition Testing is applicable when the batch process tracks **states** and **transitions** between them. Tests must cover:
- All **states**.
- All **valid transitions**.
- All **invalid transitions**.

### 4.2 When to Use

- Tracking record statuses (e.g., PENDING → PROCESSING → COMPLETED/FAILED).
- Retry mechanisms (FAILED → RETRY → COMPLETED/PERMANENTLY_FAILED).
- Approval workflows (DRAFT → SUBMITTED → APPROVED/REJECTED).

### 4.3 Example: Order Status Lifecycle

**State Diagram:**
```
[NEW] →(validate)→ [VALIDATED] →(process)→ [COMPLETED]
  |                    |
  ↓                    ↓
[INVALID]          [FAILED] →(retry)→ [VALIDATED]
                       |
                       ↓ (max retries)
                [PERMANENTLY_FAILED]
```

**State Transition Table:**

| Current State | Event | Next State | Action | Testcase ID |
|---|---|---|---|---|
| NEW | validate success | VALIDATED | Proceed to processing | TC-ST-001 |
| NEW | validate fail | INVALID | Log validation error | TC-ST-002 |
| VALIDATED | process success | COMPLETED | Record success result | TC-ST-003 |
| VALIDATED | process fail | FAILED | Log error, increment retry | TC-ST-004 |
| FAILED | retry (count < max) | VALIDATED | Reset status, re-process | TC-ST-005 |
| FAILED | retry (count >= max)| PERMANENTLY_FAILED | Alert administrator | TC-ST-006 |

**Invalid Transitions (must be rejected):**

| Current State | Event | Expected Behavior | Testcase ID |
|---|---|---|---|
| COMPLETED | process | ERROR: Already completed | TC-ST-007 |
| INVALID | process | ERROR: Cannot process invalid | TC-ST-008 |
| PERMANENTLY_FAILED | retry | ERROR: Max retries exceeded | TC-ST-009 |

---

## 5. Negative Testing / Error Guessing

### 5.1 Common Negative Cases

All batch test suites MUST include test cases for:

#### 5.1.1 Input Data Errors

| Category | Test Cases | Example |
|---|---|---|
| **Null/Empty** | Required field = null | `{"name": null}` |
| | Required field = empty string | `{"name": ""}` |
| | Required field = whitespace only | `{"name": "   "}` |
| **Wrong Type** | String in integer field | `{"age": "twenty"}` |
| | Integer in date field | `{"date": 12345}` |
| | Boolean in string field | `{"name": true}` |
| **Overflow** | Integer max + 1 | `{"age": 2147483648}` |
| | String exceeding max length | `{"name": "a" × 10000}` |
| **Special Characters**| SQL injection | `{"name": "'; DROP TABLE users; --"}` |
| | XSS | `{"name": "<script>alert('xss')</script>"}` |
| | Unicode | `{"name": "田中太郎"}` |
| | Zero-width characters | `{"name": "Jo\u200Bhn"}` |

#### 5.1.2 File-Level Errors
- File does not exist.
- File is empty (0 bytes).
- File has only headers, no data.
- Incorrect file format (e.g., CSV instead of JSON).
- Wrong encoding (e.g., SJIS instead of UTF-8).
- File permission denied.

#### 5.1.3 System Errors
- Database connection timeout or refused.
- Database query deadlock.
- Disk full when writing output files.
- Output directory does not exist.
- External API timeouts or failures.

### 5.2 Critical Rules

- **Fault Isolation Principle**: Each invalid test dataset must violate **exactly one** constraint.
- Always test empty files and single-record files.
- Test null, empty, and wrong types for all required fields.

---

## 6. TestCase Naming Convention

### 6.1 Format

```
TC-{NNN} — {CATEGORY}_{ShortDescription}
```

Fields:
- `{NNN}`: 3-digit sequential number (001, 002, ...).
- `{CATEGORY}`: Testcase category (NORMAL, BOUNDARY, LOGIC, STATE, NEGATIVE, EDGE).
- `{ShortDescription}`: Brief description using underscores.

### 6.2 Categories

| Category | Description | Example |
|---|---|---|
| **NORMAL** | Happy path execution | TC-001 — NORMAL_valid_basic_input |
| **BOUNDARY** | Boundary value analysis | TC-010 — BOUNDARY_age_min_value |
| **LOGIC** | Business logic (decision tables) | TC-020 — LOGIC_vip_discount_with_coupon |
| **STATE** | Lifecycle state changes | TC-030 — STATE_new_to_validated |
| **NEGATIVE** | Error conditions | TC-040 — NEGATIVE_null_required_field |
| **EDGE** | Rare edge cases | TC-050 — EDGE_unicode_input |

### 6.3 Priority

- **CRITICAL**: Core business logic, basic happy path.
- **HIGH**: Validation rules, key boundary cases.
- **MEDIUM**: Standard negative cases, error handling.
- **LOW**: Rare unicode, extreme values, concurrent access.

---

## 7. Traceability Matrix

### 7.1 Format

| Requirement ID | Requirement Description | TestCase IDs | Coverage Status | Priority |
|---|---|---|---|---|
| REQ-001 | Validate customer_id format | TC-001, TC-010, TC-040 | ✅ Full | CRITICAL |
| REQ-002 | Validate age range 0-150 | TC-010, TC-011, TC-012, TC-013 | ✅ Full | HIGH |

---
## 8. Batch Test Data Matrix

To prove systematic and 100% test coverage to stakeholders, you must construct a **Batch Test Data Matrix** during the testcase design phase.

### 8.1 Concept
- **Vertical Axis**: Input fields identified from the SPEC (with their technical data types, e.g., `customer_id (String)`, `amount (Decimal)`, `order_date (Date)`).
- **Horizontal Axis**: Test characteristics including both generic field validations and batch-specific behaviors:
  1. **Normal Case**: Standard valid input.
  2. **Boundary**: Min/Max boundary values.
  3. **Null/Empty/Space**: NULL, empty string `""`, and space-padded string `"   "`.
  4. **Invalid / Format**: Data type mismatch, wrong formats, negative values where forbidden.
  5. **Encoding / Special Characters**: Shift-JIS, half-width vs full-width, wave dash, BOM, control characters.
  6. **Batch-specific Volume**: Empty file (0 records), Single record (1 record), Large volume.
  7. **Batch-specific States**: Duplicate keys, Sort order violation, Truncated/Malformed record.
  8. **Batch-specific Resilience**: Mid-run crash & restart (Rerun/Recovery Idempotency).

### 8.2 Matrix Format Template

Mark cells with the corresponding **TestCase ID** (`TC-xxx`) covering that specific intersection, or `N/A` (if logically excluded based on SPEC, documented with a reason).

| Field & Technical Type | Normal | Boundary | Null/Empty/Space | Invalid / Format | Encoding / Spec. Char | Batch Volume / State | Rerun / Resilience |
|---|---|---|---|---|---|---|---|
| **customer_id** <br>*(String, Max 10, Fixed)* | `TC-001` | `TC-010` (1 char) <br> `TC-011` (10 chars) | `TC-040` (Null) <br> `TC-041` (Empty) <br> `TC-042` (Spaces) | `TC-043` (11 chars) | `TC-050` (Shift-JIS) <br> `TC-051` (Control char) | `TC-060` (Duplicate) | `N/A` (N/A at field level) |
| **amount** <br>*(Decimal, Min 0)* | `TC-001` | `TC-012` (0) | `TC-044` (Null) | `TC-045` (-1) <br> `TC-046` (Decimal precision) | `N/A` | `N/A` | `TC-080` (Rerun idempotency check) |
| **order_date** <br>*(Date, YYYYMMDD)* | `TC-001` | `TC-013` (Leap year) | `TC-047` (Null) | `TC-048` (Invalid day) <br> `TC-049` (Wrong format) | `N/A` | `TC-061` (Out-of-order) | `N/A` |
| **Global File/Batch** | `TC-001` | `N/A` | `TC-070` (Empty file) | `TC-071` (Wrong format) | `TC-072` (BOM prefix) | `TC-073` (1 record) <br> `TC-074` (Large vol) | `TC-081` (Network fail) <br> `TC-082` (Disk full) |

### 8.3 Rules for Matrix Completion
1. **No Blank Cells**: Every cell must contain a `TC-xxx` or an explicit `N/A` with a brief explanation.
2. **Field Isolation**: When testing field-level validations (Normal, Boundary, Null, Invalid, Encoding), modify only the target field while keeping all other fields at their default `Normal` values.
3. **Traceability**: Every TestCase ID listed in the matrix must map to a test case in the test case design document and have a corresponding dataset in the test data file.

---

## 9. TestCase Design Checklist

- [ ] Every equivalence partition (Phase 1) has at least 1 NORMAL test case.
- [ ] Every range/length constraint has 6 BOUNDARY test cases.
- [ ] Every combination of business rules has a LOGIC test case.
- [ ] Stateful batch processes have STATE test cases covering all transitions.
- [ ] NEGATIVE test cases cover null, empty, and wrong types for all required fields.
- [ ] EDGE test cases cover Unicode, SQL injection, XSS, and special characters.
- [ ] Batch Test Data Matrix is created, showing 100% coverage or logical exclusion with reasons.
- [ ] Every testcase includes ID, Name, Category, Priority, Description, Input Summary, and Expected Output.
- [ ] The Traceability Matrix coverage is ≥ 95% (ideally 100%).
- [ ] Output matches the template in `templates/testcase_output.md`.

