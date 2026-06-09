#!/usr/bin/env python3
"""
validate_testdata.py
--------------------
Programmatically validates test data JSON files against constraints extracted from 
SPEC analysis or raw SPEC documents, driven by a batch-specific configuration file.

This validator enforces the Isolation Principle for negative test cases:
- Positive TCs (expected SUCCESS/APPROVED): All fields must comply with SPEC constraints.
- Negative TCs (expected ERROR/REJECTED): Exactly one field must violate constraints, other fields must be valid.
  (Unless it is a business logic error or combination test case, which are exempted).

Exit codes:
- 0: Validation SUCCESS
- 1: Validation FAILED
"""

import argparse
import json
import re
import sys
from pathlib import Path

def parse_markdown_tables(spec_path: Path):
    """Parses markdown tables in SPEC or SPEC analysis to extract fields and constraints by table."""
    if not spec_path.exists():
        print(f"⚠️ Warning: SPEC file not found at {spec_path}. Performing structural JSON checks only.")
        return None, None

    content = spec_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    fields = {} # table_name -> {field_name -> {required: bool, type: str}}
    constraints = {} # table_name -> {field_name -> {min: val, max: val, format: regex, valid_values: list}}

    table_headers = []
    table_rows = []
    current_table = "default"

    for line in lines:
        line_stripped = line.strip()
        
        # Detect table section heading (e.g., "### 3.1. users (master)" or "## 5. Output Schema")
        match_h3 = re.search(r"###?\s+\d+(?:\.\d+)*\.\s+`?([a-zA-Z_]+)`?", line_stripped)
        if match_h3:
            current_table = match_h3.group(1).strip()
            if current_table not in fields:
                fields[current_table] = {}
            if current_table not in constraints:
                constraints[current_table] = {}

        if line_stripped.startswith("|"):
            # It's a table row
            row = [cell.strip() for cell in line_stripped.split("|")[1:-1]]
            if not table_headers:
                table_headers = row
            elif line_stripped.replace(" ", "").replace("-", "").replace("|", "") == "":
                # It's the header separator line, e.g. |---|---|
                continue
            else:
                table_rows.append(row)
        else:
            # Table ended or not in table
            if table_headers and table_rows:
                # Process the table
                headers_lower = [h.lower().replace("`", "").strip() for h in table_headers]
                
                # Check if it's a fields/constraints table (supporting EN and VN headers)
                if "field" in headers_lower or "field name" in headers_lower or "cột" in headers_lower:
                    idx_name = (headers_lower.index("field") if "field" in headers_lower 
                                else (headers_lower.index("field name") if "field name" in headers_lower 
                                      else headers_lower.index("cột")))
                    idx_req = (headers_lower.index("required") if "required" in headers_lower 
                               else (headers_lower.index("bắt buộc") if "bắt buộc" in headers_lower else -1))
                    idx_type = (headers_lower.index("data type") if "data type" in headers_lower 
                                else (headers_lower.index("type") if "type" in headers_lower 
                                      else (headers_lower.index("kiểu") if "kiểu" in headers_lower else -1)))
                    idx_min = headers_lower.index("min") if "min" in headers_lower else -1
                    idx_max = headers_lower.index("max") if "max" in headers_lower else -1
                    idx_fmt = headers_lower.index("format/pattern") if "format/pattern" in headers_lower else (headers_lower.index("format") if "format" in headers_lower else -1)
                    idx_vals = headers_lower.index("valid values") if "valid values" in headers_lower else -1
                    idx_cons = headers_lower.index("constraints") if "constraints" in headers_lower else -1

                    if current_table not in fields:
                        fields[current_table] = {}
                    if current_table not in constraints:
                        constraints[current_table] = {}

                    for row in table_rows:
                        if len(row) > idx_name:
                            f_name = row[idx_name].strip("`").strip()
                            if not f_name:
                                continue
                            
                            is_req = False
                            if idx_req != -1 and idx_req < len(row):
                                req_val = row[idx_req].lower()
                                is_req = "✅" in req_val or "yes" in req_val or "required" in req_val or "mandatory" in req_val or "true" in req_val
                            
                            # Preserve True required status from previous tables
                            if f_name in fields[current_table] and fields[current_table][f_name]["required"] and not is_req:
                                is_req = True
                            
                            f_type = "String"
                            if idx_type != -1 and idx_type < len(row):
                                f_type = row[idx_type].strip()
                            
                            # Preserve specific types if already parsed
                            if f_name in fields[current_table] and fields[current_table][f_name]["type"] != "String" and f_type == "String":
                                f_type = fields[current_table][f_name]["type"]

                            fields[current_table][f_name] = {"required": is_req, "type": f_type}

                            if f_name not in constraints[current_table]:
                                constraints[current_table][f_name] = {}

                            # Check for text constraints column
                            if idx_cons != -1 and idx_cons < len(row) and row[idx_cons]:
                                cons_str = row[idx_cons].lower()
                                
                                # 1. Check for min/max lengths
                                match_len = re.search(r"(\d+)-(\d+)\s+(?:characters|chars|length)", cons_str)
                                if not match_len:
                                    match_len = re.search(r"length\s+(\d+)-(\d+)", cons_str)
                                if match_len:
                                    constraints[current_table][f_name]["min"] = float(match_len.group(1))
                                    constraints[current_table][f_name]["max"] = float(match_len.group(2))
                                
                                # 2. Check for numeric ranges
                                match_range = re.search(r"(?:from|between)\s+(\d+)\s+(?:to|and)\s+(\d+)", cons_str)
                                if match_range:
                                    constraints[current_table][f_name]["min"] = float(match_range.group(1))
                                    constraints[current_table][f_name]["max"] = float(match_range.group(2))

                                # 3. Check for positive integer or > 0
                                if (">" in cons_str or "positive" in cons_str) and ">=" not in cons_str:
                                    match_gt = re.search(r">\s*(\d+)", cons_str)
                                    if match_gt:
                                        gt_val = float(match_gt.group(1))
                                        constraints[current_table][f_name]["min"] = gt_val + 1 if "int" in f_type.lower() else gt_val
                                    else:
                                        constraints[current_table][f_name]["min"] = 1 if "int" in f_type.lower() else 0.00001

                                # 4. Check for specific whitelists
                                match_oneof = re.search(r"one\s+of:\s*`?([a-z0-9,\s`']+)`?", cons_str)
                                if match_oneof:
                                    constraints[current_table][f_name]["valid_values"] = [v.strip().strip("`").strip("'") for v in match_oneof.group(1).split(",")]

                            if idx_min != -1 and idx_min < len(row) and row[idx_min] and row[idx_min] != "—" and row[idx_min] != "-":
                                try:
                                    constraints[current_table][f_name]["min"] = float(row[idx_min].replace(",", "").strip("`").strip())
                                except ValueError:
                                    pass
                            
                            if idx_max != -1 and idx_max < len(row) and row[idx_max] and row[idx_max] != "—" and row[idx_max] != "-":
                                try:
                                    constraints[current_table][f_name]["max"] = float(row[idx_max].replace(",", "").strip("`").strip())
                                except ValueError:
                                    pass

                            if idx_fmt != -1 and idx_fmt < len(row) and row[idx_fmt] and row[idx_fmt] != "—" and row[idx_fmt] != "-":
                                fmt = row[idx_fmt].strip("`").strip()
                                if fmt and "YYYYMMDD" not in fmt:
                                    constraints[current_table][f_name]["format"] = fmt

                            if idx_vals != -1 and idx_vals < len(row) and row[idx_vals] and row[idx_vals] != "—" and row[idx_vals] != "-":
                                vals = [v.strip().strip('"').strip("'") for v in row[idx_vals].replace("{", "").replace("}", "").split(",")]
                                if vals and vals[0]:
                                    constraints[current_table][f_name]["valid_values"] = vals

                table_headers = []
                table_rows = []
            if not line_stripped.startswith("|"):
                table_headers = []
                table_rows = []

    # Default fallback formatting and checks
    for table_name, table_fields in fields.items():
        for f_name, meta in table_fields.items():
            if "email" in f_name.lower():
                if f_name not in constraints[table_name]:
                    constraints[table_name][f_name] = {}
                constraints[table_name][f_name]["format"] = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if "name" in f_name.lower():
                if f_name not in constraints[table_name]:
                    constraints[table_name][f_name] = {}
                constraints[table_name][f_name]["format"] = r"^.+$"

    return fields, constraints

