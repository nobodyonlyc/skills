# Guide to SPEC Document Analysis

> This document guides the agent on how to read, analyze, and extract information from a SPEC (Specification) document to prepare for generating test cases and test data.

---

## 1. How to Read and Parse SPEC Documents

### 1.1 SPEC in Markdown Format

Markdown SPECs typically have the following structure:

```markdown
# Batch Name

## Description
General functional description of the batch.

## Input
Description of the input data: file format, fields, constraints.

## Output
Description of the output data: format, fields.

## Business Rules
List of business rules.

## Error Handling
Description of error handling.
```

**How to parse:**
1. Read the entire file and identify the heading structure (H1, H2, H3).
2. Separate content by section (heading).
3. In each section, look for:
   - **Tables**: containing field information and constraints.
   - **Lists**: containing business rules and error conditions.
   - **Code blocks**: containing sample formats or example data.
   - **Inline constraints**: e.g., "maximum 100 characters", "values from 0 to 999", "required".

### 1.2 SPEC in JSON Format

JSON SPECs typically have the following structure:

```json
{
  "batch_name": "BatchXYZ",
  "description": "...",
  "input": {
    "format": "CSV",
    "fields": [
      {
        "name": "customer_id",
        "type": "string",
        "required": true,
        "constraints": {
          "max_length": 20,
          "pattern": "^[A-Z0-9]+$"
        }
      }
    ]
  },
  "output": {
    "fields": [...]
  },
  "business_rules": [...],
  "error_handling": [...]
}
```

**How to parse:**
1. Read the entire JSON and validate its structure.
2. Extract each main key: `input`, `output`, `business_rules`, `error_handling`.
3. For each field in `input.fields`, extract: name, type, required status, and constraints.
4. For `constraints`, pay attention to: `max_length`, `min_length`, `pattern`, `enum`, `min`, `max`.

### 1.3 Key Considerations When Reading SPECs

- **Read the ENTIRE document before extracting** — do not miss any sections.
- **Pay attention to footnotes, notes, and remarks** — these often contain hidden constraints.
- **Look at examples** — examples often reveal the exact data format.
- **Identify implicit constraints** — e.g., a "customer code" is implicitly unique and not null.
- **Identify the version** — a SPEC may have multiple versions; always use the latest one.

---

## 2. How to Extract Business Rules

Business rules are the business logic governing the batch processing. Each rule must be extracted as a clear **condition-action** pair.

### 2.1 Extraction Format

Each business rule must follow this format:

| Rule ID | Description | Condition | Expected Action |
|---|---|---|---|
| BR-001 | Validate age range | `age < 0 OR age > 150` | Reject record, error code: `E001` |
| BR-002 | Calculate VIP discount | `customer_type == "VIP" AND total_purchase > 1000000` | Apply 10% discount |
| BR-003 | Handle duplicates | `customer_id` appears multiple times in input | Keep the first record, skip subsequent ones |

### 2.2 Where to Find Business Rules

Look for business rules in the following sections of the SPEC:
1. **"Business Rules" section** — the primary source.
2. **"Validation" section** — contains rules for validating input data.
3. **"Processing Logic" section** — contains processing rules.
4. **"Error Handling" section** — contains error handling rules.
5. **Field descriptions** — e.g., "the `status` field only accepts: ACTIVE, INACTIVE" → this is a rule.
6. **Examples** — examples often contain implicit rules.

### 2.3 Classification of Business Rules

- **Validation Rules**: Validate the correctness of input data.
- **Calculation Rules**: Formulate calculations (discount, tax, total).
- **Transformation Rules**: Modify data representation (format date, uppercase, trim).
- **Conditional Rules**: Handle conditional processing (if-then-else).
- **Aggregation Rules**: Summarize data (sum, count, average).
- **Ordering Rules**: Specify sorting rules (sort by date, priority).

### 2.4 Practical Example

**SPEC text:**
> The batch processes a CSV file containing orders. Each order has a customer ID, amount, and order date. Orders over 10 million receive a 5% discount. Orders from VIP customers are processed with high priority. If the customer ID does not exist in the system, log a warning and skip the record.

**Extracted rules:**

| Rule ID | Description | Condition | Expected Action |
|---|---|---|---|
| BR-001 | Discount for large orders | `order_amount > 10,000,000` | Apply 5% discount |
| BR-002 | VIP priority | `customer_type == "VIP"` | Process before regular orders |
| BR-003 | Non-existent customer | `customer_id` not found in DB | Log a warning, skip the record |

---

## 3. How to Extract Input/Output Fields

### 3.1 Input Fields

Extract each field according to the following table structure:

| Field Name | Data Type | Required | Constraints | Default | Description |
|---|---|---|---|---|---|
| customer_id | string | Yes | max 20 chars, pattern: `^[A-Z0-9]+$` | — | Unique customer ID |
| order_amount | decimal | Yes | min: 0, max: 999,999,999.99 | — | Order amount |
| order_date | date | Yes | format: `YYYY-MM-DD`, cannot be > current date | — | Order date |
| discount_code | string | No | max 10 chars, alphanumeric | null | Discount code (optional) |
| quantity | integer | Yes | min: 1, max: 9999 | 1 | Product quantity |

### 3.2 Output Fields

| Field Name | Data Type | Description |
|---|---|---|
| process_status | string | Processing status: `SUCCESS`, `FAILED`, `SKIPPED` |
| final_amount | decimal | Final amount after applying discounts |
| error_code | string | Error code if FAILED, null if SUCCESS |
| error_message | string | Detailed error description |

### 3.3 Notes on Extracting Fields

- **Identify the exact data type**: string, integer, decimal, date, boolean, enum.
- **Find all constraints**: length, range, pattern/regex, enum values, format.
- **Distinguish required vs. optional fields**.
- **Determine the default value**: the value used when no data is provided.
- **Look for inter-field dependencies**: e.g., if `type == "REFUND"`, then `refund_reason` is mandatory.

---

## 4. How to Determine Constraints and Boundaries

### 4.1 Types of Constraints

| Constraint Type | Example | Boundary Values |
|---|---|---|
| **Range (min-max)** | age: 0-150 | -1, 0, 1, 149, 150, 151 |
| **Length (min-max length)** | name: 1-100 chars | "", "a", "a"×100, "a"×101 |
| **Pattern (regex)** | email: `^[^@]+@[^@]+$` | valid@email.com, invalid, @, a@ |
| **Enum (allowed values)** | status: [A, I, D] | "A", "I", "D", "X", "", null |
| **Format (date, number)** | date: YYYY-MM-DD | 2024-01-01, 2024-13-01, 2024-02-30 |
| **Unique** | customer_id must be unique | 2 records with the same ID |
| **Not null** | required field | null, empty string, whitespace only |
| **Cross-field** | end_date > start_date | end = start, end < start, end = start + 1 |

### 4.2 Finding Constraints in the SPEC

1. **Explicit constraints**: SPEC explicitly states "maximum 100 characters", "from 0 to 999".
2. **Implicit constraints**: Deduced from context — e.g., "employee code" → alphanumeric, fixed length.
3. **Database constraints**: SPEC references a DB schema → check DB field definitions.
4. **Business constraints**: "order amount cannot be negative" → min = 0.
5. **Format constraints**: "date in ISO format" → YYYY-MM-DD.

### 4.3 Summary Constraints Table

The output must include a summary table:

| Field | Min Value | Max Value | Min Length | Max Length | Format/Pattern | Allowed Values | Other |
|---|---|---|---|---|---|---|---|
| customer_id | — | — | 1 | 20 | `^[A-Z0-9]+$` | — | Unique, Not null |
| age | 0 | 150 | — | — | Integer | — | Not null |
| status | — | — | — | — | — | A, I, D | Not null |
| email | — | — | 5 | 254 | RFC 5322 | — | Optional |

---

## 5. How to Create Equivalence Partitions

### 5.1 Concept

Equivalence Partitioning divides the input domain into groups (partitions) such that:
- All values in the same partition behave similarly.
- You only need to test 1 representative value for each partition.
- You must have both valid partitions and invalid partitions.

### 5.2 Division Method

**Step 1**: Identify the input domain for each field.
**Step 2**: Divide into valid partitions (acceptable values).
**Step 3**: Divide into invalid partitions (unacceptable values).
**Step 4**: Choose 1 representative value for each partition.

### 5.3 Example: `age` field (0-150, integer, required)

| Partition ID | Type | Description | Representative Value |
|---|---|---|---|
| EP-AGE-V1 | Valid | Valid age range (0-150) | 25 |
| EP-AGE-V2 | Valid | Age = 0 (boundary) | 0 |
| EP-AGE-V3 | Valid | Age = 150 (boundary) | 150 |
| EP-AGE-I1 | Invalid | Negative age | -5 |
| EP-AGE-I2 | Invalid | Age exceeds max | 200 |
| EP-AGE-I3 | Invalid | Non-numeric string | "abc" |
| EP-AGE-I4 | Invalid | Null value | null |
| EP-AGE-I5 | Invalid | Decimal value | 25.5 |

### 5.4 Example: `status` field (enum: A, I, D)

| Partition ID | Type | Description | Representative Value |
|---|---|---|---|
| EP-STS-V1 | Valid | Status = A | "A" |
| EP-STS-V2 | Valid | Status = I | "I" |
| EP-STS-V3 | Valid | Status = D | "D" |
| EP-STS-I1 | Invalid | Value not in enum | "X" |
| EP-STS-I2 | Invalid | Lowercase character | "a" |
| EP-STS-I3 | Invalid | Empty string | "" |
| EP-STS-I4 | Invalid | Null value | null |

