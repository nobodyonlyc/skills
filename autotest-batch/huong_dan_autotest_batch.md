# 📖 CẨM NANG HƯỚNG DẪN QUY TRÌNH BATCH AUTOTEST TOÀN DIỆN
> **Phiên bản tài liệu**: 1.3.0  
> **Ngôn ngữ**: Tiếng Việt  
> **Đối tượng**: Chuyên viên QA, Developer, Business Analyst (BA) và Khách hàng  

Tài liệu này trình bày chi tiết quy trình kiểm thử tự động hóa cho các hệ thống xử lý hàng loạt (**Batch Processing**) sử dụng AI Agent. Quy trình này được thiết kế để đảm bảo độ bao phủ **100% yêu cầu (Requirements)** và **100% các biên dữ liệu đầu vào**, loại bỏ hoàn toàn rủi ro thiếu kịch bản kiểm thử, đồng thời phân định rõ ràng ranh giới tự động hóa thông qua mô hình phân cấp 3 mức độ.

---

## 🗺️ Sơ Đồ Tổng Quan Quy Trình 5 Giai Đoạn (5-Phase Pipeline)

Quy trình vận hành qua 5 giai đoạn tuần tự với **5 Cổng kiểm soát chất lượng (Review Gates)** bắt buộc phải có sự phê duyệt của con người trước khi chuyển bước:

```
[ Phase 1: SPEC Analysis ] 
       │
   (Gate 1: Duyệt Phân tích SPEC)
       ▼
[ Phase 2: TestCase Generation ] 
       │
   (Gate 2: Duyệt Ma trận & TC)
       ▼
[ Phase 3: TestData Generation ] 
       │
   (Gate 3: Thẩm định Tĩnh Data)
       ▼
[ Phase 4: Parallel Test Execution ] 
       │
   (Gate 4: Duyệt Verdict Level 2)
       ▼
[ Phase 5: Report Aggregation ] 
       │
   (Gate 5: Ký duyệt Báo cáo Cuối)
```

---

## 📌 GIAI ĐOẠN 1: PHÂN TÍCH TÀI LIỆU ĐẶC TẢ (SPEC ANALYSIS)

AI Agent tiếp nhận tài liệu đặc tả (SPEC) nghiệp vụ đầu vào và tiến hành trích xuất cấu trúc dữ liệu kỹ thuật thành các bảng chuẩn hóa:

1.  **Trích xuất Yêu cầu Nghiệp vụ (Business Rules - BR)**: Đánh mã định danh duy nhất (`BR-001`, `BR-002`,...) cho từng quy tắc để phục vụ việc truy vết.
2.  **Bảng Cấu trúc Trường Đầu Vào/Đầu Ra (Fields Schema)**: Xác định tên trường, kiểu dữ liệu kỹ thuật (String, Decimal, Date, Boolean, Binary), độ dài và tính bắt buộc (Required/Optional).
3.  **Bảng Ràng buộc & Biên dữ liệu**: Liệt kê cụ thể khoảng giá trị, định dạng định sẵn (Regex), danh sách hợp lệ (Enum).
4.  **Phân tích Trạng thái Dữ liệu (Data States)**: Các trạng thái của bản ghi trong vòng đời xử lý (ví dụ: `RECEIVED` ➔ `PROCESSING` ➔ `SUCCESS`/`FAILED`).
5.  **Bảng Tác động Cơ sở Dữ liệu (DB CRUD Impact)**: Các bảng DB mà Batch tương tác cùng hành động mong đợi (Read, Write, Update, Delete).
6.  **Phân chia Vùng Tương Đương (Equivalence Partitions)**: Chia miền giá trị của từng trường thành các phân vùng hợp lệ và bất hợp lệ.

> [!NOTE]
> **Cổng Kiểm soát 1 (Gate 1)**: Agent in báo cáo tóm tắt spec trực tiếp lên chat. BA/PM rà soát xem Agent đã hiểu đúng và đủ các quy tắc nghiệp vụ chưa trước khi cho phép sinh TestCase.

