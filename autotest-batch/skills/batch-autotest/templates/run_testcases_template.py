#!/usr/bin/env python3
"""
run_testcases_template.py
-------------------------
Template script for executing batch test cases, validating actual outputs against 
expected results, and exporting execution summaries.

[HOW TO GENERATE]:
This template is read by the AutoTest Agent, populated with batch-specific 
configurations (TABLE_COLUMNS, RUN_COMMAND_TEMPLATE, etc.), and written to 
the local run directory as `run_testcases.py`.
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ==============================================================================
# BATCH SPECIFIC CONFIGURATIONS (Generated Dynamically)
# ==============================================================================
# BATCH_NAME: The logical name of the batch application
BATCH_NAME = "settlement_batch"

# RUN_COMMAND_TEMPLATE: The command to execute the batch, using placeholders for dynamic arguments
# Placeholders: {input_dir}, {output_dir}, {run_id}, {period_start}, {period_end}, {error_threshold}
RUN_COMMAND_TEMPLATE = [
    sys.executable, "-m", "settlement_batch",
    "--input", "{input_dir}",
    "--output", "{output_dir}",
    "--run-id", "{run_id}",
    "--period-start", "{period_start}",
    "--period-end", "{period_end}",
    "--run-at", "2026-06-08T12:00:00Z"
]

# TABLE_COLUMNS: Dictionary defining the column schema for each input CSV table
TABLE_COLUMNS = {
    "users": ["user_id", "name", "country", "signup_date", "status", "kyc_level"],
    "accounts": ["account_id", "user_id", "currency", "account_type", "opened_at", "status"],
    "transactions": ["txn_id", "account_id", "merchant_id", "gross_amount", "currency", "txn_type", "original_txn_id", "txn_timestamp", "status", "promo_code"],
    "merchants": ["merchant_id", "merchant_name", "category_code", "country", "risk_level"],
    "exchange_rates": ["currency", "rate_to_usd", "effective_from", "effective_to"],
    "fee_schedule": ["category_code", "tier_name", "fee_percent", "fixed_fee_usd", "min_fee_usd", "max_fee_usd"],
    "loyalty_tiers": ["tier_name", "min_qualifying_spend_usd", "fee_discount_percent"],
    "promotions": ["promo_code", "discount_percent", "max_discount_usd", "valid_from", "valid_to", "min_txn_usd", "applicable_category"]
}

# SPECIAL_HANDLERS: Dict defining custom behaviors for specific testcase IDs (e.g., column mutations, idempotency)
SPECIAL_HANDLERS = {
    "TC-040": {
        "type": "mutate_columns",
        "table": "transactions",
        "remove_last_n_columns": 2
    },
    "TC-050": {
        "type": "idempotency_check"
    },
    "TC-052": {
        "type": "override_threshold",
        "param": "--error-threshold",
        "value": 0.25
    }
}

# EXPECTED_ERRORS: Keywords to verify batch-level errors
EXPECTED_ERRORS = {
    "encoding_error": ["decode", "encoding", "unicode", "invalid byte"],
    "empty_master": ["empty", "missing", "not found", "exchange_rates", "dimension", "master"],
    "exceed_error_threshold": ["error rate", "threshold", "exceeds", "fraction"]
}

# EXPECTED_RECORD_ERRORS: Keywords in error logs (e.g., errors.jsonl) to match with expected row-level rejection reasons
EXPECTED_RECORD_ERRORS = {
    "missing_rate": ["fx_gap", "gap", "unknown_currency", "exchange rate"],
    "overlap_rate": ["overlap", "overlapping"],
    "missing_fee_schedule": ["fee_schedule_missing", "fee_schedule", "no fee schedule"],
    "bad_promo_code": ["promo_unknown", "promo", "invalid promo"],
    "refund_missing_original": ["refund_orphan", "original transaction", "not found"],
    "refund_exceeds_original": ["exceeds", "original amount"]
}


# ==============================================================================
# UTILITY AND EXECUTION LOGIC (Generic)
# ==============================================================================
def setup_csv_files(input_dir: Path, tc_data: dict, mutate_cols_info: dict | None, encoding: str):
    """Generate CSV input files from TestCase JSON data."""
    input_dir.mkdir(parents=True, exist_ok=True)
    
    for table_name, columns in TABLE_COLUMNS.items():
        filepath = input_dir / f"{table_name}.csv"
        records = tc_data.get(table_name, [])
        
        with open(filepath, "w", encoding=encoding, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            
            for idx, r in enumerate(records):
                # Apply column mutation handler if configured for this testcase and table
                if mutate_cols_info and mutate_cols_info.get("table") == table_name and idx == 0:
                    remove_n = mutate_cols_info.get("remove_last_n_columns", 0)
                    cols_to_write = columns[:-remove_n] if remove_n > 0 else columns
                    row_vals = [r.get(col) for col in cols_to_write]
                    row_vals = ["" if v is None else v for v in row_vals]
                    writer.writerow(row_vals)
                else:
                    row_vals = [r.get(col) for col in columns]
                    row_vals = ["" if v is None else v for v in row_vals]
                    writer.writerow(row_vals)


def calculate_period(transactions: list) -> tuple[str, str]:
    """Dynamically compute batch period based on timestamps in transactions."""
    timestamps = []
    for txn in transactions:
        ts_str = txn.get("txn_timestamp")
        if ts_str:
            try:
                # Replace 'Z' with UTC offset to support ISO parsing
                dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                timestamps.append(dt)
            except ValueError:
                pass
    if timestamps:
        min_ts = min(timestamps)
        max_ts = max(timestamps)
        period_start = min_ts.replace(hour=0, minute=0, second=0, microsecond=0)
        period_end = (max_ts + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return period_start.strftime("%Y-%m-%dT%H:%M:%SZ"), period_end.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # Default fallback period
        return "2026-06-08T00:00:00Z", "2026-06-09T00:00:00Z"


def run_batch(input_dir: Path, output_dir: Path, run_id: str, p_start: str, p_end: str, extra_args: list[str]) -> tuple[int, dict | None, str]:
    """Execute the batch process using command line parameters."""
    # Build execution command from template
    cmd = []
    for item in RUN_COMMAND_TEMPLATE:
        val = item.format(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            run_id=run_id,
            period_start=p_start,
            period_end=p_end
        )
        cmd.append(val)
        
    cmd.extend(extra_args)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    stdout_json = None
    if result.stdout.strip():
        try:
            # Parse the last valid JSON block outputted by the batch process
            lines = result.stdout.strip().splitlines()
            for line in reversed(lines):
                if line.strip().startswith("{") and line.strip().endswith("}"):
                    stdout_json = json.loads(line)
                    break
            if not stdout_json:
                stdout_json = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
            
    return result.returncode, stdout_json, result.stderr


def verify_results(tc_id: str, returncode: int, stdout_json: dict | None, output_dir: Path, expected: dict) -> tuple[str, str]:
    """Evaluate batch output outcomes against expected SPEC constraints."""
    exp_status = expected.get("status")
    exp_action = expected.get("action")
    exp_error_code = expected.get("error_code")
    
    batch_status = stdout_json.get("status") if stdout_json else "UNKNOWN"
    batch_err = stdout_json.get("error", "") if stdout_json else ""
    
    # 1. Batch-Level Error expected
    if exp_status == "ERROR":
        if returncode != 0:
            if not batch_err:
                batch_err = "Process crashed or returned non-zero code."
            
            # Check expected error keywords
            keywords = EXPECTED_ERRORS.get(exp_error_code, [])
            if not keywords:
                # If no specific mapping, pass as long as batch failed
                return "✅ PASS", f"Batch failed as expected. Error: {batch_err}"
                
            matched = any(kw.lower() in batch_err.lower() for kw in keywords)
            if matched:
                return "✅ PASS", f"Batch failed as expected with matching error code ({exp_error_code}). Error: {batch_err}"
            else:
                return "❌ FAIL", f"Batch failed, but error did not match expected keywords for '{exp_error_code}'. Error details: {batch_err}"
        else:
            return "❌ FAIL", f"Expected batch-level failure (ERROR), but batch completed successfully (code: {returncode})."
            
    # 2. Batch-Level Success expected
    if returncode != 0 or batch_status != "SUCCESS":
        return "❌ FAIL", f"Batch execution failed (exit code: {returncode}, status: {batch_status}). StdErr: {batch_err}"
        
    summary_path = output_dir / f"RUN_{tc_id}" / "settlement_summary.csv"
    errors_path = output_dir / f"RUN_{tc_id}.errors.jsonl"
    
    # A. Case expected to insert data into DB/Summary
    if exp_action == "INSERT_DB":
        if not summary_path.exists():
            return "❌ FAIL", "Output summary CSV file does not exist."
            
        with open(summary_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        if len(rows) == 0:
            return "❌ FAIL", "Output summary CSV is empty."
            
        return "✅ PASS", f"Settlement summary successfully created. Output row count: {len(rows)}"
        
    # B. Case expected to skip (row rejection or filtering)
    elif exp_action == "SKIP":
        if exp_status == "REJECTED":
            # Business logic rejection - check errors.jsonl
            if not errors_path.exists():
                # Fallback search in parent output directory
                possible_paths = list(output_dir.glob("*.errors.jsonl"))
                if possible_paths:
                    errors_path = possible_paths[0]
                    
            if not errors_path.exists() or os.path.getsize(errors_path) == 0:
                return "❌ FAIL", "Expected row-level rejection, but errors.jsonl is missing or empty."
                
            # Search for expected error reason keywords inside error logs
            has_error = False
            error_reason = ""
            with open(errors_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        err_rec = json.loads(line)
                        reason = err_rec.get("reason", "")
                        
                        keywords = EXPECTED_RECORD_ERRORS.get(exp_error_code, [])
                        if keywords:
                            matched = any(kw.lower() in reason.lower() for kw in keywords)
                            if matched:
                                has_error = True
                                error_reason = reason
                                break
                        else:
                            # Fallback if no specific expected error mapping is found
                            has_error = True
                            error_reason = reason
                            break
                    except json.JSONDecodeError:
                        pass
                        
            if has_error:
                return "✅ PASS", f"Transaction rejected and logged correctly. Reason: {error_reason}"
            else:
                return "❌ FAIL", f"Rejection error reason does not match expected code ({exp_error_code}) in error logs."
                
        elif exp_status == "APPROVED":
            # Filtering due to KYC=0 or Frozen accounts (exclude without logging error)
            if summary_path.exists():
                with open(summary_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                active_rows = [r for r in rows if float(r.get("gross_settled_usd", "0")) > 0]
                if len(active_rows) == 0:
                    return "✅ PASS", "Transactions successfully excluded from settlement (gross_settled_usd is 0)."
                else:
                    return "❌ FAIL", "Transactions that should be excluded were included in the summary."
            else:
                return "✅ PASS", "Summary file not created or empty, which matches expectations."
                
    return "✅ PASS", "Execution status matches expectations."


def main():
    parser = argparse.ArgumentParser(description="Batch AutoTest Runner")
    parser.add_argument("--tc-ids", required=True, help="Test cases to run (comma-separated, or 'all')")
    parser.add_argument("--run-dir", required=True, help="Target directory for running tests and outputs")
    parser.add_argument("--testdata-json", required=True, help="Path to testdata JSON file")
    args = parser.parse_args()
    
    run_dir = Path(args.run_dir)
    testdata_path = Path(args.testdata_json)
    
    if not testdata_path.exists():
        print(f"Error: {testdata_path} not found")
        sys.exit(1)
        
    with open(testdata_path, "r", encoding="utf-8") as f:
        all_tc_data = json.load(f)
        
    tc_ids_to_run = []
    if args.tc_ids.lower() == "all":
        tc_ids_to_run = [tc["testcase_id"] for tc in all_tc_data]
    else:
        tc_ids_to_run = [t.strip() for t in args.tc_ids.split(",") if t.strip()]
        
    results = []
    
    for tc_id in tc_ids_to_run:
        tc_item = next((tc for tc in all_tc_data if tc["testcase_id"] == tc_id), None)
        if not tc_item:
            print(f"⚠️ Warning: TestCase {tc_id} not found in test data.")
            continue
            
        print(f"▶️ Running {tc_id}: {tc_item.get('description')} ...")
        
        tc_input_data = tc_item["input"]
        expected = tc_item.get("expected_output", {})
        
        # Check special handlers configured for this test case
        handler = SPECIAL_HANDLERS.get(tc_id)
        
        # Handling CSV Column mutation
        mutate_cols_info = None
        if handler and handler.get("type") == "mutate_columns":
            mutate_cols_info = handler
            
        # Encoding check
        invalid_encoding = tc_input_data.get("invalid_encoding", "UTF8")
        encoding = "shift_jis" if invalid_encoding == "SJIS" else "utf-8-sig"
        
        # Prepare execution input and output paths
        tc_run_dir = run_dir / tc_id
        input_dir = tc_run_dir / "input"
        output_dir = tc_run_dir / "output"
        
        if tc_run_dir.exists():
            shutil.rmtree(tc_run_dir)
            
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup input CSVs
        setup_csv_files(input_dir, tc_input_data, mutate_cols_info, encoding)
        
        # Compute dates
        p_start, p_end = calculate_period(tc_input_data.get("transactions", []))
        
        run_id = f"RUN_{tc_id}"
        
        # Dynamic execution argument overrides
        extra_args = []
        error_threshold_val = 1.0
        if handler and handler.get("type") == "override_threshold":
            error_threshold_val = handler.get("value")
        extra_args.extend(["--error-threshold", str(error_threshold_val)])
            
        # Handle Idempotency verification
        if handler and handler.get("type") == "idempotency_check":
            # Execution 1
            code1, stdout1, stderr1 = run_batch(input_dir, output_dir, run_id, p_start, p_end, extra_args)
            summary_path = output_dir / run_id / "settlement_summary.csv"
            
            if code1 != 0 or not summary_path.exists():
                status, detail = "❌ FAIL", f"First execution of idempotency test failed. Error: {stderr1}"
            else:
                with open(summary_path, "r", encoding="utf-8") as f:
                    csv_content1 = f.read()
                    
                # Execution 2 (Re-execution)
                code2, stdout2, stderr2 = run_batch(input_dir, output_dir, run_id, p_start, p_end, extra_args)
                
                if code2 != 0 or not summary_path.exists():
                    status, detail = "❌ FAIL", f"Second execution of idempotency test failed. Error: {stderr2}"
                else:
                    with open(summary_path, "r", encoding="utf-8") as f:
                        csv_content2 = f.read()
                        
                    if csv_content1 == csv_content2:
                        status, detail = "✅ PASS", "Idempotency guaranteed (re-run yielded identical summary CSV)."
                    else:
                        status, detail = "❌ FAIL", "Idempotency violated (re-run outputs differed or duplicated)."
        else:
            # Regular execution
            code, stdout, stderr = run_batch(input_dir, output_dir, run_id, p_start, p_end, extra_args)
            status, detail = verify_results(tc_id, code, stdout, output_dir, expected)
            
        print(f"  Result: {status} | Detail: {detail}")
        results.append({
            "testcase_id": tc_id,
            "status": status,
            "detail": detail
        })
        
    print("\n=== TEST_EXECUTION_JSON_SUMMARY ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
