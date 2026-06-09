# TestCase Suite - {{BATCH_NAME}}

> **Batch Name:** {{BATCH_NAME}}
> **Batch Code:** {{BATCH_CODE}}
> **SPEC Version:** {{SPEC_VERSION}}
> **Generation Date:** {{GENERATION_DATE}}
> **Author:** {{GENERATOR_NAME}}
> **Based on SPEC Analysis:** {{SPEC_ANALYSIS_REF}}

---

## 1. TestCase Summary

### 1.1 Statistics by Category

| TestCase Category | Count | Percentage |
|-------------------|-------|------------|
| Normal | {{NORMAL_COUNT}} | {{NORMAL_PCT}}% |
| Boundary | {{BOUNDARY_COUNT}} | {{BOUNDARY_PCT}}% |
| Negative | {{NEGATIVE_COUNT}} | {{NEGATIVE_PCT}}% |
| Edge Case | {{EDGE_COUNT}} | {{EDGE_PCT}}% |
| Decision Table | {{DECISION_COUNT}} | {{DECISION_PCT}}% |
| Volume | {{VOLUME_COUNT}} | {{VOLUME_PCT}}% |
| **Total** | **{{TOTAL_COUNT}}** | **100%** |

### 1.2 Statistics by Priority

| Priority | Count | Percentage |
|----------|-------|------------|
| Critical | {{CRITICAL_COUNT}} | {{CRITICAL_PCT}}% |
| High | {{HIGH_COUNT}} | {{HIGH_PCT}}% |
| Medium | {{MEDIUM_COUNT}} | {{MEDIUM_PCT}}% |
| Low | {{LOW_COUNT}} | {{LOW_PCT}}% |
| **Total** | **{{TOTAL_COUNT}}** | **100%** |

---

## 2. Detailed TestCase List

### 2.1 Normal Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Normal | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

### 2.2 Boundary Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Boundary | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

### 2.3 Negative Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Negative | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

### 2.4 Edge Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Edge Case | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

### 2.5 Decision Table Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Decision Table | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

### 2.6 Volume Cases

| ID | TestCase Name | Category | Priority | Description | Precondition | Input Summary | Expected Output |
|----|---------------|----------|----------|-------------|--------------|---------------|-----------------|
| TC-{{NNN}} | {{TC_NAME}} | Volume | {{PRIORITY}} | {{DESCRIPTION}} | {{PRECONDITION}} | {{INPUT_SUMMARY}} | {{EXPECTED_OUTPUT}} |

---

## 3. Traceability Matrix

| Requirement ID | Requirement Description | TestCase IDs | Coverage Status |
|----------------|-------------------------|--------------|-----------------|
| {{REQ_ID}} | {{REQ_DESCRIPTION}} | {{TC_IDS}} | {{COVERAGE_STATUS}} |

<!-- Coverage Status: ✅ Full | ⚠️ Partial | ❌ Not Covered -->

---

## 4. Decision Table Reference

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|--------------------|--------|--------|--------|--------|
| **Conditions** | | | | |
| {{CONDITION_1}} | {{VALUE}} | {{VALUE}} | {{VALUE}} | {{VALUE}} |
| **Actions** | | | | |
| {{ACTION_1}} | {{VALUE}} | {{VALUE}} | {{VALUE}} | {{VALUE}} |

---

## 5. TestCase Checklist

- [ ] Every requirement maps to at least 1 test case.
- [ ] Every equivalence partition is tested.
- [ ] Every boundary value is evaluated.
- [ ] Negative test cases exist for all error conditions.
- [ ] Priorities assigned correctly.
- [ ] Standard sequential naming naming convention `TC-{NNN}` followed.
- [ ] Preconditions and expected outputs are explicit.
- [ ] Traceability matrix coverage is complete (all statuses are ✅).
