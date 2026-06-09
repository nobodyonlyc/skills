# Test Report - {{BATCH_NAME}}

> **Batch Name:** {{BATCH_NAME}}
> **Batch Code:** {{BATCH_CODE}}
> **SPEC Version:** {{SPEC_VERSION}}
> **Execution Date:** {{EXECUTION_DATE}}
> **Environment:** {{ENVIRONMENT}}
> **Executor:** {{EXECUTOR_NAME}}
> **Execution Duration:** {{EXECUTION_DURATION}}

---

## 1. Executive Summary

### 1.1 Overview

| Category | Count | Percentage |
|---|---|---|
| ✅ Passed | {{PASSED_COUNT}} | {{PASSED_PCT}}% |
| ❌ Failed | {{FAILED_COUNT}} | {{FAILED_PCT}}% |
| ⏭️ Skipped | {{SKIPPED_COUNT}} | {{SKIPPED_PCT}}% |
| ⚠️ Blocked | {{BLOCKED_COUNT}} | {{BLOCKED_PCT}}% |
| **Total** | **{{TOTAL_COUNT}}** | **100%** |

### 1.2 Pass Rate

<!-- Visual progress bar. The agent replaces this with the actual rate. -->

```
Pass Rate: {{PASS_RATE}}%
[{{PROGRESS_BAR_FILLED}}{{PROGRESS_BAR_EMPTY}}] {{PASSED_COUNT}}/{{TOTAL_COUNT}}
```

<!-- Example:
Pass Rate: 77.4%
[████████████████████░░░░░░] 24/31
-->

### 1.3 Overall Evaluation

| Criteria | Result | Evaluation |
|---|---|---|
| Pass Rate | {{PASS_RATE}}% | {{PASS_EVALUATION}} |
| Critical Test Pass | {{CRITICAL_PASS_RATE}}% | {{CRITICAL_EVALUATION}} |
| Coverage | {{COVERAGE_PCT}}% | {{COVERAGE_EVALUATION}} |
| Defects Found | {{DEFECTS_COUNT}} | {{DEFECTS_EVALUATION}} |

<!-- Evaluation: ✅ Passed (≥ 95%) | ⚠️ Review Required (80-94%) | ❌ Failed (< 80%) -->

---

## 2. Detailed Results

<!-- Lists the results of each testcase. Status: ✅ PASS | ❌ FAIL | ⏭️ SKIP | ⚠️ BLOCKED -->

| ID | TestCase Name | Status | Input | Expected Output | Actual Output | Error |
|---|---|---|---|---|---|---|
| TC-{{NNN}} | {{TC_NAME}} | {{STATUS}} | {{INPUT_SUMMARY}} | {{EXPECTED}} | {{ACTUAL}} | {{ERROR}} |
| TC-{{NNN}} | {{TC_NAME}} | {{STATUS}} | {{INPUT_SUMMARY}} | {{EXPECTED}} | {{ACTUAL}} | {{ERROR}} |
| TC-{{NNN}} | {{TC_NAME}} | {{STATUS}} | {{INPUT_SUMMARY}} | {{EXPECTED}} | {{ACTUAL}} | {{ERROR}} |

<!-- Repeat for all testcases. The "Error" column should only be filled when Status = FAIL. -->

---

## 3. Failed TestCases Analysis

<!-- Detailed analysis for each failed testcase. Each testcase should include: root cause, SPEC reference, and recommended fixes. -->

{{FAILED_TC_ANALYSIS_START}}

### 3.{{N}} {{TC_ID}} - {{TC_NAME}}

