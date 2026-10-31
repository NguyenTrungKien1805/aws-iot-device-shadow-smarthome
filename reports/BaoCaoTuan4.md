# BÁO CÁO TIẾN ĐỘ TUẦN 4 – ĐỀ TÀI: NHÀ THÔNG MINH ĐIỀU KHIỂN THIẾT BỊ GIẢ LẬP QUA AWS IoT CORE

**Môn học:** Cloud – Đợt 1 – Năm học 2026–2027
**Nhóm:** Integration & IoT
**Giảng viên hướng dẫn:** TS. Huỳnh Xuân Phụng
**Thời gian báo cáo:** 26/10/2026 – 01/11/2026
**GitHub Repository (Public):** https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
**Báo cáo tuần 4:** [reports/BaoCaoTuan4.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan4.md)
**Sơ đồ kiến trúc hệ thống:** [reports/docs/architecture-diagram.png](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/architecture-diagram.png)
**Video demo (≤ 10 phút):** https://www.youtube.com/watch?v=xsARCcqz1pI

---

## 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ SỐ GIỜ LÀM VIỆC

### 1.1. Phân công nhiệm vụ

| Thành viên | MSSV | Vai trò và nhiệm vụ chính | Số giờ cá nhân | Tổng số giờ |
|---|---|---|---|---|
| Trần Nguyễn Minh Hiếu | 24110212 | Kiểm thử tổng thể 3 thiết bị; hoàn thiện simulator và hướng dẫn chạy; rà soát bảo mật IoT Policy; viết phần báo cáo cuối về IoT Core, Device Shadow, bảo mật; chuẩn bị kịch bản demo | 8 giờ | 8 giờ |
| Nguyễn Trung Kiên | 24110263 | Thống kê và tối ưu chi phí; dọn dẹp tài nguyên; hoàn thiện báo cáo cuối (kiến trúc, chi phí, kiểm thử); quay và dựng video demo | 8 giờ | 8 giờ |
| **Tổng cộng** | | | **16 giờ** | **16 giờ** |

> Mỗi sinh viên làm 8 giờ trong tuần 4, đạt mức tối thiểu 8 giờ/tuần theo yêu cầu.

### 1.2. Nhật ký công việc (Worklog)

| Ngày thực hiện | Thành viên | Nội dung công việc | Thời gian |
|---|---|---|---|
| 27/10/2026 | Trần Nguyễn Minh Hiếu | Kiểm thử simulator 3 thiết bị, kiểm thử payload không hợp lệ (API trả HTTP 400), kiểm thử tự kết nối lại | 3 giờ |
| 28/10/2026 | Trần Nguyễn Minh Hiếu | Rà soát IoT Policy theo quyền tối thiểu; viết hướng dẫn chạy simulator | 1,5 giờ |
| 29/10/2026 | Trần Nguyễn Minh Hiếu | Viết phần báo cáo cuối về IoT Core, Device Shadow, MQTT và bảo mật | 2 giờ |
| 30/10/2026 | Trần Nguyễn Minh Hiếu | Soạn kịch bản demo và diễn tập | 1,5 giờ |
| 27/10/2026 | Nguyễn Trung Kiên | Xem Billing, thống kê chi phí và rà soát tối ưu chi phí | 1,5 giờ |
| 28/10/2026 | Nguyễn Trung Kiên | Thu hẹp CORS (Lambda và API Gateway), kiểm thử CloudWatch Alarm bằng lỗi có chủ đích | 2 giờ |
| 30/10/2026 | Nguyễn Trung Kiên | Quay và dựng video demo | 3 giờ |
| 31/10/2026 | Nguyễn Trung Kiên | Chuẩn bị quy trình dọn dẹp tài nguyên sau demo (thứ tự xóa, lệnh CLI) và cập nhật báo cáo | 1,5 giờ |
| **Tổng cộng** | 2 thành viên | | **16 giờ** |

---

## 2. CHI TIẾT CÔNG VIỆC VÀ MINH CHỨNG TRÊN GITHUB

Tuần 3 còn một số nội dung chưa có minh chứng trực tiếp. Tuần 4 hoàn thiện các nội dung này trước khi kiểm thử tổng thể và dọn dẹp. Hạng mục nào chưa có ảnh hoặc log trong repository thì được ghi rõ là chưa có minh chứng.