def validate_field(field_name, value, fields_meta, constraints_meta):
    """Validates a single field value against its constraints. Returns (is_valid, reason)."""
    if value is None or value == "":
        return True, ""

    # Data Type Check
    f_type = fields_meta.get(field_name, {}).get("type", "String").lower()
    if "number" in f_type or "decimal" in f_type or "int" in f_type or "integer" in f_type:
        if isinstance(value, str):
            try:
                float(value.replace(",", ""))
            except ValueError:
                return False, f"Field '{field_name}' data type must be numeric, received string '{value}'"
        elif not isinstance(value, (int, float)) and value is not None:
            return False, f"Field '{field_name}' data type must be numeric, received {type(value)}"
    
    # Field constraints
    c = constraints_meta.get(field_name)
    if not c:
        return True, ""

    val_as_num = None
    if isinstance(value, (int, float)):
        val_as_num = value
    elif isinstance(value, str):
        try:
            val_as_num = float(value.replace(",", ""))
        except ValueError:
            pass

    # Min/Max range
    if val_as_num is not None:
        if "min" in c and val_as_num < c["min"]:
            return False, f"Field '{field_name}' value {val_as_num} is less than min ({c['min']})"
        if "max" in c and val_as_num > c["max"]:
            return False, f"Field '{field_name}' value {val_as_num} is greater than max ({c['max']})"

    # String length
    if isinstance(value, str):
        val_len = len(value)
        if "min" in c and val_len < c["min"]:
            return False, f"Field '{field_name}' length ({val_len}) is less than min length ({c['min']})"
        if "max" in c and val_len > c["max"]:
            return False, f"Field '{field_name}' length ({val_len}) is greater than max length ({c['max']})"

    # Format / Regex
    if isinstance(value, str) and "format" in c:
        regex = c["format"]
        if not regex.startswith("^"):
            regex = "^" + regex + "$"
        try:
            if not re.match(regex, value):
                return False, f"Field '{field_name}' value '{value}' does not match format '{c['format']}'"
        except re.error:
            pass

    # Valid values / Whitelist
    if "valid_values" in c and str(value) not in c["valid_values"]:
        return False, f"Field '{field_name}' value '{value}' is not in whitelist {c['valid_values']}"

    return True, ""

