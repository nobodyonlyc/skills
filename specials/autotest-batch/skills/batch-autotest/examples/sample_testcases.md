# TestCase List - Batch Import User CSV

> **Batch Name:** Batch Import User CSV
> **Batch Code:** IMP_USER_CSV
> **SPEC Version:** 1.0
> **TestCase Creation Date:** 2026-06-03
> **Creator:** AutoTest Agent
> **Based on SPEC Analysis:** SPEC_ANALYSIS_IMP_USER_CSV_v1.0

---

## 1. TestCase Overview

### 1.1 Statistics by Category

| TestCase Category | Count | Percentage |
|---|---|---|
| Normal | 5 | 16.1% |
| Boundary | 8 | 25.8% |
| Negative | 10 | 32.3% |
| Edge Case | 5 | 16.1% |
| Decision Table | 3 | 9.7% |
| **Total** | **31** | **100%** |

### 1.2 Statistics by Priority

| Priority | Count | Percentage |
|---|---|---|
| Critical | 5 | 16.1% |
| High | 13 | 41.9% |
| Medium | 10 | 32.3% |
| Low | 3 | 9.7% |
| **Total** | **31** | **100%** |

---

## 2. Detailed TestCase List

### 2.1 Normal Cases

| ID | TestCase Name | Category | Priority | Description | Preconditions | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-001 | Import valid record with role user | Normal | Critical | Verify importing 1 valid record with all fields populated, role = user | CSV file exists, DB is ready | `1,Nguyen Van A,nguyenvana@email.com,25,user` | Record inserted into t_user, status SUCCESS |
| TC-002 | Import valid record with role admin | Normal | Critical | Verify importing valid record with role = admin | CSV file exists, DB is ready | `2,Tran Thi B,tranthib@email.com,30,admin` | Record inserted into t_user, status SUCCESS |
| TC-003 | Import valid record with role viewer | Normal | Critical | Verify importing valid record with role = viewer | CSV file exists, DB is ready | `3,Le Van C,levanc@email.com,40,viewer` | Record inserted into t_user, status SUCCESS |
| TC-004 | Import valid record with blank age | Normal | High | Verify importing valid record when age is blank (optional field) | CSV file exists, DB is ready | `4,Pham Thi D,phamthid@email.com,,user` | Record inserted with age = NULL, status SUCCESS |
| TC-005 | Import CSV file with multiple valid records | Normal | Critical | Verify importing CSV file containing 5 valid records, all must be inserted successfully | CSV file has 5 records, DB is ready | CSV file with 5 valid data rows | 5 records inserted successfully, summary: total=5, success=5, failed=0 |

### 2.2 Boundary Cases

| ID | TestCase Name | Category | Priority | Description | Preconditions | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-006 | ID minimum boundary value (id=1) | Boundary | High | Verify id = 1, the minimum valid value (> 0) | CSV file exists, DB is ready | `1,Boundary Min,boundarymin@test.com,20,user` | Record inserted successfully with id=1 |
| TC-007 | ID maximum boundary value (id=2147483647) | Boundary | High | Verify id = 2147483647 (max INT value) | CSV file exists, DB is ready | `2147483647,Max Int,maxint@test.com,25,admin` | Record inserted successfully with id=2147483647 |
| TC-008 | Name 1 character (min boundary) | Boundary | High | Verify name with exactly 1 character, the minimum length boundary | CSV file exists, DB is ready | `5,A,a@test.com,25,user` | Record inserted successfully with name='A' |
| TC-009 | Name 100 characters (max boundary) | Boundary | High | Verify name with exactly 100 characters, the maximum length boundary | CSV file exists, DB is ready | `6,AAAA...A (100 chars),long@test.com,25,user` | Record inserted successfully with 100-char name |
| TC-010 | Age minimum boundary value (age=0) | Boundary | High | Verify age = 0, the minimum valid value | CSV file exists, DB is ready | `7,Baby User,baby@test.com,0,viewer` | Record inserted successfully with age=0 |
| TC-011 | Age maximum boundary value (age=150) | Boundary | High | Verify age = 150, the maximum valid value | CSV file exists, DB is ready | `8,Old User,old@test.com,150,user` | Record inserted successfully with age=150 |
| TC-012 | Email minimum valid format | Boundary | Medium | Verify email with minimum format a@b.c (shortest valid email) | CSV file exists, DB is ready | `9,Min Email,a@b.c,25,user` | Record inserted successfully |
| TC-013 | CSV with exactly 100,000 records | Boundary | Low | Verify batch processes exactly 100,000 records (max boundary value) | 100K records CSV file, DB ready | CSV file with 100,000 valid data rows | All 100,000 records inserted successfully, duration ≤ 30 mins |