| Category | Detail |
|---|---|
| **TestCase ID** | {{TC_ID}} |
| **TestCase Name** | {{TC_NAME}} |
| **Category** | {{TC_CATEGORY}} |
| **Priority** | {{TC_PRIORITY}} |
| **Input** | {{TC_INPUT}} |
| **Expected Output** | {{TC_EXPECTED}} |
| **Actual Output** | {{TC_ACTUAL}} |
| **Root Cause** | {{ROOT_CAUSE}} |
| **SPEC Reference** | {{SPEC_REFERENCE}} |
| **Severity** | {{SEVERITY}} |
| **Recommended Fix** | {{RECOMMENDATION}} |
| **Impact** | {{IMPACT}} |

{{FAILED_TC_ANALYSIS_END}}

<!-- Repeat the block above for each failed testcase. -->

---

## 4. Coverage Matrix

<!-- Maps each requirement in the SPEC to testcases and outcomes. -->

| SPEC Requirement | Description | TestCase IDs | Status |
|---|---|---|---|
| {{REQ_ID}} | {{REQ_DESC}} | {{TC_IDS}} | {{STATUS}} |
| {{REQ_ID}} | {{REQ_DESC}} | {{TC_IDS}} | {{STATUS}} |
| {{REQ_ID}} | {{REQ_DESC}} | {{TC_IDS}} | {{STATUS}} |
| {{REQ_ID}} | {{REQ_DESC}} | {{TC_IDS}} | {{STATUS}} |
| {{REQ_ID}} | {{REQ_DESC}} | {{TC_IDS}} | {{STATUS}} |

<!-- Status:
  ✅ COVERED - All TCs passed
  ⚠️ PARTIAL - Some TCs failed
  ❌ FAILED - All TCs failed
  ⏭️ NOT TESTED - No TCs defined or skipped
-->

### 4.1 Coverage Summary

| Status | Requirement Count | Percentage |
|---|---|---|
| ✅ COVERED | {{COVERED_COUNT}} | {{COVERED_PCT}}% |
| ⚠️ PARTIAL | {{PARTIAL_COUNT}} | {{PARTIAL_PCT}}% |
| ❌ FAILED | {{FAILED_REQ_COUNT}} | {{FAILED_REQ_PCT}}% |
| ⏭️ NOT TESTED | {{NOT_TESTED_COUNT}} | {{NOT_TESTED_PCT}}% |
| **Total** | **{{TOTAL_REQ_COUNT}}** | **100%** |

---

## 5. Statistics

### 5.1 Statistics by TestCase Category

| Category | Total | Passed | Failed | Skipped | Pass Rate |
|---|---|---|---|---|---|
| Normal | {{N_TOTAL}} | {{N_PASS}} | {{N_FAIL}} | {{N_SKIP}} | {{N_RATE}}% |
| Boundary | {{B_TOTAL}} | {{B_PASS}} | {{B_FAIL}} | {{B_SKIP}} | {{B_RATE}}% |
| Negative | {{NEG_TOTAL}} | {{NEG_PASS}} | {{NEG_FAIL}} | {{NEG_SKIP}} | {{NEG_RATE}}% |
| Edge Case | {{E_TOTAL}} | {{E_PASS}} | {{E_FAIL}} | {{E_SKIP}} | {{E_RATE}}% |
| Decision Table | {{D_TOTAL}} | {{D_PASS}} | {{D_FAIL}} | {{D_SKIP}} | {{D_RATE}}% |
| Volume | {{V_TOTAL}} | {{V_PASS}} | {{V_FAIL}} | {{V_SKIP}} | {{V_RATE}}% |
| **Total** | **{{TOTAL}}** | **{{T_PASS}}** | **{{T_FAIL}}** | **{{T_SKIP}}** | **{{T_RATE}}%** |

### 5.2 Statistics by Priority