---

## 📌 GIAI ĐOẠN 2: THIẾT KẾ KỊCH BẢN KIỂM THỬ (TESTCASE GENERATION)

Để tránh bỏ sót kịch bản (nỗi sợ lớn nhất của khách hàng), Agent sử dụng một tổ hợp các phương pháp thiết kế TestCase nâng cao:

### 2.1 Ma trận Kiểm thử Dữ liệu Batch (Batch Test Data Matrix)
Agent thiết lập một ma trận hai chiều bao phủ toàn bộ biên trường dữ liệu đầu vào kết hợp với các đặc thù Batch:
*   **Trục dọc (Vertical)**: Các trường dữ liệu đầu vào + Các kịch bản Batch toàn cục (Global File/Batch).
*   **Trục ngang (Horizontal)**: 8 đặc tính kiểm thử bắt buộc:
    1.  **Normal Case**: Giá trị hợp lệ thông thường.
    2.  **Boundary**: Giá trị biên ($Min, Max, Min-1, Max+1$, độ dài chuỗi tối đa).
    3.  **Null/Empty/Space**: Giá trị rỗng (`NULL`), chuỗi rỗng (`""`), chuỗi toàn khoảng trắng (`"   "`).
    4.  **Invalid / Format**: Định dạng sai, kiểu dữ liệu không khớp, số âm ở nơi không cho phép.
    5.  **Encoding / Ký tự đặc biệt**: Shift-JIS/CP932 (half-width kana vs full-width), wave dash `〜` (lỗi dịch Unicode), control characters (Null byte `\x00`, Tab, LF), Byte Order Mark (BOM).
    6.  **Batch Volume**: File trống (0 record), file chỉ có 1 record, file khối lượng cực lớn (Large Volume) để test tràn bộ đệm.
    7.  **Batch State**: Bản ghi trùng khóa (Duplicate key), sai thứ tự sắp xếp bắt buộc (Sort order), bản ghi bị cắt dở/lỗi cấu trúc (Truncated/Malformed record).
    8.  **Rerun / Resilience**: Chạy lại khi job lỗi nửa chừng để kiểm tra tính Idempotent (không trùng lặp dữ liệu).

### 2.2 Các kỹ thuật thiết kế TestCase bổ trợ
*   **Decision Table Testing (Bảng Quyết định)**: Tổ hợp toàn bộ các điều kiện nghiệp vụ để đảm bảo không sót logic rẽ nhánh.
*   **State Transition Testing (Chuyển đổi trạng thái)**: Kiểm thử tất cả các đường chuyển dịch trạng thái hợp lệ và bất hợp lệ của bản ghi.
*   **Database CRUD Matrix**: Thiết kế kịch bản thiết lập trạng thái DB trước khi chạy (Pre-state) và kiểm tra DB sau khi chạy (Post-state).
*   **Fault Tolerance & Recovery**: Giả lập sự cố mất kết nối mạng, đầy đĩa, hoặc sập tiến trình giữa chừng để test khả năng rollback/recovery từ checkpoint.
*   **Pairwise Testing**: Áp dụng thuật toán tổ hợp tối ưu cho các tham số cấu hình phức tạp nhằm giảm số lượng case nhưng vẫn đạt độ bao phủ lỗi tốt nhất.

### 2.3 Phân cấp 3 Mức độ Tự động hóa (Automation & Triage Sheet)
Để thiết lập ranh giới rõ ràng cho AI Agent và con người, mọi TestCase được phân loại:
*   **Mức 1 — Tự động hóa hoàn toàn (Level 1 - Fully Automated)**:
    *   *Đặc điểm*: Có oracle (kết quả mong đợi) rõ ràng, mang tính xác định (deterministic).
    *   *Ví dụ*: So khớp layout file, đối soát số lượng bản ghi (Vào = Ra + Reject), đối soát tổng số tiền, kiểm tra encoding/BOM, so sánh diff file/DB.