### 2.3 Negative Cases

| ID | TestCase Name | Category | Priority | Description | Preconditions | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-014 | ID null/empty | Negative | High | Verify handling when id field is missing (empty string) | CSV file exists | `,Missing ID,missing@test.com,25,user` | Record skipped, error logged: ERR_ID_REQUIRED |
| TC-015 | Negative ID (id=-1) | Negative | High | Verify handling when id = -1 (violates > 0 constraint) | CSV file exists | `-1,Negative ID,neg@test.com,25,user` | Record skipped, error logged: ERR_ID_NOT_POSITIVE |
| TC-016 | ID is not an integer | Negative | High | Verify handling when id is not an integer | CSV file exists | `abc,Not Integer,notint@test.com,25,user` | Record skipped, error logged: ERR_ID_NOT_INTEGER |
| TC-017 | Name null/empty | Negative | High | Verify handling when name field is missing | CSV file exists | `10,,noname@test.com,25,user` | Record skipped, error logged: ERR_NAME_REQUIRED |
| TC-018 | Name exceeds 100 characters | Negative | Medium | Verify handling when name is 101 characters (exceeds max limit) | CSV file exists | `11,AAAA...A (101 chars),toolong@test.com,25,user` | Record skipped, error logged: ERR_NAME_LENGTH |
| TC-019 | Email missing @ character | Negative | High | Verify handling when email does not contain @ | CSV file exists | `12,Bad Email,bademailtest.com,25,user` | Record skipped, error logged: ERR_EMAIL_FORMAT |
| TC-020 | Email missing domain (after @) | Negative | High | Verify handling when email has @ but lacks valid domain part (no dot) | CSV file exists | `13,No Domain,nodomain@test,25,user` | Record skipped, error logged: ERR_EMAIL_FORMAT |
| TC-021 | Negative age value (age=-1) | Negative | Medium | Verify handling when age = -1 (below minimum boundary 0) | CSV file exists | `14,Neg Age,negage@test.com,-1,user` | Record skipped, error logged: ERR_AGE_RANGE |
| TC-022 | Age exceeds limit (age=151) | Negative | Medium | Verify handling when age = 151 (above maximum boundary 150) | CSV file exists | `15,Over Age,overage@test.com,151,user` | Record skipped, error logged: ERR_AGE_RANGE |
| TC-023 | Invalid role | Negative | Medium | Verify handling when role = 'unknown' (not in the allowed list) | CSV file exists | `16,Bad Role,badrole@test.com,25,unknown` | Record skipped, error logged: ERR_ROLE_INVALID |

### 2.4 Edge Cases

| ID | TestCase Name | Category | Priority | Description | Preconditions | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-024 | Name contains accented Unicode characters | Edge Case | Medium | Verify handling of Vietnamese accented names (Unicode), SPEC allows Unicode letters | UTF-8 CSV file | `17,Nguyễn Văn Á,unicode@test.com,25,user` | Record inserted successfully (Unicode is valid letter) |
| TC-025 | SQL injection pattern in name field | Edge Case | Medium | Verify batch is not vulnerable to SQL injection when name contains SQL string | CSV file exists | `18,'; DROP TABLE users;--,sqlinj@test.com,25,user` | Record skipped due to special characters in name (ERR_NAME_INVALID_CHARS) |
| TC-026 | Empty CSV file (header only) | Edge Case | Medium | Verify handling when CSV file only contains header row and no data | CSV file with header only | CSV file: `id,name,email,age,role` (1 row) | Batch ends with warning, EXIT_CODE=2, no insertion |
| TC-027 | Duplicate ID in CSV file | Edge Case | Medium | Verify handling when 2 records in the file share the same ID | CSV file exists | Record 1: id=1, Record 2: id=1 | First record inserted successfully, second record skipped: ERR_ID_DUPLICATE |
| TC-028 | CSV file exceeds 100,000 records | Edge Case | Low | Verify batch rejects file with 100,001 records (exceeds performance limits) | 100,001 records CSV | 100,001 rows CSV file | Batch ends with EXIT_CODE=3, NO records processed |