### 5.5 Output Format

A summary table for all partitions:

| Field | Partition ID | Type | Description | Representative Value | Expected Result |
|---|---|---|---|---|---|
| age | EP-AGE-V1 | Valid | Valid age | 25 | Success |
| age | EP-AGE-I1 | Invalid | Negative age | -5 | Error: E001 |

---

## 6. How to Identify Error Conditions

### 6.1 Classification of Error Conditions

#### Validation Errors
| Error ID | Condition | Expected Behavior |
|---|---|---|
| VE-001 | Required field is null | Reject record, error: "Field X is required" |
| VE-002 | Field exceeds max length | Reject record, error: "Field X exceeds max length" |
| VE-003 | Invalid format (date, email) | Reject record, error: "Invalid format for field X" |
| VE-004 | Value out of range | Reject record, error: "Value out of range for field X" |
| VE-005 | Invalid enum value | Reject record, error: "Invalid value for field X" |

#### Business Logic Errors
| Error ID | Condition | Expected Behavior |
|---|---|---|
| BE-001 | Duplicate key | Skip/merge, log warning |
| BE-002 | Referenced entity not found | Reject record, error: "Entity not found" |
| BE-003 | Business rule violation | Reject record with specific error |
| BE-004 | Inconsistent data | Reject record, error: "Data inconsistency" |

#### System Errors
| Error ID | Condition | Expected Behavior |
|---|---|---|
| SE-001 | Input file not found | Abort batch, error: "File not found" |
| SE-002 | Input file is empty | Abort batch or complete with 0 records |
| SE-003 | Input file format invalid | Abort batch, error: "Invalid file format" |
| SE-004 | Database connection lost | Retry N times, then abort |
| SE-005 | Disk space insufficient | Abort batch, alert admin |

#### Data Format Errors
| Error ID | Condition | Expected Behavior |
|---|---|---|
| DF-001 | Incorrect CSV delimiter | Abort batch, error: "Invalid delimiter" |
| DF-002 | Missing header row | Abort batch, error: "Missing header" |
| DF-003 | Column count mismatch | Reject record, error: "Column mismatch" |
| DF-004 | Unsupported encoding | Abort or convert with warning |

### 6.2 Finding Error Conditions

1. **Read the "Error Handling" section** in the SPEC.
2. **Deduce from constraints**: each constraint violation → 1 error condition.
3. **Deduce from business rules**: each logic failure → 1 error condition.
4. **Consider system-level errors**: file I/O, DB, network, memory.
5. **Consider data format errors**: encoding, delimiter, header, structure.

---

## 7. How to Create a Traceability Table

### 7.1 Purpose

The traceability table ensures that:
- Every requirement in the SPEC is covered by at least 1 analysis item.
- No requirements are missed.
- You can trace from a test case back to its original requirement.

### 7.2 Format

| SPEC Requirement | Ref Section | Extracted Items | Coverage Status |
|---|---|---|---|
| REQ-001: Validate customer_id format | Input > Fields | BR-001, EP-CID-V1, EP-CID-I1-I4, VE-002, VE-003 | ✅ Covered |
| REQ-002: VIP discount | Business Rules | BR-002, EP-DISC-V1, BE-003 | ✅ Covered |
| REQ-003: Handle duplicates | Business Rules | BR-003, BE-001 | ✅ Covered |
| REQ-004: Output file format | Output | Output fields table | ✅ Covered |

### 7.3 Traceability Generation Process

1. **List all requirements** from the SPEC (label as REQ-001, REQ-002, ...).
2. **Record the reference** — section in the SPEC containing the requirement.
3. **Map extracted items** — related BRs, EPs, and Error conditions.
4. **Determine coverage status**:
   - ✅ Covered — has at least 1 analysis item.
   - ⚠️ Partial — has items but is incomplete.
   - ❌ Not Covered — has no items → needs addition.

### 7.4 REVIEW GATE

Upon completing the traceability table:
1. Verify that all requirements have a status of ✅ Covered.
2. If any are ❌ Not Covered, return and add corresponding analysis items.
3. If any are ⚠️ Partial, determine what is missing and complete it.
4. Compare counts (rules, fields, constraints, errors) with the SPEC to ensure completeness.

---

## 8. Summary Checklist

Before completing Phase 1, verify:

- [ ] Read the entire SPEC document without omitting sections.
- [ ] Extracted all business rules (with clear condition-action pairs).
- [ ] Extracted all input fields (with data types, constraints, and required status).
- [ ] Extracted all output fields (with data types and descriptions).
- [ ] Determined all constraints and boundaries.
- [ ] Created equivalence partitions for every input field.
- [ ] Listed all error conditions (validation, business, system, and format).
- [ ] Generated a traceability table, ensuring all requirements are covered.
- [ ] Ensured output matches the template in `templates/spec_analysis_output.md`.
