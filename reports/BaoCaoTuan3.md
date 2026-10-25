# BÁO CÁO TIẾN ĐỘ TUẦN 3 – ĐỀ TÀI: NHÀ THÔNG MINH ĐIỀU KHIỂN THIẾT BỊ GIẢ LẬP QUA AWS IoT CORE

**Môn học:** Cloud – Đợt 1 – Năm học 2026–2027
**Nhóm:** Integration & IoT
**Giảng viên hướng dẫn:** TS. Huỳnh Xuân Phụng
**Thời gian báo cáo:** 19/10/2026 – 25/10/2026
**GitHub Repository (Public):** https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
**Báo cáo tuần 3:** [reports/BaoCaoTuan3.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md)
**Sơ đồ kiến trúc hệ thống:** [reports/docs/images/architecture-diagram.png](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/architecture-diagram.png)

---

## 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ SỐ GIỜ LÀM VIỆC

### 1.1. Phân công nhiệm vụ

| Thành viên | MSSV | Vai trò và nhiệm vụ chính | Số giờ cá nhân | Tổng số giờ |
|---|---|---|---|---|
| Trần Nguyễn Minh Hiếu | 24110212 | Cấu hình IoT Rule ghi lịch sử vào DynamoDB; hoàn thiện simulator (kết nối lại, log); rà soát IoT Policy; kiểm thử end-to-end | 8 giờ | 8 giờ |
| Nguyễn Trung Kiên | 24110263 | Hoàn thiện DynamoDB, Lambda, API Gateway; xây dựng giao diện web trên S3; thiết lập CloudWatch Logs/Alarm; viết template IaC | 8 giờ | 8 giờ |
| **Tổng cộng** | | | **16 giờ** | **16 giờ** |

> Mỗi sinh viên làm 8 giờ trong tuần 3, đạt mức tối thiểu 8 giờ/tuần theo yêu cầu.

### 1.2. Nhật ký công việc (Worklog)

| Ngày thực hiện | Thành viên | Nội dung công việc | Thời gian |
|---|---|---|---|
| 19/10/2026 – 25/10/2026 | Trần Nguyễn Minh Hiếu | Tạo và kích hoạt IoT Rule lưu Shadow vào DynamoDB; hoàn thiện simulator (ghi log, xử lý kết nối lại); rà soát IoT Policy theo quyền tối thiểu; chạy và kiểm thử simulator 3 thiết bị | 8 giờ |
| 19/10/2026 – 25/10/2026 | Nguyễn Trung Kiên | Hoàn thiện DynamoDB, Lambda, API Gateway; xây dựng và kiểm thử giao diện web trên S3; thiết lập CloudWatch Logs/Alarm; triển khai template CloudFormation | 8 giờ |
| **Tổng cộng** | 2 thành viên | | **16 giờ** |

---

## 2. CHI TIẾT CÔNG VIỆC VÀ MINH CHỨNG TRÊN GITHUB

### 2.1. Trần Nguyễn Minh Hiếu – MSSV: 24110212

#### a. IoT Rule ghi lịch sử thiết bị vào DynamoDB

- IoT Rule lắng nghe topic `$aws/things/+/shadow/update/accepted` và ghi mỗi lần cập nhật Shadow vào bảng DynamoDB.
- Câu truy vấn SQL hiển thị trong cấu hình rule:

```sql
SELECT topic(3) AS deviceId,
       timestamp() AS timestamp,
       'SHADOW_UPDATE' AS eventType,
       state AS state
FROM '$aws/things/+/shadow/update/accepted'
```

- Rule `SaveShadowToDynamoDBRule` ở trạng thái Active, lắng nghe topic `$aws/things/+/shadow/update/accepted` và dùng action DynamoDBv2. Bảng `SmartHomeDeviceHistory` có partition key `deviceId` (String), sort key `timestamp` (Number), chế độ On-demand. Ảnh bản ghi cho thấy các sự kiện `desired` và `reported` được ghi vào bảng. Ảnh cấu hình không hiển thị role của rule nên cần xác nhận role thực tế trong AWS.
- Kiểm thử: cập nhật Shadow từ Console hoặc từ giao diện web → kiểm tra bản ghi mới trong DynamoDB (Explore items).
- Minh chứng: [cấu hình IoT Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png), [cấu hình bảng](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png)

#### b. Hoàn thiện simulator và rà soát IoT Policy

