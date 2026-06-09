# SPEC Analysis Result - {{BATCH_NAME}}

> **Batch Name:** {{BATCH_NAME}}
> **Batch Code:** {{BATCH_CODE}}
> **SPEC Version:** {{SPEC_VERSION}}
> **Analyzed Date:** {{ANALYSIS_DATE}}
> **Analyst:** {{ANALYST_NAME}}
> **Status:** {{STATUS}}

---

## 1. Overview

{{BATCH_OVERVIEW}}

<!-- Brief description of the batch purpose and scope. -->

---

## 2. Business Rules

<!-- List all business rules extracted from the SPEC. Each rule must have a unique ID, description, condition, and action. -->

| Rule ID | Description | Condition | Expected Action |
|---------|--------|-----------|-----------|
| BR-001 | {{RULE_DESCRIPTION}} | {{RULE_CONDITION}} | {{RULE_ACTION}} |
| BR-002 | {{RULE_DESCRIPTION}} | {{RULE_CONDITION}} | {{RULE_ACTION}} |
| BR-003 | {{RULE_DESCRIPTION}} | {{RULE_CONDITION}} | {{RULE_ACTION}} |
| BR-004 | {{RULE_DESCRIPTION}} | {{RULE_CONDITION}} | {{RULE_ACTION}} |
| BR-005 | {{RULE_DESCRIPTION}} | {{RULE_CONDITION}} | {{RULE_ACTION}} |

---

## 3. Input Fields

<!-- List all fields in the input data. Specify data type, required status, and constraints. -->

| Field Name | Data Type | Required | Constraints | Description |
|------------|-----------|----------|-------------|-------------|
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{REQUIRED_YES_NO}} | {{FIELD_CONSTRAINTS}} | {{FIELD_DESCRIPTION}} |
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{REQUIRED_YES_NO}} | {{FIELD_CONSTRAINTS}} | {{FIELD_DESCRIPTION}} |
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{REQUIRED_YES_NO}} | {{FIELD_CONSTRAINTS}} | {{FIELD_DESCRIPTION}} |

---

## 4. Output Fields

<!-- List all fields in the output data structure. -->

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{FIELD_DESCRIPTION}} |
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{FIELD_DESCRIPTION}} |
| {{FIELD_NAME}} | {{FIELD_TYPE}} | {{FIELD_DESCRIPTION}} |

---

## 5. Constraints & Boundaries

<!-- For each field with constraints, specify min/max, format, and allowed values. -->

| Field Name | Min Value | Max Value | Format | Allowed Values |
|------------|-----------|-----------|--------|----------------|
| {{FIELD_NAME}} | {{MIN_VALUE}} | {{MAX_VALUE}} | {{FORMAT}} | {{ALLOWED_VALUES}} |
| {{FIELD_NAME}} | {{MIN_VALUE}} | {{MAX_VALUE}} | {{FORMAT}} | {{ALLOWED_VALUES}} |

---

## 6. Equivalence Partitions

<!-- Divide the input space into valid and invalid partitions for each field. -->

| Field Name | Valid Partitions | Invalid Partitions |
|------------|------------------|--------------------|
| {{FIELD_NAME}} | {{VALID_PARTITIONS}} | {{INVALID_PARTITIONS}} |
| {{FIELD_NAME}} | {{VALID_PARTITIONS}} | {{INVALID_PARTITIONS}} |

---

## 7. Error Conditions

<!-- List all potential error scenarios and expected behaviors. -->

| Error ID | Error Condition | Expected Behavior |
|----------|-----------------|-------------------|
| ERR-001 | {{ERROR_CONDITION}} | {{EXPECTED_BEHAVIOR}} |
| ERR-002 | {{ERROR_CONDITION}} | {{EXPECTED_BEHAVIOR}} |

---

## 8. Non-Functional Requirements

| Requirement | Description | Threshold |
|-------------|-------------|-----------|
| Performance | {{PERFORMANCE_DESC}} | {{THRESHOLD}} |
| Security | {{SECURITY_DESC}} | {{THRESHOLD}} |
| Logging | {{LOGGING_DESC}} | {{THRESHOLD}} |

---

## 9. Statistics Summary

| Category | Count |
|----------|-------|
| Total Business Rules | {{TOTAL_BUSINESS_RULES}} |
| Total Input Fields | {{TOTAL_INPUT_FIELDS}} |
| Total Output Fields | {{TOTAL_OUTPUT_FIELDS}} |
| Total Constraints | {{TOTAL_CONSTRAINTS}} |
| Total Equivalence Partitions | {{TOTAL_PARTITIONS}} |
| Total Error Conditions | {{TOTAL_ERROR_CONDITIONS}} |
| Estimated Min TestCases | {{ESTIMATED_MIN_TESTCASES}} |

---

## 10. Checklist

- [ ] All business rules extracted from the SPEC.
- [ ] All input fields listed with constraints.
- [ ] All output fields listed.
- [ ] Boundary values determined for all range/length constrained fields.
- [ ] Equivalence partitions identified for all fields.
- [ ] All error conditions listed (field-level and batch-level).
- [ ] Non-functional requirements documented.
- [ ] No conflicting information between sections.
- [ ] Minimum test case count estimated.
