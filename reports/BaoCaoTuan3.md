# BÁO CÁO TIẾN ĐỘ TUẦN 3 – ĐỀ TÀI: NHÀ THÔNG MINH ĐIỀU KHIỂN THIẾT BỊ GIẢ LẬP QUA AWS IoT CORE

**Môn học:** Cloud – Đợt 1 – Năm học 2026–2027
**Nhóm:** Integration & IoT
**Giảng viên hướng dẫn:** TS. Huỳnh Xuân Phụng
**Thời gian báo cáo:** `[DD/MM/2026]` – `[DD/MM/2026]`
**GitHub Repository (Public):** https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
**Báo cáo tuần 3:** [reports/BaoCaoTuan3.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md)
**Sơ đồ kiến trúc hệ thống:** [reports/docs/images/architecture-diagram.png](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/architecture-diagram.png)

> **Hướng dẫn điền (xóa trước khi nộp):** các mục `[...]` là chỗ điền kết quả THỰC TẾ. Chỉ ghi "đã hoàn thành" cho phần đã chạy thật trên AWS Learner Lab và có ảnh (có Account ID, Region, thời gian) hoặc code trong repository. Hạng mục chưa làm thì ghi rõ và chuyển sang tuần 4.

---

## 1. MỤC TIÊU VÀ KẾT QUẢ ĐẠT ĐƯỢC TRONG TUẦN 3

Theo kế hoạch tuần 2, tuần 3 tập trung **tích hợp các thành phần, bảo mật, giám sát bằng CloudWatch và tự động hóa/IaC nếu có**. Tuần 2 chưa có minh chứng cho DynamoDB, Lambda, API Gateway và IoT Rule, nên các hạng mục này được hoàn thiện trước làm nền cho phần tích hợp.

Các kết quả đạt được *(chỉ giữ lại hạng mục đã làm thật; hạng mục chưa xong ghi ở mục 4)*:

**Hoàn thiện các thành phần còn tồn từ tuần 2:**

- Tạo bảng DynamoDB `[tên bảng]` lưu lịch sử thiết bị. *(Minh chứng: `[link ảnh]`)*
- Triển khai Lambda điều khiển thiết bị (cập nhật `desired` lên Device Shadow) và kiểm thử riêng. *(Minh chứng: `[link ảnh]`, `[link mã nguồn]`)*
- Cấu hình API Gateway tích hợp Lambda, có endpoint kiểm thử được. *(Minh chứng: `[link ảnh]`)*

**Tích hợp:**

- Cấu hình AWS IoT Rule ghi sự kiện Device Shadow vào DynamoDB. *(Minh chứng: `[link ảnh]`)*
- Xây dựng giao diện web trên S3 gọi API Gateway để bật/tắt và chỉnh thông số 3 thiết bị. *(Minh chứng: `[link ảnh]`, `[link mã nguồn]`)*
- Kiểm thử luồng end-to-end: Web → API Gateway → Lambda → Device Shadow → thiết bị Python → `reported` → DynamoDB. *(Minh chứng: `[link ảnh]`, `[link log]`)*
- Hoàn thiện simulator: xử lý ngắt kết nối/kết nối lại, ghi log, kiểm thử cả 3 thiết bị nhận `delta`. *(Minh chứng: `[link log]`)*

**Bảo mật:**

- Rà soát IoT Policy theo nguyên tắc quyền tối thiểu (giới hạn theo tên Thing). *(Minh chứng: `[link ảnh nội dung policy]`)*
- Thu hẹp CORS của API Gateway và kiểm tra dữ liệu đầu vào trong Lambda. *(Minh chứng: `[link ảnh/mã nguồn]`)*
- Kiểm tra repository không chứa certificate, private key hoặc biến môi trường. *(Minh chứng: `[link .gitignore]`, `[kết quả git status/git log]`)*

**Giám sát:**

- Bật và kiểm tra CloudWatch Logs cho Lambda và API Gateway. *(Minh chứng: `[link ảnh]`)*
- Tạo CloudWatch Alarm cho lỗi Lambda và lỗi 5XX của API Gateway. *(Minh chứng: `[link ảnh]`)*

