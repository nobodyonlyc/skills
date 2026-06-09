# 📄 Phase 1: SPEC Receipt and Analysis

> **Workflow ID**: WF1  
> **Phase**: 1/5  
> **Next**: [Phase 2 - TestCase Generation](./wf2_testcase_generation.md)

---

## 1. 🎯 Purpose and Scope

### Purpose
Perform a comprehensive analysis of the SPEC (Specification) document to extract **all necessary information** required for automated testcase generation in Phase 2.

### Scope
This phase covers the extraction of:
- ✅ Business Rules
- ✅ Input/Output Fields
- ✅ Constraints/Boundaries
- ✅ Equivalence Partitions
- ✅ Error Conditions

### Expected Results and Storage
- A complete, structured SPEC analysis document, ready to serve as input for Phase 2.
- **Mandatory Storage**: Must be recorded as `1_spec_analysis.md` and saved in the centralized run directory (`test_runs/run_<timestamp>_<run_id>/`).

---

## 2. 📥 Input

### SPEC Document
- **Supported Formats**: PDF, Word (.docx), Markdown (.md), Plain Text (.txt)
- **Language**: Any language (e.g., Japanese, Vietnamese, English, etc.)

### Minimum Requirements for SPEC
The SPEC must contain at least:

| Component | Required | Description |
|---|---|---|
| Business Description | ✅ | Functional description of the batch process |
| Business Rules | ✅ | Business rules and processing logic |
| Field Definitions | ✅ | Field name, data type, length, and mandatory/optional status |
| Constraints | ✅ | Min/max values, formats, and valid values |
| Input Format | ✅ | Structure of the input file (CSV, fixed-length, JSON, etc.) |
| Output Format | ✅ | Structure of output files and expected behavior |
| Error Handling | ⭕ | Error handling rules (if defined in SPEC) |
| State Transitions | ⭕ | State transitions (if applicable) |