*   **Mức 2 — Kiểm duyệt chéo (Level 2 - Human-in-the-loop)**:
    *   *Đặc điểm*: AI tự chạy, nhưng kết quả cần con người đưa ra phán quyết (verdict).
    *   *Ví dụ*: Chênh lệch làm tròn số nhỏ, timing lệch vài giây, cảnh báo (warning) mơ hồ trong log mà đặc tả không quy định rõ. AI trình bày bằng chứng và dừng chờ người phê duyệt.
*   **Mức 3 — Thủ công / Bàn giao (Level 3 - Manual / Handoff)**:
    *   *Đặc điểm*: Phụ thuộc môi trường ngoài, hệ thống bên thứ ba không điều khiển được, hoặc bài toán kiểm định nghiệp vụ sâu (Oracle Problem - thực tế khớp expected file, nhưng expected file có phản ánh đúng nghiệp vụ thật của khách hàng hay không).
    *   *Ví dụ*: Tích hợp CoreBank dạng black-box, timing lịch chạy thật của hệ thống khách hàng, kiểm thử dò tìm lỗi tự do (Exploratory testing), rút cáp mạng thật.
    *   *Xử lý*: AI bỏ qua việc thực thi tự động, đánh dấu trạng thái là `HANDOFF` và lập **Manual Handoff List** kèm hướng dẫn chi tiết cho tester thực hiện.

---

## 📌 GIAI ĐOẠN 3: SINH DỮ LIỆU KIỂM THỬ (TEST DATA GENERATION)

AI Agent tự động tạo các bộ dữ liệu kiểm thử dựa trên thiết kế TestCase:

1.  **Nguyên tắc Cô lập lỗi (Fault Isolation Principle)**: Với mỗi TestCase âm tính (Negative/Invalid Case), dữ liệu kiểm thử chỉ được vi phạm **duy nhất một ràng buộc** của trường đó, tất cả các trường khác phải giữ giá trị hợp lệ thông thường. Điều này đảm bảo nếu testcase fail, nguyên nhân được chỉ ra là duy nhất và chính xác.
2.  **Sinh dữ liệu đột biến cấu trúc**: Tạo ra các file bị hỏng dòng, thiếu dấu phân cách, sai encoding (ví dụ file Shift-JIS hoặc chứa ký tự đặc biệt Nhật).
3.  **Tạo Script thiết lập cơ sở dữ liệu ban đầu (Pre-state SQL)**: Thiết lập dữ liệu nền trong DB cho các ca test CRUD và kịch bản Rerun/Idempotency.
4.  **Trình thẩm định dữ liệu tĩnh (Static Test Data Validator)**: Chạy một script Python độc lập để quét file dữ liệu JSON đầu ra, đối chiếu ngược lại các ràng buộc trong SPEC nhằm phát hiện sớm lỗi sai lệch kiểu dữ liệu hoặc vi phạm nguyên tắc cô lập lỗi.

---

## 📌 GIAI ĐOẠN 4: THỰC THI KIỂM THỰ (TEST EXECUTION FLOW)

Luồng thực thi kiểm thử được tối ưu hóa bằng cách chạy song song và phân nhánh theo 3 Mức độ:

```
                  [ Bắt đầu chạy Phase 4 ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ Chạy Tự Động (Level 1, 2) ]       [ Bàn giao (Level 3) ]
            │                                 │
     Phân chia SubAgents                      │
    chạy song song (Max=5)                    │
            │                                 │
   ┌────────┴────────┐                        │
   ▼                 ▼                        ▼
[Level 1]         [Level 2]            Đánh dấu HANDOFF/SKIP
   │                 │                        │
AI chạy &        AI chạy &                    │
tự quyết         in logs ra chat              │
verdict              │                        │
   │            Gọi ask_question              │
   │            chờ người duyệt               │
   │                 │                        │
   └────────┬────────┘                        │
            ▼                                 ▼
    [ Gộp kết quả tự động ]          [ Xuất chỉ dẫn thủ công ]
            └────────────────┬────────────────┘
                             ▼
                    [ Hoàn thành Phase 4 ]
```