**Tự động hóa/IaC (nếu có):**

- Viết template CloudFormation/SAM cho `[bảng DynamoDB / IoT Rule / Lambda]` và triển khai thử. *(Minh chứng: `[link template]`, `[link ảnh stack]`)*

**Quản lý tài nguyên:**

- Gắn tag Project/Owner cho tài nguyên mới; dừng/xóa tài nguyên không cần thiết sau mỗi buổi làm. *(Minh chứng: `[link ảnh]`)*

---

## 2. BẢNG TỔNG HỢP PHÂN CÔNG VÀ SỐ GIỜ LÀM VIỆC

### 2.1. Phân công nhiệm vụ

| Thành viên | MSSV | Vai trò và nhiệm vụ chính | Số giờ cá nhân | Tổng số giờ |
|---|---|---|---|---|
| Trần Nguyễn Minh Hiếu | 24110212 | Cấu hình IoT Rule ghi lịch sử vào DynamoDB; hoàn thiện simulator (kết nối lại, log); rà soát IoT Policy; kiểm thử end-to-end | `[..] giờ` | `[..] giờ` |
| Nguyễn Trung Kiên | 24110263 | Hoàn thiện DynamoDB, Lambda, API Gateway; xây dựng giao diện web trên S3; thiết lập CloudWatch Logs/Alarm; viết template IaC | `[..] giờ` | `[..] giờ` |
| **Tổng cộng** | | | `[..] giờ` | `[..] giờ` |

> Yêu cầu: mỗi sinh viên tối thiểu **8 giờ/tuần**; giờ làm ghi đúng thời gian thực tế.

### 2.2. Nhật ký công việc (Worklog)

| Ngày thực hiện | Thành viên | Nội dung công việc | Thời gian |
|---|---|---|---|
| `[DD/MM/2026]` | Trần Nguyễn Minh Hiếu | Tạo IoT Rule ghi Shadow vào DynamoDB; kiểm thử bản ghi | `[..] giờ` |
| `[DD/MM/2026]` | Trần Nguyễn Minh Hiếu | Hoàn thiện simulator; rà soát IoT Policy; kiểm thử end-to-end | `[..] giờ` |
| `[DD/MM/2026]` | Nguyễn Trung Kiên | Hoàn thiện DynamoDB, Lambda, API Gateway; kiểm thử endpoint | `[..] giờ` |
| `[DD/MM/2026]` | Nguyễn Trung Kiên | Giao diện web trên S3; CloudWatch Logs/Alarm; template IaC | `[..] giờ` |
| **Tổng cộng** | 2 thành viên | | `[..] giờ` |

---

## 3. CHI TIẾT CÔNG VIỆC VÀ MINH CHỨNG TRÊN GITHUB

### 3.1. Trần Nguyễn Minh Hiếu – MSSV: 24110212

#### a. IoT Rule ghi lịch sử thiết bị vào DynamoDB (`[..]` giờ)

- IoT Rule lắng nghe topic `$aws/things/+/shadow/update/accepted` và ghi mỗi lần cập nhật Shadow vào bảng DynamoDB.
- Câu truy vấn SQL dự kiến (cần đối chiếu với rule thực tế đã tạo):

```sql
SELECT topic(3) AS deviceId,
       timestamp() AS timestamp,
       'SHADOW_UPDATE' AS eventType,
       state AS state
FROM '$aws/things/+/shadow/update/accepted'
```

- Action: DynamoDBv2 (mỗi trường của kết quả SQL thành một thuộc tính), ghi vào bảng có khóa `deviceId` (partition) và `timestamp` (sort). Role của rule dùng **LabRole** theo quy định môn học.
- Kiểm thử: cập nhật Shadow từ Console hoặc từ giao diện web → kiểm tra bản ghi mới trong DynamoDB (Explore items).
- Minh chứng: `[link ảnh Rule]`, `[link ảnh bản ghi DynamoDB]`

#### b. Hoàn thiện simulator và rà soát IoT Policy (`[..]` giờ)