### 2.1. Trần Nguyễn Minh Hiếu – MSSV: 24110212

#### a. Hoàn thiện kiểm thử simulator và bảo mật

- **Kiểm thử auto-reconnect thực tế:** ngắt kết nối mạng trong thời gian ngắn, sau đó xác nhận simulator tự kết nối lại mà không cần chạy lại chương trình. Minh chứng: [ảnh simulator tự kết nối lại](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/auto_connect.png); log kiểm thử: [logs/device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log).
- **Kiểm thử payload không hợp lệ:** gửi `desired` ngoài khoảng cho phép (ví dụ `brightness = 500`). Kết quả: API từ chối giá trị ngoài khoảng ([HTTP 400](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/payload_loi.png)) và simulator xử lý không bị lỗi, tiếp tục hoạt động; log kiểm thử simulator lưu trong [logs/device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log).
- **IoT Policy:** rà soát theo nguyên tắc quyền tối thiểu (giới hạn theo tên Thing, chỉ topic Shadow cần dùng). Minh chứng: [JSON policy SmartHomeDevicePolicy](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png) (ảnh tuần 3 hiển thị policy giới hạn theo Thing/topic). Nội dung policy lưu trong repository: [iac/iot-policy.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/iot-policy.json).
- **Hướng dẫn chạy simulator:** chuẩn bị certificate trong thư mục `certs/` (không đưa lên Git), đặt biến môi trường `IOT_ENDPOINT`, chạy `python src/devices/simulator.py`. Xem thêm [README.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/README.md).
- **Dữ liệu mẫu kiểm thử Device Shadow:** [shadow-desired-smart-light.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-light.json), [shadow-desired-smart-ac.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-ac.json), [shadow-desired-smart-fan.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-fan.json).
- Mã nguồn: [src/devices/simulator.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py)

#### b. Phần báo cáo cuối và kịch bản demo