def validate_testdata(testdata_path: Path, spec_path: Path, config_data: dict):
    """Validates the testdata JSON file based on SPEC and batch-specific configurations."""
    if not testdata_path.exists():
        print(f"❌ Error: Testdata file not found at {testdata_path}")
        return False

    try:
        data = json.loads(testdata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Testdata is not a valid JSON. Detail: {e}")
        return False

    testcases = []
    if isinstance(data, list):
        testcases = data
    elif isinstance(data, dict) and "data_sets" in data:
        testcases = data["data_sets"]
    else:
        print("❌ Error: Testdata must be a JSON array or a dict containing a 'data_sets' array.")
        return False

    # 1. Load schemas and constraints from Spec Analysis
    fields_meta, constraints_meta = parse_markdown_tables(spec_path)
    
    # 2. Apply Fallback values from configuration if SPEC parsing returned nothing
    if not fields_meta or "default" in fields_meta:
        fields_meta = config_data.get("fallback_fields", {})
        constraints_meta = config_data.get("fallback_constraints", {})

    # 3. Standardize metadata tables and apply default constraints from configuration
    known_tables = config_data.get("known_tables", [])
    default_constraints = config_data.get("default_constraints", {})
    
    for t in known_tables:
        if t not in fields_meta:
            fields_meta[t] = {}
        if t not in constraints_meta:
            constraints_meta[t] = {}
            
        # Apply default constraints configured for specific tables/fields
        if t in default_constraints:
            for f_name, f_consts in default_constraints[t].items():
                if f_name not in constraints_meta[t]:
                    constraints_meta[t][f_name] = {}
                for k, v in f_consts.items():
                    if k not in constraints_meta[t][f_name]:
                        constraints_meta[t][f_name][k] = v

    errors = []
    logic_error_keywords = config_data.get("logic_error_keywords", [])
    combination_error_keywords = config_data.get("combination_error_keywords", [])

    for idx, tc in enumerate(testcases):
        tc_id = tc.get("testcase_id", f"INDEX-{idx}")
        category = tc.get("category", "NORMAL").upper()
        tc_desc = tc.get("description", "").lower()
        input_data = tc.get("input", {})

        # Structural validation
        for key in ["testcase_id", "description", "category", "input", "expected_output"]:
            if key not in tc:
                errors.append(f"TestCase {tc_id} is missing required key '{key}'")

        if "expected_output" in tc:
            eo = tc["expected_output"]
            if not isinstance(eo, dict) or "status" not in eo:
                errors.append(f"TestCase {tc_id} expected_output must be a dict and contain 'status' key")

        # Constraints validation
        violated_fields = []
        violation_reasons = []

        is_multi_table = any(t in input_data for t in known_tables)

        if is_multi_table:
            # Multi-table validation
            for table_name, records in input_data.items():
                if table_name not in known_tables or not isinstance(records, list):
                    continue
                
                table_fields = fields_meta.get(table_name, {})
                table_constraints = constraints_meta.get(table_name, {})

                for row_idx, record in enumerate(records):
                    # Check required fields in the record
                    for f_name, meta in table_fields.items():
                        if meta["required"]:
                            if f_name not in record or record[f_name] is None or record[f_name] == "":
                                violated_fields.append(f"{table_name}[{row_idx}].{f_name}")
                                violation_reasons.append(f"Required field '{f_name}' in table '{table_name}' row {row_idx} is missing or null")

                    # Check type, range, format constraints
                    for f_name, val in record.items():
                        is_valid, reason = validate_field(f_name, val, table_fields, table_constraints)
                        if not is_valid:
                            violated_fields.append(f"{table_name}[{row_idx}].{f_name}")
                            violation_reasons.append(f"Table '{table_name}' row {row_idx} field '{f_name}': {reason}")
        else:
            # Single-table flat validation (legacy fallback)
            fields_to_check = {}
            if "csv_line" in input_data:
                line = input_data["csv_line"]
                if line is not None:
                    parts = [p.strip() for p in line.split(",")]
                    flat_fields = {}
                    for t_fields in fields_meta.values():
                        flat_fields.update(t_fields)
                    headers = list(flat_fields.keys())
                    for i, part in enumerate(parts):
                        if i < len(headers):
                            val = part
                            if val == "" or val.lower() == "null":
                                val = None
                            fields_to_check[headers[i]] = val
            else:
                fields_to_check = input_data

            flat_fields = {}
            for t_fields in fields_meta.values():
                flat_fields.update(t_fields)
            flat_constraints = {}
            for t_const in constraints_meta.values():
                flat_constraints.update(t_const)

            for f_name, meta in flat_fields.items():
                if meta["required"]:
                    if f_name not in fields_to_check or fields_to_check[f_name] is None:
                        violated_fields.append(f_name)
                        violation_reasons.append(f"Required field '{f_name}' is missing or null")

            for f_name, val in fields_to_check.items():
                is_valid, reason = validate_field(f_name, val, flat_fields, flat_constraints)
                if not is_valid:
                    violated_fields.append(f_name)
                    violation_reasons.append(reason)

        # Enforce the Isolation Principle based on expected_output.status
        is_expected_error = False
        error_code = ""
        if "expected_output" in tc:
            status = str(tc["expected_output"].get("status", "")).upper()
            is_expected_error = "ERROR" in status or "REJECT" in status or "FAIL" in status
            error_code = str(tc["expected_output"].get("error_code", "")).lower()

        # Check if the error is a business logic or cross-row/db state error
        is_logic_or_db_error = any(kw in error_code or kw in tc_desc for kw in logic_error_keywords)
        
        # Check if it is a combination testcase
        is_combination = (
            category == "COMBINATION" or 
            any(kw in tc_desc or kw in error_code for kw in combination_error_keywords) or
            "combination" in [t.lower() for t in tc.get("tags", [])]
        )

        if is_expected_error:
            if is_combination:
                if len(violated_fields) == 0:
                    errors.append(f"❌ COMBINATION TestCase (expected ERROR/REJECTED) {tc_id} ({tc_desc}) violates isolation principle: Data is 100% valid (no fields are invalid).")
            elif is_logic_or_db_error:
                # Business logic errors can have valid fields (0 violations on formatting)
                if len(violated_fields) > 1:
                    errors.append(f"❌ BUSINESS LOGIC TestCase (expected ERROR) {tc_id} ({tc_desc}) violates isolation principle: There are {len(violated_fields)} format-invalid fields simultaneously ({', '.join(violated_fields)}). Detailed errors: {'; '.join(violation_reasons)}")
            else:
                # Negative TC: MUST violate EXACTLY ONE constraint
                if len(violated_fields) == 0:
                    errors.append(f"❌ NEGATIVE TestCase (expected ERROR/REJECTED) {tc_id} ({tc_desc}) violates isolation principle: Data is 100% valid (no fields are invalid).")
                elif len(violated_fields) > 1:
                    errors.append(f"❌ NEGATIVE TestCase (expected ERROR/REJECTED) {tc_id} ({tc_desc}) violates isolation principle: There are {len(violated_fields)} fields invalid simultaneously ({', '.join(violated_fields)}). Detailed errors: {'; '.join(violation_reasons)}")
        else:
            # Positive TC: ALL fields must be valid
            if len(violated_fields) > 0:
                errors.append(f"❌ POSITIVE TestCase (expected SUCCESS/APPROVED) {tc_id} ({tc_desc}) contains invalid fields: {'; '.join(violation_reasons)}")

    if errors:
        print(f"\n❌ Test Data Validation FAILED. Found {len(errors)} errors:")
        for err in errors[:20]: # show first 20 errors
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} other errors.")
        return False
    else:
        print("\n✅ Test Data Validation SUCCESS! Data matches 100% with SPEC constraints and satisfies isolation principles.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Generic Test Data Validator")
    parser.add_argument("--config", "-c", required=True, help="Path to the batch validation JSON configuration file")
    parser.add_argument("--testdata", "-d", required=True, help="Path to the testdata JSON file to validate")
    parser.add_argument("--spec", "-s", help="Path to the SPEC or Spec Analysis file (optional)")
    args = parser.parse_args()

    config_path = Path(args.config)
    testdata_path = Path(args.testdata)
    spec_path = Path(args.spec) if args.spec else Path("1_spec_analysis.md")

    if not config_path.exists():
        print(f"❌ Error: Config file not found at {config_path}")
        sys.exit(1)

    try:
        config_data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Error: Config file is not a valid JSON. Detail: {e}")
        sys.exit(1)

    # Resolve spec relative paths
    if not spec_path.is_absolute() and not spec_path.exists():
        test_spec = testdata_path.parent / spec_path.name
        if test_spec.exists():
            spec_path = test_spec

    success = validate_testdata(testdata_path, spec_path, config_data)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