- Simulator xử lý ngắt kết nối và tự kết nối lại; ghi log có thời gian cho từng thiết bị.
- Kiểm thử đủ 3 thiết bị: gửi `desired` cho `smart-light`, `smart-ac`, `smart-fan` và xác nhận từng thiết bị nhận `delta`, cập nhật `reported`.
- Rà soát IoT Policy: giới hạn `iot:Connect`, `iot:Publish`, `iot:Receive`, `iot:Subscribe` theo tên Thing và chỉ các topic Shadow cần dùng; không dùng `*` cho toàn bộ tài nguyên. Nội dung policy thực tế: `[dán JSON hoặc link ảnh tab Versions]`.
- Certificate và private key lưu trong `certs/`, nằm trong `.gitignore`; không đưa lên GitHub.
- Minh chứng GitHub:
  - Mã nguồn: [src/devices/simulator.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py)
  - Log kiểm thử: `[link logs/...]`

### 3.2. Nguyễn Trung Kiên – MSSV: 24110263

#### a. DynamoDB, Lambda và API Gateway (`[..]` giờ)

- Bảng DynamoDB `[tên bảng]`: partition key `deviceId` (String), sort key `timestamp` (Number); chế độ On-demand. *(Cần khớp với cấu hình thực tế.)*
- Lambda `[tên hàm]` (Python `[phiên bản]`), execution role **LabRole**, biến môi trường `IOT_ENDPOINT`:
  - `POST /devices/{thingName}/control`: kiểm tra tên thiết bị và thuộc tính hợp lệ, cập nhật `desired` lên Device Shadow.
  - `GET /devices/{thingName}/history`: đọc lịch sử từ DynamoDB `[nếu có]`.
- API Gateway `[REST/HTTP]`, stage `[tên]`, tích hợp Lambda; CORS giới hạn origin của website S3.
- Kiểm thử bằng `curl`/Postman:

```bash
curl -X POST https://<api-id>.execute-api.us-east-1.amazonaws.com/<stage>/devices/smart-light/control \
  -H "Content-Type: application/json" -d '{"power":"ON","brightness":80}'
```

- Minh chứng: `[link ảnh bảng DynamoDB]`, `[link ảnh Lambda]`, `[link ảnh API Gateway + kết quả curl]`
- Mã nguồn: `[link src/lambda/...]`

#### b. Giao diện web trên S3 (`[..]` giờ)

- Trang web tĩnh (HTML/JS) trong bucket `iot-smarthome-website`, gọi API Gateway để điều khiển và hiển thị trạng thái 3 thiết bị `[và lịch sử]`.
- Bật static website hosting; cấu hình quyền đọc công khai chỉ cho các tệp giao diện (không chứa khóa hoặc thông tin nhạy cảm). Nếu Learner Lab hạn chế public access thì ghi rõ cách xử lý: `[..]`.
- Minh chứng: `[link ảnh cấu hình S3]`, `[link ảnh giao diện]`
- Mã nguồn: `[link web/...]`

#### c. Giám sát CloudWatch và IaC (`[..]` giờ)

- CloudWatch Logs: log group của Lambda và API Gateway; kiểm tra log xuất hiện khi gọi API.
- CloudWatch Alarm (dự kiến): `Errors ≥ 1` trong 5 phút cho Lambda; `5XXError ≥ 1` cho API Gateway. Hành động của alarm: `[thông báo SNS / chỉ hiển thị trạng thái, tùy quyền Learner Lab]`.
- IaC `[nếu có]`: template CloudFormation/SAM cho `[tài nguyên]`, ví dụ khung bảng DynamoDB (cần kiểm thử trước khi dùng):

```yaml
Resources:
  DeviceHistoryTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - { AttributeName: deviceId, AttributeType: S }
        - { AttributeName: timestamp, AttributeType: N }
      KeySchema:
        - { AttributeName: deviceId, KeyType: HASH }
        - { AttributeName: timestamp, KeyType: RANGE }
      Tags:
        - { Key: Project, Value: SmartHomeIoT }
        - { Key: Owner1, Value: SV24110212 }
        - { Key: Owner2, Value: SV24110263 }
```

- Minh chứng: `[link ảnh log group]`, `[link ảnh alarm]`, `[link template]`, `[link ảnh stack]`

---

