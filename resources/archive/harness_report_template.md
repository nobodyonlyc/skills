# Harness Task Execution Report

* **Date**: {{DATE}}
* **Feature ID**: {{FEATURE_ID}} - {{FEATURE_TITLE}}
* **Execution Status**:  **SUCCESS** | ❌ **FAILED**
* **Assigned Agent**: {{AGENT_NAME}}

---

## 1. Executive Summary
Provide a 2-3 sentence high-level overview of what this task achieved and whether it met the acceptance criteria.

## 2. Verification Outcomes
Detail the verification steps executed and their outputs:
```bash
# Example verification command
./harness verify {{FEATURE_ID}}
```

### Checks Status Table:
| Verification Step | Command / Script | Result | Output Snippet / Error Logs |
| :--- | :--- | :--- | :--- |
| Step 1 | `cargo check` |  PASS | Complies without errors |
| Step 2 | `cargo test` |  PASS | 12 tests passed |
| Step 3 | `[ -f config.json ]` | ❌ FAIL | File not found |

> [!WARNING]
> If any check failed, detail the remediation steps taken to correct the code.

## 3. Code Modifications
List the exact files created, modified, or deleted during this task:
* ➕ `Created`: `src/auth/gate.rs`
* 📝 `Modified`: `src/main.rs`
* ❌ `Deleted`: `src/temp_auth.rs`

### Code Diff Snippets (Crucial Changes):
```diff
-old_broken_logic()
+new_robust_logic()
```

## 4. Tests Added / Executed
List the test cases written to ensure zero regression:
1. `should_reject_invalid_emails`: Asserts HTTP 400 when malformed email payload is passed.
2. `should_allow_valid_auth_tokens`: Asserts HTTP 200 with correct JWT header.

## 5. Telemetry & Performance Audit
* **Execution Duration**: {{DURATION}} seconds
* **CPU / Memory Impact**: (If relevant, e.g., "Max memory footprint stayed below 50MB during batch streaming")
* **Resource Leak Audit**: Confirmed all DB connection pools and file descriptors were closed.

## 6. Next Steps & Handoff Info
List dependent tasks or unresolved items deferred to the next session:
* [ ] Integrate current auth endpoint with frontend (Feature FXX)
* [ ] Set up production DB migrations