> ⚠️ **If the SPEC lacks required information**, refer to [Error Handling](#6--error-handling--issue-resolution) below.

---

## 3. 📋 Detailed Process

### Process Overview Table

| Step | Action | Input | Output | Review Criteria |
|---|---|---|---|---|
| 1 | Read SPEC | SPEC document | Parsed SPEC content | Readable SPEC, complete content |
| 2 | Extract Business Rules | SPEC content | List of BR-xxx rules | Each rule has ID, description, condition, result |
| 3 | Extract Input/Output Fields | SPEC content | Detailed fields table | All fields have type, length, and mandatory flag |
| 4 | Identify Constraints/Boundaries | Fields + Rules | Constraints table | Each field has clear min, max, and format constraints |
| 5 | Create Equivalence Partitions | Constraints | Partitions table | Each field has ≥1 valid and ≥1 invalid partition |
| 6 | Extract Data States | SPEC content | List of processing states | Identify all valid and invalid states |
| 7 | Extract DB Interactions | SPEC content | CRUD Impacted Tables list | List target tables, columns, and operations |
| 8 | Identify Error Conditions | Rules + Constraints | List of error conditions | Covers null, empty, out-of-range, and wrong type |
| 9 | REVIEW GATE | All outputs | Checklist status (pass/fail) | All checklist criteria are met |

---

### 📌 Step 1: SPEC Receipt and Reading

**Detailed Description:**
1. Receive the SPEC document (file path or direct content).
2. Read the entire SPEC content.
3. Identify the document structure (sections, tables, diagrams).
4. Record the SPEC version and update date (if available).
5. Summarize the core purpose in 3-5 sentences.

**Review Criteria:**
- [ ] SPEC is read completely.
- [ ] Core purpose of the batch process is identified.
- [ ] Main sections of the SPEC are listed.

**Example Output:**
```
📄 SPEC Summary:
- Name: Interbank Transfer Transaction Processing Batch
- Version: 2.1
- Date: 2026-05-15
- Purpose: Process transfer transaction files from partner banks,
  validate data, calculate fees, and record transactions to core banking.
- Main Sections: Input Format, Business Rules, Output Format, Error Handling
```

---

### 📌 Step 2: Extracting Business Rules

**Detailed Description:**
1. Read the SPEC carefully to locate all business rules.
2. Assign an ID to each rule: `BR-001`, `BR-002`, etc.
3. Each rule must contain:
   - **ID**: Unique identifier.
   - **Description**: Natural language description of the rule.
   - **Condition**: Under what conditions the rule applies (IF/WHEN).
   - **Result**: Expected action or output (THEN).
   - **Source**: SPEC section containing this rule.
4. Identify **implicit rules** (unstated business rules).
5. Identify **dependent rules** (rules dependent on each other).

**Review Criteria:**
- [ ] Each rule has all 4 components: ID, Description, Condition, Result.
- [ ] No duplicate rules.
- [ ] Implicit rules are recognized and documented.
- [ ] Dependencies between rules are noted.

**Example Output:**

| ID | Description | Condition | Expected Result | Source |
|---|---|---|---|---|
| BR-001 | Validate transaction amount | Amount > 0 AND ≤ 500,000,000 VND | Transaction accepted | Section 3.1 |
| BR-002 | Calculate transfer fee | Valid transaction | Fee = 0.05% × amount, min 10,000 VND, max 50,000 VND | Section 3.2 |
| BR-003 | Validate bank code | Bank code must be in the linked bank list | Transaction accepted | Section 3.3 |
| BR-004 | Check balance | Source account balance ≥ amount + fee | Transaction executed | Section 3.4 |
| BR-005 | Handle duplicate transaction | Transaction ID already exists today | Reject transaction, error code: ERR-DUP | Section 3.5 |
| BR-006 | Daily transaction limit | Total transactions of an account today ≤ 50 | Allow transaction | Section 3.6 |
| BR-007 | Transaction date format | Date format must be YYYYMMDD and valid date | Process transaction | Section 2.1 |

---

### 📌 Step 3: Extracting Input/Output Fields

**Detailed Description:**
1. List **all** fields in the input file.
2. List **all** fields in the output file/database.
3. For each field, record:
   - Field name.
   - Data type (String, Number, Date, Boolean, etc.).
   - Length (min, max, or fixed).
   - Required status (Mandatory/Optional).
   - Detailed description.
   - Default value (if any).
4. Strictly distinguish between input and output fields.

**Review Criteria:**
- [ ] All fields from the SPEC are listed.
- [ ] Each field has a clear data type.
- [ ] Mandatory/Optional status is determined for each field.
- [ ] No fields are missing.

**Example Output — Input Fields:**

| # | Field Name | Data Type | Length | Required | Description | Default Value |
|---|---|---|---|---|---|---|
| 1 | transaction_id | String | 20 (fixed) | ✅ Mandatory | Unique transaction ID | — |
| 2 | source_account | String | 10-16 | ✅ Mandatory | Source account number | — |
| 3 | dest_account | String | 10-16 | ✅ Mandatory | Destination account number | — |
| 4 | amount | Number (Decimal) | 1-15 | ✅ Mandatory | Transaction amount (VND) | — |
| 5 | bank_code | String | 3-8 | ✅ Mandatory | Partner bank code | — |
| 6 | transaction_date | Date (YYYYMMDD) | 8 (fixed) | ✅ Mandatory | Transaction date | — |
| 7 | description | String | 0-140 | ⭕ Optional | Transfer remarks | "" |
| 8 | priority | String | 1 | ⭕ Optional | Priority level (N=Normal, H=High) | "N" |

**Example Output — Output Fields:**

| # | Field Name | Data Type | Description |
|---|---|---|---|
| 1 | transaction_id | String | Transaction ID (from input) |
| 2 | status | String | APPROVED / REJECTED |
| 3 | fee | Number (Decimal) | Calculated transaction fee |
| 4 | error_code | String | Error code (if REJECTED) |
| 5 | processed_date | Date | Processing date |

---

### 📌 Step 4: Identifying Constraints/Boundaries

**Detailed Description:**
1. For each field, identify all constraints:
   - **Value range**: Min, Max (for numeric values).
   - **Length range**: Min length, Max length (for strings).
   - **Format**: Regex pattern, date format, etc.
   - **Valid values**: List of valid values (for enums).
   - **Dependent constraints**: Constraints depending on other fields.
2. Note the source of each constraint (SPEC section).
3. Identify **implicit constraints** (e.g., numeric fields cannot contain letters).

**Review Criteria:**
- [ ] Each field has at least 1 constraint.
- [ ] Min/Max values are specific (not "reasonable range").
- [ ] Format patterns are clear.
- [ ] Dependent constraints are documented.

**Example Output:**

| Field | Constraint Type | Min | Max | Format/Pattern | Valid Values | Notes |
|---|---|---|---|---|---|---|
| transaction_id | Length | 20 | 20 | `[A-Z0-9]{20}` | — | Fixed 20 characters, uppercase letters and numbers only |
| source_account | Length | 10 | 16 | `[0-9]+` | — | Numeric characters only |
| amount | Value | 1 | 500,000,000 | — | — | VND currency, no negative numbers |
| amount | Precision | — | — | Max 2 decimal places | — | — |
| bank_code | Value | — | — | — | VCB, TCB, ACB, MBB, BID, CTG, VPB, TPB | List of linked banks |
| transaction_date | Format | — | — | `YYYYMMDD` | — | Must be a valid date, not in the future |
| description | Length | 0 | 140 | — | — | Unicode allowed, control characters prohibited |
| priority | Value | — | — | — | N, H | N=Normal, H=High |

---

### 📌 Step 5: Creating Equivalence Partitions

**Detailed Description:**
1. For each field and constraint, divide the input domain into equivalence partitions:
   - **Valid partitions**: Groups of valid values that yield the same expected behavior.
   - **Invalid partitions**: Groups of invalid values.
2. Each partition must include:
   - Partition Name/ID.
   - Range description.
   - Representative value.
   - Expected result (accepted/rejected).

**Review Criteria:**
- [ ] Each field has ≥ 1 valid partition.
- [ ] Each field has ≥ 1 invalid partition.
- [ ] Partitions cover the entire input domain.
- [ ] Partitions do not overlap.

**Example Output:**

| Field | Partition | Type | Range | Representative Value | Expected |
|---|---|---|---|---|---|
| amount | P1: Small amount | Valid | 1 - 1,000,000 | 500,000 | APPROVED |
| amount | P2: Medium amount | Valid | 1,000,001 - 100,000,000 | 50,000,000 | APPROVED |
| amount | P3: Large amount | Valid | 100,000,001 - 500,000,000 | 300,000,000 | APPROVED |
| amount | P4: Zero amount | Invalid | 0 | 0 | REJECTED |
| amount | P5: Negative amount | Invalid | < 0 | -100,000 | REJECTED |
| amount | P6: Over limit | Invalid | > 500,000,000 | 600,000,000 | REJECTED |
| bank_code | P1: Valid bank code | Valid | In whitelist | "VCB" | APPROVED |
| bank_code | P2: Bank code not exists | Invalid | Not in whitelist | "XYZ" | REJECTED |
| bank_code | P3: Empty bank code | Invalid | Empty string | "" | REJECTED |
| priority | P1: Normal | Valid | "N" | "N" | Process normally |
| priority | P2: High | Valid | "H" | "H" | Process with high priority |
| priority | P3: Invalid value | Invalid | Not N or H | "X" | REJECTED |

---

### 📌 Step 6: Extracting Data States

**Detailed Description:**
1. Analyze the lifecycle of records processed by the batch system.
2. Identify all possible processing states:
   - Initial states (e.g. `UNPROCESSED`, `NEW`).
   - Intermediate states (e.g. `PROCESSING`, `VALIDATED`).
   - Final states (e.g. `PROCESSED_SUCCESS`, `PROCESSED_FAILED`, `SKIPPED`).
3. Identify invalid state transitions (e.g. attempting to re-process an already successful record).
4. Record these states in a structured table.

**Review Criteria:**
- [ ] All processing states of the batch are identified.
- [ ] Transition triggers (what event causes state change) are documented.
- [ ] Invalid/illegal state transitions are identified for negative testing.

**Example Output:**

| State Name | Type | Description | Allowed Next States |
|---|---|---|---|
| `UNPROCESSED` | Initial | Record is newly imported and ready for batch run | `PROCESSING` |
| `PROCESSING` | Intermediate | Record is currently being validated and calculated | `PROCESSED_SUCCESS`, `PROCESSED_FAILED` |
| `PROCESSED_SUCCESS` | Final | Record processed successfully, fee calculated | None (Terminal state) |
| `PROCESSED_FAILED` | Final | Record failed validation or DB save | None (Terminal state) |

---

### 📌 Step 7: Extracting Impacted Database Tables

**Detailed Description:**
1. Identify all database tables read or modified by the batch process.
2. Identify the action type for each table:
   - **C** (Create / Insert)
   - **R** (Read / Select)
   - **U** (Update)
   - **D** (Delete)
3. Document which key columns are read or updated.
4. Record these interactions in a CRUD table.

**Review Criteria:**
- [ ] All source tables (Read) are listed.
- [ ] All target tables (Insert/Update) are listed.
- [ ] Audit trail or log tables are accounted for.

**Example Output:**

| Table Name | Action | Key Columns Impacted | Description / Notes |
|---|---|---|---|
| `accounts` | R, U | `account_id`, `balance` | Read current balance, update balance after deducting amount + fee |
| `transactions` | R | `transaction_id`, `amount`, `bank_code` | Read incoming transaction data |
| `settlement_summary` | C, U | `summary_id`, `total_amount`, `tx_count` | Insert or update daily settlement summary records |
| `audit_logs` | C | `log_id`, `timestamp`, `log_level`, `message` | Insert system execution events |

---

### 📌 Step 8: Identifying Error Conditions

**Detailed Description:**
1. List all potential error conditions:
   - Null/Missing: Mandatory field is missing.
   - Empty: Field has empty string value.
   - Out-of-range: Values outside the allowed range.
   - Wrong type: Invalid data type.
   - Format error: Violates expected format.
   - Business rule violation: Violates business rules.
   - System error: System errors (if mentioned in SPEC).
2. Each error condition must include:
   - ID (ERR-xxx).
   - Trigger (condition causing the error).
   - Expected behavior (how the system processes it).
   - Error message/code (if defined in SPEC).
   - Related business rule (BR-xxx).

**Review Criteria:**
- [ ] Covers null/empty scenarios for mandatory fields.
- [ ] Covers out-of-range scenarios for numeric fields.
- [ ] Covers wrong data types.
- [ ] Covers format errors for date and account fields.
- [ ] Clear expected behavior for each error condition.

**Example Output:**

| ID | Trigger | Related Field | Expected Behavior | Error Code | Related BR |
|---|---|---|---|---|---|
| ERR-001 | transaction_id is null | transaction_id | Reject record, log error | ERR-MISSING-TXID | — |
| ERR-002 | transaction_id duplicate today | transaction_id | Reject record | ERR-DUP | BR-005 |
| ERR-003 | amount = 0 | amount | Reject record | ERR-INVALID-AMT | BR-001 |
| ERR-004 | amount < 0 | amount | Reject record | ERR-INVALID-AMT | BR-001 |
| ERR-005 | amount > 500,000,000 | amount | Reject record | ERR-OVER-LIMIT | BR-001 |
| ERR-006 | amount contains letters | amount | Reject record | ERR-INVALID-TYPE | — |
| ERR-007 | bank_code invalid | bank_code | Reject record | ERR-INVALID-BANK | BR-003 |
| ERR-008 | transaction_date wrong format | transaction_date | Reject record | ERR-INVALID-DATE | BR-007 |
| ERR-009 | transaction_date in the future | transaction_date | Reject record | ERR-FUTURE-DATE | BR-007 |
| ERR-010 | source_account = dest_account | source_account, dest_account | Reject record | ERR-SAME-ACCT | — |
| ERR-011 | Insufficient balance | source_account, amount | Reject record | ERR-INSUF-BAL | BR-004 |
| ERR-012 | Exceeds 50 transactions/day | source_account | Reject record | ERR-DAILY-LIMIT | BR-006 |
| ERR-013 | description contains control characters | description | Reject record | ERR-INVALID-CHAR | — |

---

### 📌 Step 9: REVIEW GATE

**Detailed Description:**
This is the final quality check before moving to Phase 2. The process includes performing a brainstorming quality analysis, printing the summary report directly in the agent chat (DO NOT create a separate phase report file on disk), and obtaining user approval.

1. **Agent Brainstorming**:
   - Assess the accuracy and completeness of the SPEC analysis document.
   - Identify unclear constraints or contradictions, resolving them using assumptions labeled [ASSUMPTION].
   - Self-check against the checklist below.
2. **Print Phase Summary**:
   - Print a summary of Phase 1 results (extracted rules, fields count, constraints, data states, and database tables) directly in the agent chat conversation.
3. **Present Options via ask_question**:
    - The Agent calls the `ask_question` tool in the detected language to ask:
      - **Question**: "Is the SPEC analysis (Phase 1) output satisfactory?"
      - **Options**:
        - "(Recommended) Everything is fine, proceed to Phase 2 (TestCase Generation)."
        - "There are issues, I want to adjust or provide feedback."
4. **Wait for Response**: The pipeline blocks until the user responds to the `ask_question` modal.

**Review Gate 1 Checklist:**

```
REVIEW GATE 1 - CHECKLIST
==========================

□ 1. Business Rules
  □ All rules are extracted and assigned an ID (BR-xxx).
  □ Each rule contains: Description, Condition, Expected Result.
  □ Implicit rules are identified.
  □ Dependencies between rules are recorded.

□ 2. Input/Output Fields
  □ All input fields are listed.
  □ All output fields are listed.
  □ Each field has: Type, Length, Mandatory/Optional status.

□ 3. Constraints
  □ Each field has at least 1 constraint.
  □ Min/Max values are specific (not "reasonable").
  □ Format patterns are clear.
  □ Dependent constraints are documented.

□ 4. Equivalence Partitions
  □ Each field has ≥ 1 valid partition.
  □ Each field has ≥ 1 invalid partition.
  □ Partitions cover the entire domain.
  □ Representative values are logical.

□ 5. Data States
  □ All record processing states (initial, intermediate, terminal) are identified.
  □ Invalid/illegal state transitions are documented for testing.

□ 6. Database Interactions
  □ All source and target tables are mapped with CRUD actions.
  □ Key columns affected are documented.

□ 7. Error Conditions
  □ Covers null/empty for mandatory fields.
  □ Covers out-of-range for numeric fields.
  □ Covers wrong data types.
  □ Covers format errors.
  □ Expected behavior is clear.

□ 8. General
  □ No "TBD" or "unclear" items remain.
  □ All assumptions are marked as [ASSUMPTION].
  □ Output is detailed enough for testcase generation.
  □ User has approved the SPEC analysis.
```

**Decision:**
- **Approved by user (Option 1 selected in ask_question)** -> Proceed to Phase 2.
- **Adjustments requested (Option 2 selected in ask_question)** -> Ask the user for feedback in chat, update Phase 1 based on feedback, and repeat Review Gate 1.

---

## 4. 📝 Complete Output Example

### Sample Scenario: Interbank Transfer Transaction Processing Batch

<details>
<summary><b>📋 Click to view complete example output</b></summary>

#### Business Rules

| ID | Description | Condition | Result | Source |
|---|---|---|---|---|
| BR-001 | Validate amount | 1 ≤ amount ≤ 500,000,000 | Accept | Sec 3.1 |
| BR-002 | Calculate fee | Valid transaction | fee = max(10000, min(50000, amount × 0.05%)) | Sec 3.2 |
| BR-003 | Validate bank code | bank_code ∈ {VCB,TCB,ACB,MBB,BID,CTG,VPB,TPB} | Accept | Sec 3.3 |

#### Fields Table

| Field | Type | Length | Mandatory | Description |
|---|---|---|---|---|
| transaction_id | String | 20 fixed | ✅ | Transaction ID |
| amount | Decimal | 1-15 | ✅ | Amount in VND |
| bank_code | String | 3-8 | ✅ | Bank code |

#### Constraints Table

| Field | Min | Max | Format | Valid Values |
|---|---|---|---|---|
| amount | 1 | 500,000,000 | 2 decimal | — |
| bank_code | — | — | — | VCB,TCB,ACB,MBB,BID,CTG,VPB,TPB |

#### Equivalence Partitions

| Field | Partition | Valid/Invalid | Range | Representative |
|---|---|---|---|---|
| amount | Small | Valid | 1-1M | 500,000 |
| amount | Large | Valid | 100M-500M | 300,000,000 |
| amount | Zero | Invalid | 0 | 0 |
| amount | Negative | Invalid | <0 | -100,000 |

#### Error Conditions

| ID | Trigger | Expected | Error Code |
|---|---|---|---|
| ERR-001 | amount = 0 | Reject | ERR-INVALID-AMT |
| ERR-002 | amount < 0 | Reject | ERR-INVALID-AMT |
| ERR-003 | bank_code invalid | Reject | ERR-INVALID-BANK |

</details>

---

## 5. 🚪 Gate Condition (Phase Transition Requirements)

### MANDATORY conditions to transition to Phase 2:

| # | Condition | Level |
|---|---|---|
| 1 | All business rules are extracted and assigned an ID | 🔴 Mandatory |
| 2 | All input/output fields are identified | 🔴 Mandatory |
| 3 | All constraints have specific values (min, max, format) | 🔴 Mandatory |
| 4 | Equivalence partitions are created for each field | 🔴 Mandatory |
| 5 | Error conditions are listed | 🔴 Mandatory |
| 6 | No "TBD" or "unclear" items remain | 🔴 Mandatory |
| 7 | User approval (Option 1 in ask_question) is received | 🔴 Mandatory |
| 8 | File `1_spec_analysis.md` is created and saved in the centralized run directory | 🔴 Mandatory |
| 9 | All assumptions are marked as [ASSUMPTION] | 🟡 Recommended |

> ⛔ **If any MANDATORY condition is not met or user approval is missing, DO NOT proceed to Phase 2.**

---

## 6. ⚠️ Error Handling / Issue Resolution

### Ambiguous SPEC
```
Scenario: SPEC states "amount must be reasonable"
→ Action:
  1. Record in the "Unclear Items" list.
  2. Propose specific constraints based on domain knowledge.
  3. Mark as: [ASSUMPTION] amount range: 1 - 500,000,000 VND.
  4. Log warning: "⚠️ Ambiguous SPEC at section X, constraint assumed."
```

### Incomplete SPEC
```
Scenario: SPEC does not state the max length of the description field
→ Action:
  1. Record in the "Missing Items" list.
  2. Propose a reasonable default value: [ASSUMPTION] max_length = 255.
  3. Note: Needs confirmation from BA/PO.
```

### Contradictory SPEC
```
Scenario: Section 3.1 states amount max = 500M, Section 4.2 states amount max = 1B
→ Action:
  1. Record the contradiction.
  2. Priority order: Business Rules > Technical Details.
  3. Choose the value from the Business Rules section.
  4. Mark as: [CONFLICT] amount max: Chosen 500M (BR) vs 1B (Technical).
  5. Log: "⚠️ Contradiction detected in section 3.1 vs 4.2."
```

### Template for Logging Issues

```markdown
## 📋 Issues Detected in SPEC

### Unclear Items
| # | Section | Content | Assumption | Confirmation Needed |
|---|---|---|---|---|
| 1 | 3.1 | "Reasonable amount" | Max = 500M | ✅ |

### Missing Items
| # | Field/Rule | Missing Info | Proposed Value |
|---|---|---|---|
| 1 | description | Max length | 255 characters |

### Conflicts
| # | Section A | Section B | Content | Decision |
|---|---|---|---|---|
| 1 | 3.1 | 4.2 | Max amount | Chosen 500M (BR) |
```

---

## 7. 💡 Tips and Common Mistakes

### ✅ Best Practices

1. **Read the SPEC at least twice** — The first time for overview, the second for detailed extraction.
2. **Always identify implicit constraints** — E.g., date fields always require a "valid date" even if unstated.
3. **Pay attention to dependent fields** — E.g., Field A is valid only when Field B contains a certain value.
4. **Record domain-specific rules** — Each industry has specific rules (e.g., banking: SWIFT code, account format).
5. **Check format consistency** — The input format must align with business rules.

### ❌ Common Mistakes

| # | Mistake | Consequence | How to Avoid |
|---|---|---|---|
| 1 | Missing implicit constraints | Test cases miss scenarios like "February 30th" | Always add implicit constraints for dates and formats |
| 2 | Assuming constraints not in SPEC without marking | Test cases violate requirements | Only use constraints from SPEC; mark others as [ASSUMPTION] |
| 3 | Lacking boundary tests for string lengths | Missed edge cases | Always define min/max length for every string field |
| 4 | Neglecting null/empty handling | Incomplete negative test cases | Always ask: "how does this field handle null/empty?" |
| 5 | Conflating input vs output fields | Confusion during testcase generation | Keep Input Fields and Output Fields in separate tables |
| 6 | Ignoring error codes/messages | Unable to verify actual error outputs | Extract all error codes from the SPEC |
| 7 | Overlooking dependent rules | Missed test case combinations | Draw dependency graphs between rules |

---

## 7.5 ⚠️ Critical Rules

1. **Testing Source Code Only (No code changes during test)**:
   - Execute testing on the existing application code as-is. Absolutely no modifications to the production code are permitted.
   - If a bug is found in the application, do not change the testcase or expected output to hide the issue. Record the bug details transparently in the final report without attempting to fix the source code.
2. **Centralized Output Storage**:
   - Write the entire SPEC analysis output to `1_spec_analysis.md` and save it inside the centralized run directory: `test_runs/run_<timestamp>_<run_id>/`.
3. **Language Alignment Rule**:
   - Inspect the input SPEC/prompt to determine the execution language.
   - All generated output files, log outputs (including execution status logs shown to the user), internal reasoning/thinking blocks, and all chat communications must be written in the **exact same language** as detected (e.g., if the user prompts in Japanese, your thoughts, logs, and answers must be entirely in Japanese without mixing English or Vietnamese).

---

## 8. 📚 References

- **Next Phase**: [WF2 - TestCase Generation](./wf2_testcase_generation.md)
- **Pipeline Overview**: [README](./README.md)
- **Full Pipeline**: [WF Full Pipeline](./wf_full_pipeline.md)

---

> 📌 **Reminder**: Phase 1 output is the FOUNDATION of the entire testing process. If Phase 1 is incorrect or incomplete, ALL subsequent phases will be impacted. Spend sufficient time and care on this phase.