- Mã simulator ghi log có thời gian, xử lý callback ngắt kết nối/kết nối lại và đăng ký lại topic khi phiên MQTT cũ không còn. Log ngày 25/10 ghi nhận cả `smart-light`, `smart-ac`, `smart-fan` nhận `delta` và publish `reported`; log hiện có không ghi nhận một lần ngắt mạng thực tế để xác nhận callback tự kết nối lại.
- Ảnh policy được lưu trong repository với nội dung thể hiện rà soát theo nguyên tắc quyền tối thiểu; JSON policy đầy đủ chưa được lưu trong repository nên chưa thể xác minh từng ARN/action.
- Simulator sử dụng certificate/private key ở đường dẫn `certs/`; `.gitignore` loại trừ thư mục và các phần mở rộng nhạy cảm, không có tệp credential nào được theo dõi trong Git.
- Minh chứng GitHub:
  - Mã nguồn: [src/devices/simulator.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py)
  - Log kiểm thử: [logs/device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log)
  - Ảnh policy: [Iot-policy-least-privilege.png](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png)

### 2.2. Nguyễn Trung Kiên – MSSV: 24110263

#### a. DynamoDB, Lambda và API Gateway

- Bảng DynamoDB vận hành `SmartHomeDeviceHistory`: partition key `deviceId` (String), sort key `timestamp` (Number), chế độ On-demand.
- Lambda `SmartHomeControlFunction` chạy Python 3.12 theo log CloudWatch. Code đọc endpoint từ `IOT_ENDPOINT` (có giá trị mặc định trong mã), đọc tên bảng từ `TABLE_NAME` (mặc định `SmartHomeDeviceHistory`):
  - `POST /devices/{thingName}/control`: kiểm tra tên thiết bị và thuộc tính hợp lệ, cập nhật `desired` lên Device Shadow.
  - `GET /devices/{thingName}/history`: truy vấn tối đa 10 bản ghi lịch sử mới nhất.
  - `GET /devices/{thingName}/shadow`: đọc trạng thái Shadow hiện tại.
- Ảnh kiểm thử Lambda và log cho thấy lời gọi thành công với mã 200. API Gateway endpoint được dùng trong ảnh kiểm thử là `https://xcibzup2li.execute-api.us-east-1.amazonaws.com`; route điều khiển nhận phản hồi `Shadow desired updated`.
- CORS hiện trả `Access-Control-Allow-Origin: *` theo cấu hình mặc định của Lambda; chưa giới hạn về origin của website như dự kiến. Cần cấu hình `ALLOWED_ORIGIN` thành origin cụ thể trước khi xem là hoàn tất bảo mật.
- Lệnh kiểm thử endpoint đã thành công:

```bash
curl -X POST https://xcibzup2li.execute-api.us-east-1.amazonaws.com/devices/smart-light/control \
  -H "Content-Type: application/json" -d '{"power":"ON","brightness":80}'
```

- Minh chứng: [bảng DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png), [kiểm thử Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png), [API Gateway và kết quả curl](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png)
- Mã nguồn: [src/lambda/lambda_function.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/lambda/lambda_function.py)

#### b. Giao diện web trên S3