| Priority | Total | Passed | Failed | Skipped | Pass Rate |
|---|---|---|---|---|---|
| Critical | {{C_TOTAL}} | {{C_PASS}} | {{C_FAIL}} | {{C_SKIP}} | {{C_RATE}}% |
| High | {{H_TOTAL}} | {{H_PASS}} | {{H_FAIL}} | {{H_SKIP}} | {{H_RATE}}% |
| Medium | {{M_TOTAL}} | {{M_PASS}} | {{M_FAIL}} | {{M_SKIP}} | {{M_RATE}}% |
| Low | {{L_TOTAL}} | {{L_PASS}} | {{L_FAIL}} | {{L_SKIP}} | {{L_RATE}}% |
| **Total** | **{{TOTAL}}** | **{{T_PASS}}** | **{{T_FAIL}}** | **{{T_SKIP}}** | **{{T_RATE}}%** |

### 5.3 Defect Allocation

| Defect ID | TestCase ID | Type | Severity | Description | Status |
|---|---|---|---|---|---|
| DEF-{{NNN}} | TC-{{NNN}} | {{DEFECT_TYPE}} | {{SEVERITY}} | {{DEFECT_DESC}} | {{DEFECT_STATUS}} |
| DEF-{{NNN}} | TC-{{NNN}} | {{DEFECT_TYPE}} | {{SEVERITY}} | {{DEFECT_DESC}} | {{DEFECT_STATUS}} |

<!-- Severity: Critical | Major | Minor | Trivial -->
<!-- Status: Open | In Progress | Fixed | Closed | Deferred -->

---

## 6. Performance

| Metric | Value | Allowed Threshold | Evaluation |
|---|---|---|---|
| Average processing time/record | {{AVG_TIME}} ms | {{THRESHOLD}} ms | {{EVALUATION}} |
| Total execution time | {{TOTAL_TIME}} s | {{THRESHOLD}} s | {{EVALUATION}} |
| Max memory usage | {{MAX_MEMORY}} MB | {{THRESHOLD}} MB | {{EVALUATION}} |
| Throughput | {{THROUGHPUT}} records/s | {{THRESHOLD}} records/s | {{EVALUATION}} |

---

## 7. Conclusions and Recommendations

### 7.1 Conclusion

{{CONCLUSION}}

<!-- Summary of test results, evaluation of batch quality, and main issues discovered. -->

### 7.2 Recommendations

<!-- List of recommendations to improve performance, sorted by priority. -->

| No. | Recommendation | Priority | Related TestCase IDs |
|---|---|---|---|
| 1 | {{RECOMMENDATION_1}} | {{PRIORITY}} | {{RELATED_TC_IDS}} |
| 2 | {{RECOMMENDATION_2}} | {{PRIORITY}} | {{RELATED_TC_IDS}} |
| 3 | {{RECOMMENDATION_3}} | {{PRIORITY}} | {{RELATED_TC_IDS}} |

### 7.3 Next Decisions

- [ ] Fix all defects with Critical/Major severity before deployment
- [ ] Run regression tests after fixing defects
- [ ] Review and update SPEC if necessary
- [ ] Approve deployment to {{TARGET_ENVIRONMENT}}

---

## 8. Appendix

### 8.1 Test Environment Information

| Category | Value |
|---|---|
| Server | {{SERVER_INFO}} |
| Database | {{DB_INFO}} |
| OS | {{OS_INFO}} |
| Batch Version | {{BATCH_VERSION}} |
| Config | {{CONFIG_INFO}} |

### 8.2 Related Files

| File | Description | Path |
|---|---|---|
| SPEC Analysis | SPEC analysis report | {{SPEC_ANALYSIS_PATH}} |
| TestCase Document | List of testcases | {{TESTCASE_PATH}} |
| Test Data | Test data file | {{TESTDATA_PATH}} |
| Execution Log | Execution log | {{EXECUTION_LOG_PATH}} |
| Error Log | Error log | {{ERROR_LOG_PATH}} |

---

> **Note:** This template is used by the agent in Phase 5 (Report Generation) of the Batch AutoTest workflow. The agent needs to fill in all `{{...}}` placeholders with the actual results from Phase 4 (Test Execution). All testcases must have results. Every failed testcase must have a detailed analysis in Section 3.