## 4. KẾT QUẢ KIỂM THỬ TỪNG THÀNH PHẦN VÀ TÍCH HỢP

| Thành phần | Kịch bản kiểm thử | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|
| DynamoDB | Ghi và đọc 1 bản ghi mẫu | Bản ghi hiển thị đúng | `[..]` | `[link]` |
| Lambda | Test event hợp lệ / không hợp lệ | 200 / 400 | `[..]` | `[link]` |
| API Gateway | `curl` POST điều khiển đèn | Shadow `desired` được cập nhật | `[..]` | `[link]` |
| IoT Rule → DynamoDB | Cập nhật Shadow | Có bản ghi mới trong bảng | `[..]` | `[link]` |
| Simulator (3 thiết bị) | Gửi `desired` cho từng thiết bị | Nhận delta, cập nhật reported | `[..]` | `[link log]` |
| Web trên S3 | Bấm bật/tắt, đổi thông số | Trạng thái thiết bị đổi theo | `[..]` | `[link]` |
| End-to-end | Web → API → Lambda → Shadow → thiết bị → DynamoDB | Toàn bộ luồng chạy đúng | `[..]` | `[link]` |
| CloudWatch | Gọi API lỗi có chủ đích | Log xuất hiện, alarm đổi trạng thái | `[..]` | `[link]` |

**Lỗi gặp phải và cách khắc phục** *(điền lỗi thực tế: quyền LabRole, CORS, TLS, định dạng payload, v.v.)*:

| Lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `[..]` | `[..]` | `[..]` |

> Hạng mục chưa có kết quả hoặc minh chứng thì ghi rõ trong bảng và chuyển sang kế hoạch tuần 4.

---

## 5. QUẢN LÝ TÀI NGUYÊN, BẢO MẬT VÀ CHI PHÍ

- **Tag:** tài nguyên mới gắn `Project = SmartHomeIoT`, `Owner1 = SV24110212`, `Owner2 = SV24110263` (với dịch vụ hỗ trợ tag). Minh chứng: `[link ảnh]`.
- **Region và quyền:** chỉ dùng `us-east-1`; dùng **LabRole**, không tạo IAM user/role.
- **Bảo mật:** IoT Policy quyền tối thiểu; CORS giới hạn; Lambda kiểm tra đầu vào; không có certificate/private key/`.env` trong repository (kiểm tra bằng `git log --all -- certs/` và tìm `*.pem`, `*.key`): `[kết quả]`.
- **Tài nguyên đang chạy cuối tuần:** `[IoT Things x3, IoT Rule, Lambda, API Gateway, DynamoDB, S3, CloudWatch Alarm]`.
- **Tài nguyên đã dừng/xóa sau buổi làm:** `[..]`.
- **Chi phí ước tính tuần 3** (Billing/Cost Explorer): `[..] USD`. Minh chứng: `[link ảnh]`.

---

## 6. KHAI BÁO SỬ DỤNG AI

*(Mỗi công cụ ghi một mục riêng: công cụ, model, prompt, nội dung AI tạo ra, phần sinh viên đã sửa. Chỉ ghi công cụ đã dùng thật.)*

### 6.1. Công cụ AI đã sử dụng

- **Công cụ:** `[Copilot trong VS Code / Claude / ChatGPT ...]`
- **Mô hình ghi nhận:** `[tên model]`
- **Mục đích sử dụng:** `[ví dụ: gợi ý SQL cho IoT Rule, mã Lambda, trang web điều khiển, template CloudFormation, cách tạo CloudWatch Alarm, gỡ lỗi]`
- **Prompt đã sử dụng:**

> `[dán prompt thực tế]`

### 6.2. Nội dung AI đề xuất và các điều chỉnh của sinh viên

a. **Phân quyền IAM:** `[AI đề xuất gì; nhóm dùng LabRole như thế nào]`
b. **Mã nguồn:** `[phần nào AI sinh, phần nào nhóm sửa để chạy được trên Learner Lab, lỗi đã gỡ]`
c. **Bảo mật:** `[những điều chỉnh về CORS, policy, kiểm tra đầu vào so với đề xuất ban đầu]`
d. **IaC:** `[template AI gợi ý và phần nhóm chỉnh sửa/kiểm thử]`