- Trang tĩnh `web/index.html` được triển khai trên website S3 `iot-smarthome-website`; giao diện gọi API để điều khiển 3 thiết bị và tải lịch sử từ DynamoDB. Ảnh chụp xác nhận trang web mở được và hiển thị kết quả điều khiển/lịch sử.
- Minh chứng: [giao diện web và lịch sử DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [giao diện web](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Web%20IOT%20Smarthome.png)
- Mã nguồn: [web/index.html](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/web/index.html)

#### c. Giám sát CloudWatch và IaC

- Ảnh CloudWatch xác nhận log Lambda xuất hiện trong log group `/aws/lambda/SmartHomeControlFunction`. API Gateway có alarm `SmartHomeAPIGateway5XXAlarm`; không có minh chứng riêng về log group API Gateway.
- Đã tạo alarm `SmartHomeLambdaErrorAlarm` cho metric `Errors` với ngưỡng `>= 1` trong 5 phút và alarm `SmartHomeAPIGateway5XXAlarm` cho lỗi 5XX. Ảnh chụp cho thấy cả hai ở trạng thái OK; chưa có minh chứng gọi lỗi có chủ đích để kiểm tra chuyển trạng thái alarm.
- Template CloudFormation tạo bảng `SmartHomeDeviceHistoryIaC` theo On-demand, có tag Project/Owner và `DeletionPolicy: Retain`. Template này tạo bảng riêng, khác bảng vận hành `SmartHomeDeviceHistory`; không bao gồm Lambda hay IoT Rule.
- Minh chứng: [CloudWatch Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png), [CloudWatch Alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png), [template IaC](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml), [stack CloudFormation](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudformation%20stack%20-%20SmartHomeIaCStack.png)

### 2.3. Ảnh minh chứng tuần 3

#### DynamoDB, Lambda, API Gateway và IaC

**Bảng DynamoDB và bản ghi Shadow**

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png" alt="Bảng DynamoDB SmartHomeDeviceHistory" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png" alt="Các bản ghi Device Shadow trong DynamoDB" width="700">

**IoT Rule lưu Shadow vào DynamoDB**

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png" alt="IoT Rule SaveShadowToDynamoDBRule" width="700">

**Lambda điều khiển thiết bị và kiểm thử**

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Lambda%20SmartHomeControlFunction.png" alt="Lambda SmartHomeControlFunction" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png" alt="Kiểm thử cấu hình Lambda" width="700">

**API Gateway**

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/SmartHomeAPI.png" alt="API Gateway SmartHomeAPI" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png" alt="Kiểm thử API Gateway bằng curl" width="700">

**CloudFormation**

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Cloudformation%20stack%20-%20SmartHomeIaCStack.png" alt="CloudFormation stack SmartHomeIaCStack" width="700">

#### Giao diện web và kiểm thử tích hợp

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Web%20IOT%20Smarthome.png" alt="Giao diện web điều khiển nhà thông minh" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png" alt="Kiểm thử luồng end-to-end từ web đến DynamoDB" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png" alt="Log kiểm thử end-to-end trên PowerShell" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Simulator%203%20devices%20when%20edit%20device%20shadow.png" alt="Simulator kiểm thử ba thiết bị khi cập nhật Device Shadow" width="700">

#### Bảo mật, giám sát và chi phí

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png" alt="IoT Policy theo nguyên tắc quyền tối thiểu" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Git%20security%20check.png" alt="Kiểm tra bảo mật repository trên Git" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png" alt="CloudWatch Logs" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Create%20CloudWatch%20Alarm.png" alt="Tạo CloudWatch Alarm" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png" alt="Danh sách CloudWatch Alarms" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/SmartHomeLambdaErrorAlarm.png" alt="CloudWatch Alarm theo dõi lỗi Lambda" width="700">

<img src="https://raw.githubusercontent.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/main/reports/docs/images/Week3Pic/Billing%20and%20Cost%20Management%20-%20Credit.png" alt="Billing and Cost Management" width="700">

---

## 3. KẾT QUẢ KIỂM THỬ TỪNG THÀNH PHẦN VÀ TÍCH HỢP

| Thành phần | Kịch bản kiểm thử | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|
| DynamoDB | Ghi và đọc bản ghi lịch sử | Bản ghi hiển thị đúng | Đạt: ảnh end-to-end hiển thị sự kiện `desired`/`reported` trong bảng `SmartHomeDeviceHistory`. | [Bản ghi DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png) |
| Lambda | Gửi test event hợp lệ | HTTP 200 | Đạt: ảnh test Lambda hiển thị `statusCode: 200`. Kiểm thử payload không hợp lệ chưa có ảnh/log xác nhận. | [Lambda test](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png) |
| API Gateway | `curl` POST điều khiển đèn | Shadow `desired` được cập nhật | Đạt: endpoint trả `Shadow desired updated`; ảnh có cả các lần gõ lệnh sai trước khi chạy thành công. | [API curl](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png) |
| IoT Rule → DynamoDB | Cập nhật Shadow | Có bản ghi mới trong bảng | Đạt: rule Active dùng DynamoDBv2; ảnh bản ghi cho thấy cập nhật từ Shadow. | [IoT Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png) |
| Simulator (3 thiết bị) | Gửi `desired` cho từng thiết bị | Nhận delta, cập nhật reported | Đạt: log ngày 25/10 ghi nhận cả 3 thiết bị nhận `delta` và publish `reported`. Chưa thấy log mô phỏng mất kết nối để kiểm tra auto-reconnect thực tế. | [Log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log), [ảnh kiểm thử 3 thiết bị](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Simulator%203%20devices%20when%20edit%20device%20shadow.png) |
| Web trên S3 | Điều khiển thiết bị và xem lịch sử | API phản hồi, lịch sử hiển thị | Đạt theo ảnh giao diện và ảnh luồng web–DynamoDB; chưa có ảnh riêng cấu hình hosting/quyền truy cập bucket. | [Giao diện và kết quả](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png) |
| End-to-end | Web → API → Lambda → Shadow → thiết bị → DynamoDB | Toàn bộ luồng chạy đúng | Đạt theo ảnh giao diện/lịch sử và log simulator của ba thiết bị. | [Ảnh end-to-end](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [log PowerShell](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png) |
| CloudWatch | Gọi API và theo dõi Logs/Alarms | Log xuất hiện; alarm có ngưỡng phù hợp | Log Lambda có dữ liệu, hai alarm ở trạng thái OK. Chưa có bằng chứng tạo lỗi có chủ đích để xác nhận alarm chuyển trạng thái. | [Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png), [alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png) |

**Lỗi gặp phải và cách khắc phục:**

| Lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Lệnh `curl` ban đầu dùng URL mẫu `API_URL` hoặc ghép thừa `https://`, khiến shell báo không tìm thấy đường dẫn/không phân giải được host. | URL mẫu chưa được thay bằng endpoint thật; có tiền tố giao thức bị lặp. | Dùng endpoint `https://xcibzup2li.execute-api.us-east-1.amazonaws.com` đúng một lần; lệnh POST sau đó trả về `Shadow desired updated`. |

> Các kiểm thử chưa có bằng chứng trực tiếp (payload không hợp lệ, auto-reconnect khi mất mạng và alarm khi có lỗi) được chuyển sang kế hoạch tuần 4.

---

## 4. QUẢN LÝ TÀI NGUYÊN, BẢO MẬT VÀ CHI PHÍ

- **Tag:** template CloudFormation khai báo `Project = SmartHomeIoT`, `Owner1 = SV24110212`, `Owner2 = SV24110263`; ảnh tuần 2 cũng ghi nhận tag trên IoT Policy. Chưa có bằng chứng các tag đã được áp dụng cho mọi tài nguyên tuần 3.
- **Region:** ảnh AWS cho thấy sử dụng `us-east-1`. Execution role của Lambda và IoT Rule cần đối chiếu trực tiếp trên AWS; mã nguồn/ảnh hiện có không xác nhận các role.
- **Bảo mật:** `.gitignore` loại trừ `certs/`, `*.pem`, `*.key`, `*.crt`, `.env`. Kiểm tra repository hiện tại và lịch sử Git không tìm thấy các tệp khớp các mẫu này. Ảnh IoT Policy có minh chứng rà soát least privilege nhưng JSON đầy đủ chưa lưu trong repository. Lambda kiểm tra tên thiết bị và thuộc tính; CORS hiện mặc định `*`, cần thu hẹp về origin website.
- **Tài nguyên đang chạy cuối tuần:** chưa có ảnh inventory hoặc trạng thái hiện tại để xác nhận. Ảnh ngày 25/10 ghi nhận IoT Rule Active, CloudFormation stack `CREATE_COMPLETE`, DynamoDB Active và hai alarm ở trạng thái OK; trạng thái hiện tại có thể đã thay đổi.
- **Tài nguyên đã dừng/xóa sau buổi làm:** chưa có nhật ký xác nhận.
- **Chi phí tuần 3:** chưa xác định được từ ảnh hiện có. Ảnh Billing hiển thị số credit còn lại và đã dùng đều là `$0.00`; đây không phải báo cáo chi phí dịch vụ tuần 3. Cần lấy số liệu từ Bills/Cost Explorer.
- Minh chứng: [CloudFormation tags](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml), [ảnh kiểm tra Git](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git%20security%20check.png), [ảnh Billing Credits](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Billing%20and%20Cost%20Management%20-%20Credit.png).

---

## 5. KHAI BÁO SỬ DỤNG AI

### 5.1. Công cụ và phạm vi sử dụng

**Công cụ 1: AI assistant sử dụng Copilot SDK trong VS Code**

- **Mô hình:** tên model không được hiển thị trong thông tin phiên làm việc, nên không ghi suy đoán.
- **Mục đích:** thêm ảnh minh chứng vào báo cáo tuần 3 và hỗ trợ sửa lỗi mã nguồn.
- **Yêu cầu đã gửi:** “thêm ảnh week3 vào BaoCaoTuan3”; “Xoá phần 1 và điền vô các phần còn thiếu”; các yêu cầu hỗ trợ gỡ lỗi mã nguồn khi chạy thử.

**Công cụ 2: Claude (Anthropic, claude.ai)**

- **Mô hình:** Claude Sonnet 5.5.
- **Mục đích:** hỗ trợ dựng khung báo cáo theo mẫu tuần 1–2, kiểm tra các mục còn thiếu và định dạng báo cáo (Markdown/Word).
- **Yêu cầu đã gửi:** “dựa vào báo cáo mẫu tuần 1 làm cho tôi tuần 2”; “tiếp tục các format đó làm cho tôi tuần 3”; “Cho tôi 1 bản word”; các yêu cầu rà soát và sửa link.

### 5.2. Nội dung AI hỗ trợ và phần sinh viên thực hiện

- AI chỉ hỗ trợ thêm ảnh vào báo cáo, sửa lỗi mã nguồn và định dạng báo cáo.
- Sinh viên tự tạo và cấu hình tài nguyên AWS, chạy simulator, kiểm thử, chụp ảnh minh chứng và kiểm tra lại mã nguồn sau khi sửa lỗi.
- Các nội dung không thể xác thực bằng repository (role AWS thực tế, chi phí dịch vụ, tài nguyên đã dọn dẹp, tên model của công cụ thứ nhất) được ghi rõ là chưa có dữ liệu, không tự điền số liệu.


### 5.3. Minh chứng chỉnh sửa báo cáo

- File báo cáo: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md
- Danh sách commit: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main
- Các commit cụ thể của tuần 3:
  - [edb9c38 – Them BaoCaoTuan2](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/edb9c38405cb0756de4daf6d300b9dae5d088ef5)
  - [d18ae53 – Merge pull request #2 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/d18ae5386723f10c58eb91aec57befbc511809e6)
  - [0649b6b – Add Week3 Screenshots](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/0649b6b7499274161b6ee367ec071ad009b8f5d2)
  - [cb92671 – Merge pull request #1 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/cb92671730fa4d3915139db389edc176cdc42480)
  - [38111a7 – Cau hinh IoT Rule DynamoDB, nang cap simulator auto-reconnect va IoT Policy quyen toi thieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/38111a700964a0b3d9c643fcfadb27dc31634c48)

---

## 6. KẾT LUẬN VÀ KẾ HOẠCH CÔNG VIỆC TUẦN 4

### 6.1. Kết luận tuần 3

Tuần 3 đã có minh chứng cho DynamoDB lưu lịch sử Shadow, IoT Rule, Lambda điều khiển thiết bị, API Gateway, giao diện web trên S3 và luồng end-to-end với ba simulator. CloudWatch Logs hiển thị log Lambda; hai alarm đã được tạo và ở trạng thái OK tại thời điểm chụp. Template CloudFormation triển khai thành công một bảng DynamoDB riêng. Các nội dung còn cần hoàn tất/xác nhận gồm chi phí thực tế, trạng thái tài nguyên cuối tuần, role AWS, kiểm thử lỗi làm alarm chuyển trạng thái, kiểm thử auto-reconnect thực tế, JSON policy đầy đủ và thu hẹp CORS khỏi `*`.

### 6.2. Kế hoạch công việc tuần 4

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

## 7. DANH MỤC MINH CHỨNG TRÊN GITHUB

- Repository chính: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
- Báo cáo tuần 3: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md
- Sơ đồ kiến trúc: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/architecture-diagram.png
- Cấu hình bảo vệ tệp nhạy cảm: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/.gitignore
- Mã nguồn thiết bị giả lập: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py
- Mã nguồn Lambda: [src/lambda/lambda_function.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/lambda/lambda_function.py)
- Mã nguồn giao diện web: [web/index.html](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/web/index.html)
- Template IaC: [iac/template.yaml](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml)
- Ảnh chụp minh chứng: [thư mục reports/docs/images/Week3Pic](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/tree/main/reports/docs/images/Week3Pic)
- Lịch sử commit: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main
- Commit cụ thể của tuần 3: xem mục 5.3.
  - [edb9c38 – Them BaoCaoTuan2](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/edb9c38405cb0756de4daf6d300b9dae5d088ef5)
  - [d18ae53 – Merge pull request #2 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/d18ae5386723f10c58eb91aec57befbc511809e6)
  - [0649b6b – Add Week3 Screenshots](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/0649b6b7499274161b6ee367ec071ad009b8f5d2)
  - [cb92671 – Merge pull request #1 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/cb92671730fa4d3915139db389edc176cdc42480)
  - [38111a7 – Cau hinh IoT Rule DynamoDB, nang cap simulator auto-reconnect va IoT Policy quyen toi thieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/38111a700964a0b3d9c643fcfadb27dc31634c48)