### 2.5 Decision Table Cases

| ID | TestCase Name | Category | Priority | Description | Preconditions | Input Summary | Expected Output Summary |
|---|---|---|---|---|---|---|---|
| TC-029 | Multiple invalid fields simultaneously | Decision Table | Medium | Verify when a record has both an invalid ID and an invalid email. The batch must log only the first encountered error (first error wins) | CSV file exists | `abc,Test,bademail,25,user` | Record skipped, error log only logs the first error: ERR_ID_NOT_INTEGER |
| TC-030 | First record invalid, second record valid | Decision Table | High | Verify batch continues processing after encountering an invalid record. Invalid record does not affect subsequent valid record | CSV file exists | Record 1: invalid, Record 2: valid | Record 1 skipped + error logged, Record 2 inserted successfully |
| TC-031 | All records invalid | Decision Table | Low | Verify batch handling when 100% of records are invalid | CSV file exists | CSV file with 3 records, all invalid | 0 records inserted, 3 records error, summary: success=0, failed=3 |

---

## 3. Traceability Matrix

| Requirement ID | Requirement Description | TestCase IDs | Coverage Status |
|---|---|---|---|
| REQ-001 | Import valid records into database | TC-001, TC-002, TC-003, TC-004, TC-005 | ✅ Complete |
| REQ-002 | Validate id field (required, integer, > 0, unique) | TC-006, TC-007, TC-014, TC-015, TC-016, TC-027 | ✅ Complete |
| REQ-003 | Validate name field (required, 1-100 chars, no special chars) | TC-008, TC-009, TC-017, TC-018, TC-024, TC-025 | ✅ Complete |
| REQ-004 | Validate email field (required, format xxx@xxx.xxx) | TC-012, TC-019, TC-020 | ✅ Complete |
| REQ-005 | Validate age field (optional, 0-150) | TC-004, TC-010, TC-011, TC-021, TC-022 | ✅ Complete |
| REQ-006 | Validate role field (required, in [admin, user, viewer]) | TC-001, TC-002, TC-003, TC-023 | ✅ Complete |
| REQ-007 | Write error log for invalid records | TC-014 ~ TC-023, TC-025, TC-027 | ✅ Complete |
| REQ-008 | Process empty CSV file | TC-026 | ✅ Complete |
| REQ-009 | Limit to 100,000 records | TC-013, TC-028 | ✅ Complete |
| REQ-010 | Invalid record does not affect other records | TC-030 | ✅ Complete |
| REQ-011 | First error wins (only 1 error logged per record) | TC-029 | ✅ Complete |
| REQ-012 | All records invalid | TC-031 | ✅ Complete |

---

## 4. Reference Decision Table

| Condition / Action | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|
| **Conditions** | | | | | | |
| valid id | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| valid name | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| valid email | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Actions** | | | | | | |
| Insert DB | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Skip + Error Log | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Error field | - | id | name | email | id | id |

---

## 5. TestCase Review Checklist

- [x] Each requirement has at least 1 testcase.
- [x] There is a testcase for every equivalence partition.
- [x] There is a testcase for every boundary value.
- [x] There is a negative testcase for every error condition.
- [x] Priorities are correctly assigned.
- [x] Naming convention strictly follows TC-{NNN}.
- [x] TestCase descriptions are clear and understandable without reading the SPEC.
- [x] Preconditions are fully documented.
- [x] Expected output is specific and verifiable.
- [x] Traceability matrix is complete, and all requirements have the ✅ status.
- [x] No duplicate testcases exist.
- [x] Total number of testcases (31) matches the estimation.