- Phần báo cáo cuối về AWS IoT Core, Device Shadow, MQTT và bảo mật thiết bị được tổng hợp ở mục 6 và 7 của báo cáo này.
- Kịch bản demo (≤ 10 phút), thể hiện trong [video demo](https://www.youtube.com/watch?v=xsARCcqz1pI):
  1. Giới thiệu kiến trúc (sơ đồ kiến trúc).
  2. Chạy simulator 3 thiết bị, hiện log kết nối.
  3. Điều khiển từ giao diện web: bật/tắt và chỉnh thông số từng thiết bị.
  4. Cho thấy Device Shadow (`desired`/`reported`) trên Console đổi theo.
  5. Cho thấy lịch sử trong DynamoDB và log CloudWatch.
  6. Nêu ngắn gọn chi phí, bảo mật và phần dọn dẹp tài nguyên.

### 2.2. Nguyễn Trung Kiên – MSSV: 24110263

#### a. Tối ưu chi phí và thống kê chi phí sử dụng

- Ảnh [Billing overview tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/billing.png) hiển thị **$0.04 month-to-date**. Ảnh chưa có chi tiết theo dịch vụ (IoT Core, Lambda, API Gateway, DynamoDB, S3, CloudWatch, CloudFormation), nên chưa chốt được tổng chi phí cuối kỳ theo từng dịch vụ.
- Các biện pháp tối ưu: dùng kiến trúc serverless trả theo lượt dùng, DynamoDB chế độ On-demand, không dùng EC2 hay tài nguyên chạy liên tục.
- Ảnh [Credits tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Billing%20and%20Cost%20Management%20-%20Credit.png) chỉ hiển thị credit (`$0.00`), không phải báo cáo chi phí dịch vụ hoặc số dư credit cuối kỳ.

#### b. Hoàn thiện bảo mật API và giám sát

- **CORS:** đã thu hẹp origin từ `*` về địa chỉ website S3 `http://iot-smarthome-website.s3-website-us-east-1.amazonaws.com`. Lambda trả `Access-Control-Allow-Origin` đúng origin này ([ảnh kiểm thử Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/lambda_hoanthien.jpg)) và API Gateway cấu hình CORS với cùng origin, các method `GET`, `POST`, `OPTIONS` và header `content-type` ([ảnh cấu hình CORS API Gateway](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/Cors.jpg)).
- **Bảo vệ endpoint:** ảnh [cấu hình route API tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeAPI.png) chỉ xác nhận các route tồn tại, không chứng minh đã bật throttling hoặc xác thực.
- **CloudWatch Alarm:** đã kiểm thử bằng lỗi có chủ đích: alarm chuyển sang ALARM khi có lỗi và trở lại OK sau đó. Minh chứng: [alarm ở trạng thái ALARM tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/alarm.png) và [alarm ở trạng thái OK](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeLambdaErrorAlarm.png). Hai ảnh được chụp ở các thời điểm khác nhau, không phải một chuỗi liên tục.
- Mã nguồn: [src/lambda/lambda_function.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/lambda/lambda_function.py)
- **Dữ liệu kiểm thử Lambda:** [tests/lambda-test-event.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/lambda-test-event.json).
- **Chính sách bucket S3 cho website tĩnh:** [iac/s3-bucket-policy.json](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/s3-bucket-policy.json).

#### c. Dọn dẹp tài nguyên

Thứ tự dọn dẹp áp dụng sau khi quay xong video demo và chụp đủ minh chứng:

1. CloudWatch Alarms và log group của Lambda.
2. API Gateway (xóa API).
3. Lambda `SmartHomeControlFunction`.
4. IoT Rule `SaveShadowToDynamoDBRule`.
5. IoT Things, certificate (hủy kích hoạt và gỡ khỏi Thing/policy trước khi xóa) và IoT Policy.
6. Bucket S3 `iot-smarthome-website` (xóa hết object trước khi xóa bucket).
7. CloudFormation stack `SmartHomeIaCStack`. Bảng `SmartHomeDeviceHistoryIaC` có `DeletionPolicy: Retain` nên **vẫn còn sau khi xóa stack và phải xóa thủ công**.
8. Bảng DynamoDB `SmartHomeDeviceHistory` và `SmartHomeDeviceHistoryIaC`.

Ví dụ lệnh AWS CLI (kiểm tra tên và ID thực tế trước khi chạy):

```bash
aws cloudwatch delete-alarms --alarm-names SmartHomeLambdaErrorAlarm SmartHomeAPIGateway5XXAlarm
aws apigatewayv2 delete-api --api-id <api-id>
aws lambda delete-function --function-name SmartHomeControlFunction
aws iot delete-topic-rule --rule-name SaveShadowToDynamoDBRule
aws s3 rm s3://iot-smarthome-website --recursive
aws s3api delete-bucket --bucket iot-smarthome-website
aws cloudformation delete-stack --stack-name SmartHomeIaCStack
aws dynamodb delete-table --table-name SmartHomeDeviceHistory
aws dynamodb delete-table --table-name SmartHomeDeviceHistoryIaC
```

- Hiện chưa có ảnh inventory trước và sau dọn dẹp trong repository nên chưa xác nhận được kết quả dọn dẹp.

### 2.3. Ảnh minh chứng

- Kiểm thử auto-reconnect: [simulator tự kết nối lại](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/auto_connect.png)
- Kiểm thử payload ngoài khoảng: [API từ chối `brightness = 500` (HTTP 400)](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/payload_loi.png); log simulator trong [logs/device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log)
- Nội dung IoT Policy: [ảnh policy quyền tối thiểu tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png)
- Cấu hình CORS sau khi thu hẹp: [Lambda trả origin website S3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/lambda_hoanthien.jpg), [cấu hình CORS API Gateway](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/Cors.jpg)
- CloudWatch Alarm: [alarm OK tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeLambdaErrorAlarm.png) và [alarm ALARM tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/alarm.png)
- Billing: [Billing overview ($0.04 month-to-date)](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/billing.png)
- Luồng end-to-end: [giao diện web và lịch sử DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png)
- Dọn dẹp tài nguyên: chưa có ảnh inventory sau dọn dẹp.

---

## 3. KẾT QUẢ KIỂM THỬ TỔNG THỂ

| Thành phần | Kịch bản kiểm thử | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|
| End-to-end | Web → API Gateway → Lambda → Shadow → simulator → DynamoDB, lần lượt cho 3 thiết bị | Cả 3 thiết bị đổi trạng thái, lịch sử được ghi | Đạt ở tuần 3 theo ảnh web–DynamoDB và log simulator; chưa có ảnh xác nhận đủ cả 3 thiết bị trong cùng một lượt kiểm thử | [Web/DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png) |
| Lambda | Payload hợp lệ / không hợp lệ | 200 / 400 | Đạt: 200 với payload hợp lệ (tuần 3) và 400 khi `brightness = 500` (tuần 4) | [Lambda 200](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png), [API 400](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/payload_loi.png) |
| Simulator | Mất kết nối rồi kết nối lại | Tự kết nối lại, tiếp tục nhận `delta` | Đạt: simulator tự kết nối lại sau khi mất kết nối, theo ảnh kiểm thử tuần 4 | [Ảnh auto-connect](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/auto_connect.png), [log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log) |
| Simulator | `desired` sai kiểu hoặc ngoài khoảng | Không crash; trạng thái hợp lệ được giữ | Đạt: API từ chối giá trị ngoài khoảng (HTTP 400) và simulator hoạt động bình thường theo log kiểm thử | [HTTP 400](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/payload_loi.png), [log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log) |
| IoT Rule | Nhiều lần cập nhật liên tiếp | Mỗi lần cập nhật có 1 bản ghi | Đạt ở tuần 3: rule hoạt động và bảng có bản ghi `desired`/`reported` | [Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png) |
| CORS | Gọi API từ website S3 và từ origin khác | Origin website được phép; origin khác bị chặn | Đạt: CORS đã thu hẹp từ `*` về origin website S3 ở cả Lambda và API Gateway; chưa có ảnh gọi thử từ origin khác | [Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/lambda_hoanthien.jpg), [API Gateway](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/Cors.jpg) |
| CloudWatch Alarm | Gọi Lambda gây lỗi có chủ đích | Alarm chuyển ALARM rồi về OK | Đạt: alarm chuyển ALARM khi có lỗi và trở về OK; hai ảnh minh chứng chụp ở các thời điểm khác nhau | [OK](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeLambdaErrorAlarm.png), [ALARM](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/alarm.png) |
| Bảo mật repository | Tìm `*.pem`, `*.key`, `*.crt`, `.env` trong repo và lịch sử Git | Không có tệp nhạy cảm | Đạt theo ảnh kiểm tra tuần 3; cần chạy lại trước khi kết luận cuối kỳ | [Kiểm tra Git](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git%20security%20check.png) |

**Lỗi gặp phải và cách khắc phục:**

| Lỗi | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Lệnh `curl` dùng URL mẫu `API_URL` hoặc ghép thừa `https://`, shell báo không tìm thấy đường dẫn/không phân giải được host. | URL mẫu chưa được thay bằng endpoint thật; tiền tố giao thức bị lặp. | Dùng đúng endpoint API Gateway một lần; lệnh POST sau đó trả về `Shadow desired updated`. |
| Giá trị `brightness = 500` ngoài khoảng cho phép. | Dữ liệu đầu vào không hợp lệ. | Lambda kiểm tra giá trị và trả HTTP 400, không cập nhật Shadow. |

> Hạng mục nào chưa có đủ bằng chứng được ghi rõ trong mục hạn chế, không đánh dấu "đạt".

---

## 4. CHI PHÍ, TÀI NGUYÊN VÀ BẢO MẬT CUỐI KỲ

- **Chi phí sử dụng cuối kỳ:** ảnh [Billing overview](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week4Pic/billing.png) hiển thị **$0.04 month-to-date**; chưa có chi tiết theo dịch vụ từ Bills/Cost Explorer. Credit còn lại chưa được xác nhận bằng ảnh cuối kỳ (ảnh [Credits tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Billing%20and%20Cost%20Management%20-%20Credit.png) là ảnh tuần trước).
- **Tag:** tài nguyên gắn `Project = SmartHomeIoT`, `Owner1 = SV24110212`, `Owner2 = SV24110263` (với dịch vụ hỗ trợ tag). Minh chứng tiêu biểu: tag trên [Thing smart-ac](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/smart-ac%20Attributes.png), [IoT Policy](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/SmartHomeDevicePolicy%20Tags.png) và [bucket S3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week1Pic/s3-tags.png).
- **Region và quyền:** chỉ dùng `us-east-1`; dùng LabRole/LabInstanceProfile, không tạo IAM user/role. Ảnh [LabRole](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week1Pic/iam-labrole.png) và [IoT endpoint Data-ATS](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/iot%20Data-ATS.png) là minh chứng tuần trước; chưa có ảnh xác nhận role đang gán cho Lambda và IoT Rule.
- **Bảo mật:** `.gitignore` loại trừ `certs/`, `*.pem`, `*.key`, `*.crt`, `.env`. Ảnh [kiểm tra Git tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git%20security%20check.png) cho thấy lệnh tìm tệp nhạy cảm không trả kết quả.

---

## 5. KHAI BÁO SỬ DỤNG AI

### 5.1. Công cụ và phạm vi sử dụng

**Công cụ: Claude (Anthropic, claude.ai)**

- **Mô hình:** Claude Sonnet 5.5.
- **Mục đích:** Hỗ trợ sửa đổi mã nguồn khi gặp lỗi lúc chạy thử; rà soát các mục còn thiếu minh chứng.
- **Yêu cầu đã gửi:** Các yêu cầu hỗ trợ sửa lỗi mã nguồn của dự án

### 5.2. Nội dung AI hỗ trợ và phần sinh viên thực hiện

- **AI hỗ trợ:** Sửa đổi mã nguồn theo lỗi phát sinh khi chạy thử; rà soát và gợi ý cách trình bày các hạng mục chưa có minh chứng; định dạng danh sách link commit.
- **Sinh viên tự thực hiện:** Tự viết và chủ động quản lý nội dung file báo cáo, tạo và cấu hình tài nguyên AWS, chạy lại và kiểm thử mã sau khi sửa, chụp ảnh minh chứng, quay video demo, kiểm tra kết quả và giải thích được mã nguồn khi vấn đáp.
- Số liệu, ảnh, log và kết quả kiểm thử trong báo cáo lấy từ repository và AWS Console; hạng mục không có bằng chứng được ghi rõ là chưa có.


### 5.3. Minh chứng chỉnh sửa báo cáo

- File báo cáo: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan4.md
- Danh sách commit tuần 4 (xếp từ cũ đến mới):
  - [ce1e5b1 – Thêm thư mục ảnh và các ảnh tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/ce1e5b1) – NguyenTrungKien1805
  - [9c3138a – Thêm BaoCaoTuan4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/9c3138a) – NguyenTrungKien1805
  - [da73d2f – Cap nhat log sau khi chay demo](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/da73d2f) – 24110212-TranNguyenMinhHieu
  - [8954522 – Merge pull request #3 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/8954522) – TranNguyenMinhHieu006
  - [e6d4c19 – add JSON files and simplify simulator startup message](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/e6d4c19) – 24110212-TranNguyenMinhHieu
  - [c9f20b7 – Thêm các file JSON và rít gọn dòng thông báo khởi động khi chạy simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/c9f20b7) – TranNguyenMinhHieu006
  - [7474253 – Thêm ảnh báo cáo tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/7474253) – NguyenTrungKien1805
  - [b2628ae – Cap nhat tai lieu README.md huong dan chi tiet toan bo he thong Smart Home IoT](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/b2628ae) – 24110212-TranNguyenMinhHieu
  - [baf44fb – Cập nhật tài liệu README.md hướng dẫn chi tiết cho hệ thống SmarthomeIoT](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/baf44fb) – TranNguyenMinhHieu006
  - [dc5ac1a – Update README.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/dc5ac1a) – TranNguyenMinhHieu006
  - [12860a2 – Fix image link in README.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/12860a2) – NguyenTrungKien1805
  - [ad0e1d3 – Thêm ảnh vào tuần 4](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/ad0e1d3) – NguyenTrungKien1805
  - [17aef93 – Merge branch 'main' of https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/17aef93) – NguyenTrungKien1805
  - [b270edd – Update README.md](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/b270edd) – TranNguyenMinhHieu006
  - [2763df2 – Merge branch 'main' of https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/2763df2) – NguyenTrungKien1805
---

## 6. TỔNG KẾT ĐỀ TÀI SAU 4 TUẦN

Đối chiếu với sản phẩm dự kiến trong đề cương:

- **≥ 3 thing giả lập (Python SDK) dùng certificate:** 3 Thing `smart-light`, `smart-ac`, `smart-fan` với certificate Active và IoT Policy; simulator tại [src/devices/simulator.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py). Minh chứng: [danh sách Thing](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/Things.png), [certificate smart-light](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/smart-light%20Certificates.png).
- **Device Shadow:** luồng `desired` → `delta` → `reported` đã kiểm thử với simulator; ảnh [cập nhật Shadow smart-light](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week2Pic/Update%20Device%20shadow%20document%20c%E1%BB%A7a%20smart-light.png) và [log simulator tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Simulator%203%20devices%20when%20edit%20device%20shadow.png).
- **Web điều khiển qua API Gateway + Lambda cập nhật Shadow:** trang web trên S3, API Gateway, Lambda `SmartHomeControlFunction`. Minh chứng tuần 3: [giao diện web/lịch sử DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [route API](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeAPI.png), [kiểm thử Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png).
- **IoT Rule lưu lịch sử vào DynamoDB:** rule `SaveShadowToDynamoDBRule` ghi vào bảng `SmartHomeDeviceHistory`. Minh chứng tuần 3: [cấu hình Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png).
- **Không public private key lên Git:** `.gitignore` và ảnh [kiểm tra Git](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git%20security%20check.png).
- **Giám sát và IaC:** [CloudWatch Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png), [CloudWatch Alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png) và [CloudFormation stack](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudformation%20stack%20-%20SmartHomeIaCStack.png); các ảnh này ghi nhận trạng thái tuần 3.

**Hạn chế và hướng phát triển:**

- Endpoint API chưa có xác thực hoặc throttling; chưa có ảnh gọi thử từ một origin khác để xác nhận bị chặn.
- CloudWatch Alarm chưa có thông báo SNS khi kích hoạt; ảnh alarm OK và ALARM được chụp ở hai thời điểm khác nhau.
- IaC mới bao phủ bảng DynamoDB, chưa gồm Lambda, API Gateway và IoT Rule.
- Chưa có báo cáo chi phí theo dịch vụ và ảnh inventory sau dọn dẹp.

---

## 7. KẾT LUẬN

Sau 4 tuần, nhóm đã xây dựng và chạy được luồng điều khiển nhà thông minh trên AWS Learner Lab: 3 thiết bị giả lập kết nối AWS IoT Core bằng certificate, đồng bộ trạng thái qua Device Shadow, điều khiển từ giao diện web trên S3 qua API Gateway và Lambda, và lưu lịch sử vào DynamoDB thông qua IoT Rule. Hệ thống có giám sát CloudWatch, IaC cho bảng DynamoDB và không đưa chứng chỉ hoặc private key lên GitHub.

Trong tuần 4, nhóm bổ sung kiểm thử payload ngoài khoảng (API trả HTTP 400), ghi nhận chi phí ở mức $0.04 month-to-date và quay video demo. Các nội dung chưa có đủ minh chứng gồm chi phí theo dịch vụ và kết quả dọn dẹp tài nguyên; các nội dung này được ghi rõ ở mục 6 và là hướng hoàn thiện tiếp theo. Bài học chính là cần kiểm tra quyền thực tế của Learner Lab, giới hạn quyền truy cập ngay từ đầu và lưu minh chứng đầy đủ trong khi triển khai.

---

## 8. DANH MỤC MINH CHỨNG TRÊN GITHUB

- Repository chính: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome
- Báo cáo tuần 4: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan4.md
- Sơ đồ kiến trúc: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/architecture-diagram.png
- Cấu hình bảo vệ tệp nhạy cảm: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/.gitignore
- Mã nguồn thiết bị giả lập: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py
- Mã nguồn Lambda: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/lambda/lambda_function.py
- Mã nguồn giao diện web: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/web/index.html
- Template IaC: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml
- IoT Policy (SmartHomeDevicePolicy): https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/iot-policy.json
- Chính sách bucket S3: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/s3-bucket-policy.json
- Dữ liệu kiểm thử Lambda: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/lambda-test-event.json
- Dữ liệu mẫu Device Shadow: [smart-light](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-light.json), [smart-ac](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-ac.json), [smart-fan](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/tests/shadow-desired-smart-fan.json)
- Log simulator: [device_simulator.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator.log), [device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log)
- Tài liệu dự án: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/README.md
- Ảnh minh chứng tuần 4: [thư mục reports/docs/images/Week4Pic](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/tree/main/reports/docs/images/Week4Pic)
- Báo cáo các tuần trước: [Tuần 1](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan1.md), [Tuần 2](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan2.md), [Tuần 3](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md)
- Video demo: https://www.youtube.com/watch?v=xsARCcqz1pI
- Lịch sử commit: https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main