> Mọi thành viên phải giải thích được toàn bộ cấu hình và mã nguồn khi vấn đáp.

### 6.3. Minh chứng chỉnh sửa báo cáo

- File báo cáo: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md
- Danh sách commit: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main
- Commit cụ thể của tuần 3 *(dán link kèm message sau khi push)*:
  - `[link commit 1 – message]`
  - `[link commit 2 – message]`

---

## 7. KẾT LUẬN VÀ KẾ HOẠCH CÔNG VIỆC TUẦN 4

### 7.1. Kết luận tuần 3

`[Tóm tắt thực tế: thành phần nào đã chạy thật, luồng end-to-end đã kiểm thử chưa, hạng mục nào còn dang dở và lý do.]`

### 7.2. Kế hoạch công việc tuần 4

**Mục tiêu:** Kiểm thử tổng thể, tối ưu chi phí, dọn dẹp tài nguyên, viết báo cáo cuối và quay video demo.

1. **Trần Nguyễn Minh Hiếu – MSSV: 24110212**
   - Công việc 1: Kiểm thử tổng thể toàn bộ luồng với cả 3 thiết bị; ghi nhận lỗi và kết quả; hoàn thiện mã simulator và tài liệu hướng dẫn chạy. *(4 giờ)*
   - Công việc 2: Viết phần báo cáo cuối về IoT Core, Device Shadow và bảo mật; chuẩn bị kịch bản demo. *(4 giờ)*
2. **Nguyễn Trung Kiên – MSSV: 24110263**
   - Công việc 1: Tối ưu chi phí, thống kê chi phí sử dụng; dọn dẹp tài nguyên không cần thiết (giữ lại những gì cần cho demo). *(4 giờ)*
   - Công việc 2: Hoàn thiện báo cáo cuối (kiến trúc, chi phí, kết quả kiểm thử); quay và dựng video demo ≤ 10 phút. *(4 giờ)*
3. **Công việc phối hợp:** diễn tập demo, chụp minh chứng cuối kỳ (Account ID, Region, thời gian), cập nhật Worklog và mã nguồn lên GitHub, chuẩn bị vấn đáp.

**Kết quả đầu ra dự kiến tuần 4:** hệ thống chạy ổn định end-to-end; báo cáo cuối kỳ kèm sơ đồ kiến trúc và báo cáo chi phí; video demo ≤ 10 phút; tài nguyên đã được dọn dẹp sau demo.

> **Lưu ý:** Mỗi sinh viên tối thiểu 8 giờ trong tuần 4; sử dụng LabRole/LabInstanceProfile được cấp; không công khai private key lên GitHub.

---

## 8. DANH MỤC MINH CHỨNG TRÊN GITHUB

- Repository chính: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
- Báo cáo tuần 3: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md
- Sơ đồ kiến trúc: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/architecture-diagram.png
- Cấu hình bảo vệ tệp nhạy cảm: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/.gitignore
- Mã nguồn thiết bị giả lập: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py
- Mã nguồn Lambda: `[link]`
- Mã nguồn giao diện web: `[link]`
- Template IaC: `[link]`
- Ảnh chụp minh chứng: [thư mục reports/docs/images/Week3Pic](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/tree/main/reports/docs/images/Week3Pic)
- Lịch sử commit: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main

### Danh sách ảnh minh chứng cần chụp (đều phải thấy Account ID, Region, giờ hệ thống)

1. Bảng DynamoDB và bản ghi mẫu
2. Lambda: cấu hình, biến môi trường, test thành công
3. API Gateway: route, CORS, kết quả `curl`
4. IoT Rule: câu SQL và action
5. Bản ghi mới trong DynamoDB sau khi cập nhật Shadow
6. Nội dung IoT Policy (tab Versions)
7. Giao diện web điều khiển và S3 static website hosting
8. Log simulator của cả 3 thiết bị nhận `delta`
9. CloudWatch Logs của Lambda/API Gateway
10. CloudWatch Alarm
11. Stack CloudFormation/SAM (nếu có)
12. Billing/Cost Explorer và tag trên tài nguyên