*   **Cô lập thư mục TestCase**: Để thư mục làm việc sạch sẽ, dữ liệu đầu vào và kết quả đầu ra của từng testcase `TC-xxx` được gom gọn vào cấu trúc thư mục cô lập: `test_runs/run_<timestamp>_<run_id>/TC-xxx/input/` và `/output/`. Không tạo các thư mục tạm tràn lan ngoài thư mục chạy tập trung.
*   **Quy tắc Source Code Integrity**: Tuyệt đối không sửa đổi mã nguồn hoặc tiêm mã giả (mock code) vào tiến trình ứng dụng thực tế. Nếu phát hiện lỗi, ghi nhận lỗi trực tiếp, không tự sửa code để làm đẹp báo cáo.

---

## 📌 GIAI ĐOẠN 5: TỔNG HỢP & BÁO CÁO (REPORT OUTPUT)

Giai đoạn cuối cùng gộp tất cả dữ liệu thực thi thành báo cáo kỹ thuật toàn diện `5_final_report.md` và tệp dữ liệu gốc `5_report_raw.json` lưu trong thư mục chạy tập trung.

### Cấu trúc Báo cáo Kết quả cuối cùng (`5_final_report.md`):

1.  **Executive Summary (Tóm tắt điều hành)**:
    *   Tổng số TestCase, số lượng/tỷ lệ đạt (Passed), lỗi (Failed), bỏ qua (Skipped/Handoff).
    *   Tỷ lệ đạt (Pass Rate) tính trên các case đã chạy: $\text{Pass Rate} = \frac{\text{Passed}}{\text{Total} - \text{Skipped}} \times 100\%$.
    *   Kết luận cuối cùng: `PASS` / `CONDITIONAL PASS` / `FAIL`.
2.  **Detailed Statistics (Thống kê chi tiết)**:
    *   Thống kê chi tiết số lượng Pass/Fail/Skip theo Phân loại (Category).
    *   Thống kê chi tiết theo Độ ưu tiên (Priority).
    *   Thống kê chi tiết theo **Mức độ Tự động hóa (Automation Level)** (Level 1, 2, 3).
3.  **Detailed Results (Bảng kết quả chi tiết)**:
    *   Hiển thị bảng kết quả đầy đủ: `ID | Tên | Phân loại | Độ ưu tiên | Mức độ Auto | Trạng thái | Input | Expected | Actual | Chi tiết lỗi`.
4.  **Failed TestCases Analysis (Phân tích lỗi)**:
    *   Với mỗi kịch bản bị Fail, báo cáo chỉ rõ **Nguyên nhân gốc rễ (Root Cause)**, **Tham chiếu SPEC bị vi phạm**, và **Đề xuất khắc phục cụ thể** kèm theo mức độ nghiêm trọng (Critical/High/Medium/Low).
5.  **Coverage Matrix (Ma trận độ bao phủ yêu cầu)**:
    *   Truy vết ngược từ từng yêu cầu đặc tả `BR-xxx` sang trạng thái Pass/Fail của các TestCase tương ứng, đảm bảo mọi nghiệp vụ đều đã được kiểm tra thành công.
6.  **Manual Integration Testing Handoff List (Danh sách bàn giao thủ công)**:
    *   Liệt kê toàn bộ các TestCase Level 3 kèm theo **Lý do bàn giao (Triage Reason)** và **Hướng dẫn các bước thực hiện thủ công chi tiết** cho tester con người.
7.  **Metadata (Siêu dữ liệu vận hành)**:
    *   Ghi nhận thời gian thực hiện (Duration), tổng lượng Token AI đã tiêu thụ để đo lường hiệu năng của hệ thống AutoTest.

---
*Bản quyền quy trình kiểm thử thuộc về dự án Batch AutoTest Pipeline.*
