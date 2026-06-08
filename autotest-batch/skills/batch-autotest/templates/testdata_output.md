# Test Data Structure - {{BATCH_NAME}}

> **Batch Name:** {{BATCH_NAME}}
> **Batch Code:** {{BATCH_CODE}}
> **SPEC Version:** {{SPEC_VERSION}}
> **Generation Date:** {{GENERATION_DATE}}
> **Creator:** {{GENERATOR_NAME}}
> **TestCase Reference:** {{TESTCASE_REF}}
> **Data File Path:** {{DATA_FILE_PATH}}

---

## 1. Introduction

This document describes the structure of the test data generated for batch **{{BATCH_NAME}}**. The test data is stored in JSON format and is used in Phase 4 (Test Execution) of the Batch AutoTest workflow.

Each entry in the JSON file corresponds to one testcase and contains the complete inputs and expected outputs so that the agent can execute tests and verify results automatically.

---

## 2. JSON Schema - Single Test Data Entry

<!-- Schema for a single entry in the test data array. The Agent MUST follow this schema when generating data. -->

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TestDataEntry",
  "description": "Schema for a single test data entry",
  "type": "object",
  "required": ["testcase_id", "description", "input", "expected_output"],
  "properties": {
    "testcase_id": {
      "type": "string",
      "pattern": "^TC-[0-9]{3}$",
      "description": "The ID of the corresponding testcase, in the format TC-{NNN}"
    },
    "data_set_id": {
      "type": "string",
      "pattern": "^DS-[0-9]{3}$",
      "description": "The ID of the dataset (if a testcase has multiple datasets)"
    },
    "description": {
      "type": "string",
      "description": "A brief description of this test data"
    },
    "category": {
      "type": "string",
      "enum": ["Normal", "Boundary", "Invalid", "Edge Case", "Volume", "Combination"],
      "description": "Category of test data"
    },
    "input": {
      "type": "object",
      "description": "Input data for the testcase",
      "properties": {
        "csv_line": {
          "type": "string",
          "description": "Input CSV line (if the batch processes CSV)"
        },
        "line_number": {
          "type": "integer",
          "description": "Line number in the file (starting from 1 for header, 2 for data)"
        },
        "file_path": {
          "type": "string",
          "description": "Input file path (if needed)"
        },
        "additional_params": {
          "type": "object",
          "description": "Other additional parameters depending on the batch"
        }
      }
    },
    "expected_output": {
      "type": "object",
      "description": "Expected outcome after processing",
      "required": ["status", "action"],
      "properties": {
        "status": {
          "type": "string",
          "enum": ["SUCCESS", "ERROR", "SKIP", "WARNING"],
          "description": "Expected processing status"
        },
        "action": {
          "type": "string",
          "enum": ["INSERT_DB", "UPDATE_DB", "SKIP", "LOG_ERROR", "ABORT"],
          "description": "Expected system action"
        },
        "record": {
          "type": "object",
          "description": "Record written to the DB (if status = SUCCESS)"
        },
        "error_message": {
          "type": "string",
          "description": "Expected error message (if status = ERROR)"
        },
        "error_field": {
          "type": "string",
          "description": "The field that caused the error (if status = ERROR)"
        },
        "error_code": {
          "type": "string",
          "description": "Error code (if applicable)"
        }
      }
    },
    "setup": {
      "type": "object",
      "description": "Data setup required before running the testcase (e.g., seeding DB)",
      "properties": {
        "db_records": {
          "type": "array",
          "description": "Records to insert into DB before testing"
        },
        "files": {
          "type": "array",
          "description": "Files to create before testing"
        }
      }
    },
    "teardown": {
      "type": "object",
      "description": "Cleanup actions to perform after running the testcase",
      "properties": {
        "delete_records": {
          "type": "boolean",
          "description": "Whether to delete the inserted records"
        },
        "delete_files": {
          "type": "boolean",
          "description": "Whether to delete the created files"
        }
      }
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Tags to classify and filter the testcases"
    }
  }
}
```

---

## 3. JSON Schema - Complete Test Data File

<!-- Schema for the entire test data file (array of entries). -->

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TestDataFile",
  "description": "Schema for the complete test data file",
  "type": "array",
  "minItems": 1,
  "items": {
    "$ref": "#/definitions/TestDataEntry"
  },
  "definitions": {
    "TestDataEntry": {
      "type": "object",
      "required": ["testcase_id", "description", "input", "expected_output"],
      "properties": {
        "testcase_id": { "type": "string", "pattern": "^TC-[0-9]{3}$" },
        "data_set_id": { "type": "string", "pattern": "^DS-[0-9]{3}$" },
        "description": { "type": "string" },
        "category": {
          "type": "string",
          "enum": ["Normal", "Boundary", "Invalid", "Edge Case", "Volume", "Combination"]
        },
        "input": { "type": "object" },
        "expected_output": {
          "type": "object",
          "required": ["status", "action"]
        },
        "setup": { "type": "object" },
        "teardown": { "type": "object" },
        "tags": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

---

## 4. Test Data Examples

### 4.1 Example - Valid Data (Normal)

```json
{
  "testcase_id": "TC-001",
  "data_set_id": "DS-001",
  "description": "Valid record with all fields populated",
  "category": "Normal",
  "input": {
    "csv_line": "{{VALID_CSV_LINE}}",
    "line_number": 2
  },
  "expected_output": {
    "status": "SUCCESS",
    "action": "INSERT_DB",
    "record": {
      "{{FIELD_1}}": "{{VALUE_1}}",
      "{{FIELD_2}}": "{{VALUE_2}}"
    }
  },
  "tags": ["normal", "valid", "all-fields"]
}
```

### 4.2 Example - Boundary Data (Boundary)

```json
{
  "testcase_id": "TC-006",
  "data_set_id": "DS-006",
  "description": "Minimum boundary value for {{FIELD_NAME}}",
  "category": "Boundary",
  "input": {
    "csv_line": "{{BOUNDARY_CSV_LINE}}",
    "line_number": 2
  },
  "expected_output": {
    "status": "SUCCESS",
    "action": "INSERT_DB",
    "record": {
      "{{FIELD_NAME}}": "{{MIN_VALUE}}"
    }
  },
  "tags": ["boundary", "min-value", "{{FIELD_NAME}}"]
}
```

### 4.3 Example - Invalid Data (Invalid)

```json
{
  "testcase_id": "TC-014",
  "data_set_id": "DS-014",
  "description": "Missing {{FIELD_NAME}} (null/empty)",
  "category": "Invalid",
  "input": {
    "csv_line": "{{INVALID_CSV_LINE}}",
    "line_number": 2
  },
  "expected_output": {
    "status": "ERROR",
    "action": "SKIP",
    "error_message": "{{EXPECTED_ERROR_MESSAGE}}",
    "error_field": "{{ERROR_FIELD}}",
    "error_code": "{{ERROR_CODE}}"
  },
  "tags": ["invalid", "null-field", "{{FIELD_NAME}}"]
}
```

### 4.4 Example - Special Cases (Edge Case)

```json
{
  "testcase_id": "TC-024",
  "data_set_id": "DS-024",
  "description": "Data contains Unicode characters",
  "category": "Edge Case",
  "input": {
    "csv_line": "{{UNICODE_CSV_LINE}}",
    "line_number": 2
  },
  "expected_output": {
    "status": "{{SUCCESS_OR_ERROR}}",
    "action": "{{EXPECTED_ACTION}}",
    "record": "{{IF_SUCCESS}}"
  },
  "tags": ["edge-case", "unicode", "special-chars"]
}
```

---

## 5. Test Data Coverage Summary

<!-- Statistical summary of data set count per category. Each category should have at least 1 data set. -->

| Data Category | TestCase IDs | Count |
|---|---|---|
| Normal | {{NORMAL_TC_IDS}} | {{NORMAL_COUNT}} |
| Boundary | {{BOUNDARY_TC_IDS}} | {{BOUNDARY_COUNT}} |
| Invalid | {{INVALID_TC_IDS}} | {{INVALID_COUNT}} |
| Edge Case | {{EDGE_TC_IDS}} | {{EDGE_COUNT}} |
| Volume | {{VOLUME_TC_IDS}} | {{VOLUME_COUNT}} |
| Combination | {{COMBINATION_TC_IDS}} | {{COMBINATION_COUNT}} |
| **Total** | | **{{TOTAL_COUNT}}** |

---

## 6. Test Data Generation Guidelines

### 6.1 General Principles

1. **At least 1 dataset per testcase**: If a testcase has multiple sub-scenarios, create multiple datasets with different `data_set_id`s.
2. **Realistic data**: Use realistic values (proper names, valid emails, etc.).
3. **Isolated data**: Each dataset must be independent and not rely on other datasets.
4. **Reproducible**: Results must be consistent across multiple runs.

### 6.2 Specific Guidelines by Category

| Category | Principle |
|---|---|
| Normal | Fully valid data complying with all constraints in the SPEC |
| Boundary | Exactly at the boundary values (min, max), do NOT use near-boundary values |
| Invalid | Violates **exactly one** constraint, while all other fields remain valid |
| Edge Case | Includes Unicode, injection patterns, special characters, empty inputs |
| Volume | Large volume of data to test performance/limits |
| Combination | Combines multiple conditions, designed using Decision Tables |

---

## 7. Test Data Review Checklist

<!-- The agent MUST complete all items before moving to Phase 4. -->

- [ ] Each testcase has at least one dataset.
- [ ] Valid data fully complies with SPEC constraints.
- [ ] Invalid data violates exactly one constraint (other fields remain valid).
- [ ] Boundary data is exactly at the boundary values (not near the boundaries).
- [ ] Edge case data includes Unicode, injection patterns, special characters.
- [ ] Data is realistic (proper names, valid emails, etc.).
- [ ] Each dataset is independent of others.
- [ ] Expected output is specific and can be verified automatically.
- [ ] Error messages in expected output match the SPEC.
- [ ] JSON file is valid and parses without error.
- [ ] Full coverage: all 6 categories have at least one entry.
- [ ] Setup/teardown is defined if the testcase requires a specific DB state.

---

> **Note:** This template is used by the agent during Phase 3 (Test Data Generation) of the Batch AutoTest workflow. The agent should generate the JSON file according to the schemas in Sections 2 and 3, then fill out the coverage details in Section 5. The JSON file must be valid and conform to the defined schemas.
