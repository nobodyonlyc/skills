# Field-Level Test Checklist and SPEC Filtering Guide

> **Document ID**: REF-FIELD-CHECKLIST  
> **Status**: Approved  
> **Target**: Input Field Validation Verification

---

## 1. 🎯 Purpose

This guide defines the standard **Master Field Checklists** for common data types and explains how to apply **SPEC-based filtering** to construct an **Input Validation Matrix** for each input field.

By analyzing every input field against a standard checklist and filtering out irrelevant scenarios based on SPEC constraints, the Agent ensures 100% field-level coverage and prevents missing boundary or edge-case test cases.

---

## 2. 📋 Master Field Checklists

For every input field, identify its data type (both technical type and batch characteristics) and apply the corresponding checklist below.

### 🏷️ Type: String (Character / Text)
Includes text fields, codes (customer ID, product code), names.
*Technical variations:* Fixed-length (requires space padding) vs Variable-length.
*Japanese environment note (JP1/HULFT):* Shift-JIS/CP932 encoding, full-width vs half-width representation.

| ID | Test Scenario | Description | Expected Classification (Default) |
|---|---|---|---|
| STR-001 | **Null / Missing** | Omit the field entirely from the input | `❌ Invalid` (Error code: Mandatory field) |
| STR-002 | **Empty String** | Field is present but has zero length (`""`). Very important to verify behavior. | `❌ Invalid` (For required fields) |
| STR-003 | **Only Whitespaces** | Field contains only spaces (`"   "`). For fixed-length files, spaces are padding, which might equal empty. Verify if processed as empty or kept as spaces. | `✅ Valid` (If allowed as blank/empty) / `❌ Invalid` |
| STR-004 | **Minimum Length** | Length = 1 character | `✅ Valid` (Happy path) |
| STR-005 | **Normal Length** | Length = $N / 2$ characters | `✅ Valid` (Happy path) |
| STR-006 | **Boundary Max Length** | Length = $N$ characters (Max allowed) | `✅ Valid` (Happy path) |
| STR-007 | **Boundary Max + 1** | Length = $N + 1$ characters (Overshoot) | `❌ Invalid` (Error code: Length exceeded) |
| STR-008 | **Special Characters** | Contains symbols like `@`, `#`, `$`, `%`, `*` | `❌ Invalid` (Unless SPEC allows symbols) |
| STR-009 | **Unicode / Accents** | Contains characters like `Á`, `ệ`, `emoji` | `❌ Invalid` (Unless SPEC allows Unicode) |
| STR-010 | **SQL Injection / XSS** | Contains `' OR '1'='1` or `<script>` | `❌ Invalid` (Should be rejected or sanitized) |
| STR-011 | **Half-width vs Full-width** | Test CP932/Shift-JIS half-width kana (`ｱ`) vs full-width (`ア`). Test behavior when conversion is required. | `✅ Valid` (If encoding is Shift-JIS and allowed) |
| STR-012 | **Japanese Wave Dash / Minus** | Test Japanese wave dash `〜` (U+301C) vs tilde `〜` (U+FF5E), or wave dash `−` (U+FF0D) vs minus `-` (U+002D) to check for CP932/Unicode translation errors. | `✅ Valid` (If system handles encoding conversion correctly) |
| STR-013 | **Control Characters** | Input control characters like Tab, LF, CR, or Null byte (`\x00`) inside the string. | `❌ Invalid` (Should be rejected) |
| STR-014 | **Byte Order Mark (BOM)** | File prefix containing BOM (`EF BB BF` for UTF-8) or string fields starting with BOM. | `❌ Invalid` (If parser doesn't strip it) |

---

### 🔢 Type: Numeric (Integer / Float / Decimal)
*Technical variations:*
* **Integer**: signed vs unsigned.
* **Float / Double**: floating-point (prone to rounding errors, do NOT use for money).
* **Decimal / Numeric**: exact precision (used for financial amounts).
* **Packed Decimal / Zoned Decimal**: legacy COBOL formats (often used in mainframe interfaces).

| ID | Test Scenario | Description | Expected Classification (Default) |
|---|---|---|---|
| NUM-001 | **Null / Missing** | Omit the field entirely from the input | `❌ Invalid` (Error code: Mandatory field) |
| NUM-002 | **Boundary Min - 1** | Value = $Min - 1$ (or $Min - 0.1$ depending on precision) | `❌ Invalid` (Error code: Below minimum) |
| NUM-003 | **Boundary Min** | Value = $Min$ | `✅ Valid` (Happy path) |
| NUM-004 | **Boundary Min + 1** | Value = $Min + 1$ (or $Min + \text{precision}$) | `✅ Valid` (Happy path) |
| NUM-005 | **Normal Value** | Value = Midpoint between $Min$ and $Max$ | `✅ Valid` (Happy path) |
| NUM-006 | **Boundary Max - 1** | Value = $Max - 1$ | `✅ Valid` (Happy path) |
| NUM-007 | **Boundary Max** | Value = $Max$ | `✅ Valid` (Happy path) |
| NUM-008 | **Boundary Max + 1** | Value = $Max + 1$ (Overshoot) | `❌ Invalid` (Error code: Exceeds maximum) |
| NUM-009 | **Zero Value** | Value = 0 (Verify behavior for signed/unsigned) | `❌ Invalid` (If $Min > 0$), else `✅ Valid` |
| NUM-010 | **Negative Value** | Value < 0 (Unsigned fields must reject negative numbers) | `❌ Invalid` (If $Min \ge 0$), else `✅ Valid` |
| NUM-011 | **Integer vs Decimal** | Input decimal value (e.g. `12.34`) in an Integer field | `❌ Invalid` (If field is Integer only) |
| NUM-012 | **Precision Exceeded** | Decimal places = $Precision + 1$ | `❌ Invalid` (Error code: Precision exceeded) |
| NUM-013 | **Floating Point Rounding** | Value like `0.1 + 0.2` (test if system precision errors occur, e.g., `0.30000000000000004`) | `❌ Invalid` (Should be validated or rounded correctly) |
| NUM-014 | **Packed Decimal (COBOL)** | Input malformed packed decimal sign nibble (e.g. invalid C/D/F sign in low nibble) | `❌ Invalid` (Error code: Invalid packed decimal format) |
| NUM-015 | **Zoned Decimal (COBOL)** | Input non-numeric character in zoned decimal representation (e.g. missing high nibble `3` or `F`) | `❌ Invalid` (Error code: Invalid zoned decimal format) |

---

### 📅 Type: Date / DateTime / Timestamp
*Technical variations:*
* **Date**: YYYYMMDD, YYYY/MM/DD, etc.
* **DateTime / Timestamp**: with or without Timezone, millisecond/microsecond precision.

| ID | Test Scenario | Description | Expected Classification (Default) |
|---|---|---|---|
| DAT-001 | **Null / Missing** | Omit the field entirely | `❌ Invalid` (Error code: Mandatory field) |
| DAT-002 | **Wrong Format** | Input format e.g. `DD/MM/YYYY`, `YYYY-MM-DD` | `❌ Invalid` (Error code: Invalid format) |
| DAT-003 | **Non-existent Date** | Input day that does not exist (e.g. `20260230`, `20260631`) | `❌ Invalid` (Error code: Invalid date) |
| DAT-004 | **Non-leap Year Feb 29** | Input `20250229` (2025 is not a leap year) | `❌ Invalid` (Error code: Invalid date) |
| DAT-005 | **Leap Year Feb 29** | Input `20240229` (2024 is a leap year) | `✅ Valid` (Happy path) |
| DAT-006 | **Past/Future Date Boundaries** | Date is in the extreme past/future (e.g. `19000101`, `99991231`) | `✅ Valid` / `❌ Invalid` (Depends on SPEC) |
| DAT-007 | **Timezone Discrepancy** | Input timestamp with different timezones (e.g., UTC vs JST +09:00). Test conversion logic. | `✅ Valid` (If correctly normalized) |
| DAT-008 | **DST Transition** | Test time values during Daylight Saving Time transition boundaries (if applicable). | `✅ Valid` (Should not double-process or skip) |

---

### ⚪ Type: Boolean / Flag
Status flag (0/1, Y/N, true/false).

| ID | Test Scenario | Description | Expected Classification (Default) |
|---|---|---|---|
| BOL-001 | **Null / Missing** | Omit the field entirely | `❌ Invalid` (Error code: Mandatory field) |
| BOL-002 | **Valid True** | Input e.g. `true`, `1`, `Y`, `T` (depending on SPEC format) | `✅ Valid` (Happy path) |
| BOL-003 | **Valid False** | Input e.g. `false`, `0`, `N`, `F` | `✅ Valid` (Happy path) |
| BOL-004 | **Invalid Value** | Input invalid string/number (e.g. `2`, `YES`, `invalid`) | `❌ Invalid` (Error code: Invalid flag) |

---

### 💾 Type: Binary / Null / Blob
Stores binary data or actual NULL value.

| ID | Test Scenario | Description | Expected Classification (Default) |
|---|---|---|---|
| BIN-001 | **Null Value** | Input value is database `NULL` vs empty byte array `0x` | `✅ Valid` (If nullable in DB) / `❌ Invalid` |
| BIN-002 | **Malformed Binary** | Input invalid hex string or corrupted binary payload | `❌ Invalid` (Error code: Corrupted binary) |
| BIN-003 | **Size Overshoot** | Binary payload size exceeds maximum blob capacity | `❌ Invalid` (Error code: Size limit exceeded) |

---

## 3. 🔍 SPEC Filtering and Exclude Mechanism

Do not blindly generate TestCases for every scenario in the Master Checklist. You must filter and adjust them based on the **SPEC rules**.

### Step-by-Step Process:

1. **Map Fields**: List all input fields from SPEC Analysis.
2. **Apply Master Checklist**: Retrieve the master checklist matching the field's data type.
3. **Filter and Customize**:
   - **Re-classify**: If the SPEC says a field is optional, change the classification of `Null/Empty` (STR-001, NUM-001) from `❌ Invalid` to `✅ Valid` (Normal case).
   - **Exclude**: If a checklist scenario is impossible or explicitly contradicted by SPEC, mark it as `Excluded` and document the reason.
     * *Example*: If the SPEC states "field A must contain alphanumeric characters", do not create a separate test case for "Only special characters" as a length-only test; instead, combine format checks.
     * *Example*: If a numeric field has no minimum constraint (can be any negative/positive number), exclude the `Boundary Min - 1` scenario as it has no boundary.
4. **Generate TestCases**: Convert only the active (non-excluded) checklist rows into official TestCases (`TC-xxx`).

---

## 💡 Practical Example

### Field: `amount` (DataType: Numeric, Constraints: $Min = 1$, $Max = 500,000,000$, Required = Yes)

| Master ID | Scenario | SPEC Constraint Check | Decision | Generated TC | Reason / Note |
|---|---|---|---|---|---|
| NUM-001 | Null / Missing | Required = Yes | **Keep (Invalid)** | `TC-050` | Verify error when `amount` is omitted. |
| NUM-002 | Boundary Min - 1 | Value = 0 | **Keep (Invalid)** | `TC-012` | $Min - 1 = 0$. Expected Reject. |
| NUM-003 | Boundary Min | Value = 1 | **Keep (Valid)** | `TC-010` | $Min = 1$. Expected Approve. |
| NUM-004 | Boundary Min + 1 | Value = 2 | **Exclude** | — | Excluded because normal range is covered by `TC-001` (normal amount). |
| NUM-005 | Normal Value | Value = 50,000,000 | **Keep (Valid)** | `TC-001` | Normal transaction amount. |
| NUM-006 | Boundary Max - 1 | Value = 499,999,999 | **Exclude** | — | Excluded as `TC-003` (large amount) and Max boundary are sufficient. |
| NUM-007 | Boundary Max | Value = 500,000,000 | **Keep (Valid)** | `TC-011` | $Max = 500,000,000$. Expected Approve. |
| NUM-008 | Boundary Max + 1 | Value = 500,000,001 | **Keep (Invalid)** | `TC-013` | $Max + 1$. Expected Reject. |
| NUM-009 | Zero Value | Covered by Min-1 | **Exclude** | — | Excluded because $Min - 1 = 0$, duplicate check. |
| NUM-010 | Negative Value | Value = -100 | **Keep (Invalid)** | `TC-014` | Negative number check. Expected Reject. |
| NUM-011 | Integer vs Decimal | Precision = 0 | **Keep (Invalid)** | `TC-015` | Input `10.5` (decimal) is not allowed. |
| NUM-012 | Precision Exceed | Precision = 0 | **Exclude** | — | Excluded, same as NUM-011. |

By documenting this filtering table, you prove to the customer that **every potential boundary has been systematically analyzed, checked, and either mapped to a TestCase or logically excluded**.
