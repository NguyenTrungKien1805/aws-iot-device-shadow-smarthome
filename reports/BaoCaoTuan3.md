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

### 1.2. Nhật ký công việc (Worklog)

| Ngày thực hiện | Thành viên | Nội dung công việc | Thời gian |
|---|---|---|---|
| 19/10/2026 – 25/10/2026 | Trần Nguyễn Minh Hiếu | Tạo và kích hoạt IoT Rule lưu Shadow vào DynamoDB; hoàn thiện simulator (ghi log, xử lý kết nối lại); rà soát IoT Policy theo quyền tối thiểu; chạy và kiểm thử simulator 3 thiết bị | 8 giờ |
| 19/10/2026 – 25/10/2026 | Nguyễn Trung Kiên | Hoàn thiện DynamoDB, Lambda, API Gateway; xây dựng và kiểm thử giao diện web trên S3; thiết lập CloudWatch Logs/Alarm; triển khai template CloudFormation | 8 giờ |
| **Tổng cộng** | 2 thành viên | | **16 giờ** |

---

## 2. CHI TIẾT CÔNG VIỆC VÀ MINH CHỨNG TRÊN GITHUB

### 2.1. Trần Nguyễn Minh Hiếu – MSSV: 24110212

#### a. Cấu hình IoT Rule lưu lịch sử trạng thái vào DynamoDB

- Thiết lập rule `SaveShadowToDynamoDBRule` trên AWS IoT Core ở trạng thái Active để bắt các bản tin cập nhật thành công từ Device Shadow qua topic `$aws/things/+/shadow/update/accepted`.

- Câu truy vấn SQL cấu hình trong rule để trích xuất tên thiết bị từ topic thứ 3, thời gian hệ thống và dữ liệu `state`:

```sql
SELECT topic(3) AS deviceId,
       timestamp() AS timestamp,
       'SHADOW_UPDATE' AS eventType,
       state AS state
FROM '$aws/things/+/shadow/update/accepted'
```

- Rule sử dụng action **DynamoDBv2** để tách các trường trong kết quả truy vấn và đẩy trực tiếp vào bảng `SmartHomeDeviceHistory` (Partition key: `deviceId` kiểu String, Sort key: `timestamp` kiểu Number, chế độ On-demand).

- Thực hiện kiểm thử bằng cách thay đổi trạng thái Shadow từ giao diện web và AWS Console, sau đó vào mục **Explore items** trên DynamoDB kiểm tra: các bản ghi chứa cả phần `desired` và `reported` đều đã được lưu thành công theo đúng mốc thời gian. (Lưu ý: ảnh chụp màn hình cấu hình rule hiện chưa chụp phần IAM Role gắn kèm, nhóm sẽ bổ sung kiểm tra đối chiếu `LabRole` trong tuần 4).

- Minh chứng: [cấu hình IoT Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png), [cấu hình bảng](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png)

#### b. Nâng cấp mã nguồn Simulator và rà soát bảo mật IoT Policy

- Cập nhật file `src/devices/simulator.py`: bổ sung ghi log kèm timestamp chi tiết ra file và console; viết thêm các hàm callback xử lý sự kiện mất kết nối (`on_connection_interrupted`) và khôi phục kết nối (`on_connection_resumed`), tự động subscribe lại các topic Shadow khi phiên MQTT cũ bị hủy.

- Chạy kiểm thử đồng thời 3 thiết bị giả lập (`smart-light`, `smart-ac`, `smart-fan`) vào ngày 25/10: cả 3 thiết bị đều nhận được bản tin `delta` khi điều khiển và gửi phản hồi `reported` về AWS IoT Core. Do trong buổi chạy thử mạng ổn định nên log chưa ghi nhận tình huống rớt mạng thực tế; kịch bản ngắt mạng chủ động để test callback kết nối lại sẽ được thực hiện ở tuần 4.

- Rà soát lại IoT Policy trên AWS IoT Core theo nguyên tắc quyền tối thiểu (least privilege), giới hạn các quyền `iot:Connect`, `iot:Publish`, `iot:Subscribe`, `iot:Receive` theo đúng nhóm thiết bị của dự án.

- Kiểm tra bảo mật mã nguồn: các chứng chỉ và khóa bí mật trong thư mục `certs/` cùng các đuôi file `*.pem`, `*.key`, `*.crt` đã được chặn trong `.gitignore`, đảm bảo không bị đẩy lên GitHub.

- Minh chứng mã nguồn: [src/devices/simulator.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/devices/simulator.py)

- Minh chứng log kiểm thử: [logs/device_simulator_week3.log](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log)

- Minh chứng ảnh policy: [Iot-policy-least-privilege.png](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png)

### 2.2. Nguyễn Trung Kiên – MSSV: 24110263

#### a. Xây dựng DynamoDB, hàm Lambda và API Gateway

- Khởi tạo bảng chính `SmartHomeDeviceHistory` trên DynamoDB với khóa chính `deviceId` (String) và khóa sắp xếp `timestamp` (Number), chọn chế độ tính phí On-demand để tiết kiệm chi phí.

- Viết hàm Lambda `SmartHomeControlFunction` (chạy trên môi trường Python 3.12), lấy cấu hình từ biến môi trường `IOT_ENDPOINT` và `TABLE_NAME` để xử lý 3 nhóm yêu cầu từ người dùng:

- Route `POST /devices/{thingName}/control`: kiểm tra tính hợp lệ của tên thiết bị và tham số gửi lên, sau đó gọi Boto3 cập nhật trạng thái `desired` vào Device Shadow.

- Route `GET /devices/{thingName}/history`: truy vấn bảng `SmartHomeDeviceHistory` lấy 10 bản ghi lịch sử thay đổi trạng thái gần nhất của thiết bị.

- Route `GET /devices/{thingName}/shadow`: đọc toàn bộ trạng thái Shadow hiện tại của thiết bị.

- Thiết lập HTTP API trên API Gateway (`SmartHomeAPI`) tại địa chỉ `https://xcibzup2li.execute-api.us-east-1.amazonaws.com` và tích hợp với hàm Lambda.

- Kiểm thử trực tiếp trên Lambda Console và gọi qua lệnh `curl` đều trả về HTTP 200 kèm thông báo `Shadow desired updated`:

```bash
curl -X POST [https://xcibzup2li.execute-api.us-east-1.amazonaws.com/devices/smart-light/control](https://xcibzup2li.execute-api.us-east-1.amazonaws.com/devices/smart-light/control) \
  -H "Content-Type: application/json" -d '{"power":"ON","brightness":80}'
```

- Hiện tại header CORS trong Lambda đang để mặc định `Access-Control-Allow-Origin: *` để thuận tiện test kết nối; nhóm sẽ giới hạn biến môi trường `ALLOWED_ORIGIN` về đúng URL của S3 website trong tuần 4.

- Minh chứng: [bảng DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png), [kiểm thử Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png), [API Gateway và kết quả curl](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png)

- Mã nguồn: [src/lambda/lambda_function.py](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/src/lambda/lambda_function.py)

#### b. Triển khai giao diện điều khiển Web trên Amazon S3

- Xây dựng giao diện điều khiển `web/index.html` và đưa lên S3 bucket `iot-smarthome-website` cấu hình Static Website Hosting.

- Giao diện cho phép bật/tắt, chỉnh thông số của 3 thiết bị (`smart-light`, `smart-ac`, `smart-fan`) thông qua API Gateway, đồng thời hiển thị bảng lịch sử trạng thái lấy từ DynamoDB. Kết quả chạy thử trên trình duyệt cho thấy lệnh điều khiển và bảng lịch sử hoạt động đồng bộ.

- Minh chứng: [giao diện web và lịch sử DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [giao diện web](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Web%20IOT%20Smarthome.png)

- Mã nguồn: [web/index.html](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/web/index.html)

#### c. Thiết lập giám sát CloudWatch và triển khai IaC (CloudFormation)

- Kiểm tra log thực thi của Lambda trong CloudWatch Log Group `/aws/lambda/SmartHomeControlFunction`, xác nhận các request gọi từ web và `curl` đều được ghi nhận đầy đủ.

- Tạo cảnh báo `SmartHomeLambdaErrorAlarm` trên CloudWatch Alarms: theo dõi metric `Errors` của Lambda với ngưỡng `>= 1` lỗi trong vòng 5 phút.

- Tạo cảnh báo `SmartHomeAPIGateway5XXAlarm` trên CloudWatch Alarms: theo dõi lỗi máy chủ `5XX` từ API Gateway. Tại thời điểm kiểm thử, cả 2 alarm đều ở trạng thái `OK`.

- Viết file mẫu Infrastructure as Code (`iac/template.yaml`) và triển khai thành công stack `SmartHomeIaCStack` trên CloudFormation để tạo bảng `SmartHomeDeviceHistoryIaC` (chế độ On-demand, có gắn tag quản lý dự án và cấu hình `DeletionPolicy: Retain` để tránh mất dữ liệu khi xóa stack).

- Minh chứng: [CloudWatch Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png), [CloudWatch Alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png), [template IaC](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml), [stack CloudFormation](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudformation%20stack%20-%20SmartHomeIaCStack.png)

### 2.3. Ảnh minh chứng tuần 3

#### DynamoDB, Lambda, API Gateway và IaC

**Bảng DynamoDB và bản ghi Shadow**

- [Bảng DynamoDB SmartHomeDeviceHistory](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB-SmartHomeDeviceHistory.png)

- [Các bản ghi Device Shadow trong DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png)

**IoT Rule lưu Shadow vào DynamoDB**

- [IoT Rule SaveShadowToDynamoDBRule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png)

**Lambda điều khiển thiết bị và kiểm thử**

- [Lambda SmartHomeControlFunction](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20SmartHomeControlFunction.png)

- [Kiểm thử cấu hình Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png)

**API Gateway**

- [API Gateway SmartHomeAPI](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeAPI.png)

- [Kiểm thử API Gateway bằng curl](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png)

**CloudFormation**

- [CloudFormation stack SmartHomeIaCStack](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudformation%20stack%20-%20SmartHomeIaCStack.png)

#### Giao diện web và kiểm thử tích hợp

- [Giao diện web điều khiển nhà thông minh](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Web%20IOT%20Smarthome.png)

- [Kiểm thử luồng end-to-end từ web đến DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png)

- [Log kiểm thử end-to-end trên PowerShell](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png)

- [Simulator kiểm thử ba thiết bị khi cập nhật Device Shadow](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Simulator%203%20devices%20when%20edit%20device%20shadow.png)

#### Bảo mật, giám sát và chi phí

- [IoT Policy theo nguyên tắc quyền tối thiểu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Iot-policy-least-privilege.png)

- [Kiểm tra bảo mật repository trên Git](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git%20security%20check.png)

- [CloudWatch Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png)

- [Tạo CloudWatch Alarm](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Create%20CloudWatch%20Alarm.png)

- [Danh sách CloudWatch Alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png)

- [CloudWatch Alarm theo dõi lỗi Lambda](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SmartHomeLambdaErrorAlarm.png)

- [Billing and Cost Management](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Billing%20and%20Cost%20Management%20-%20Credit.png)

---

## 3. KẾT QUẢ KIỂM THỬ TỪNG THÀNH PHẦN VÀ TÍCH HỢP

| Thành phần | Kịch bản kiểm thử | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|
| DynamoDB | Lưu và truy vấn lịch sử trạng thái | Các bản ghi được lưu đúng định dạng khóa | Đạt: Bảng `SmartHomeDeviceHistory` lưu đầy đủ các bản ghi `desired` và `reported` kèm timestamp. | [Bản ghi DynamoDB](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png) |
| Lambda | Chạy test event hợp lệ trên Console | Trả về mã `statusCode: 200` | Đạt: Hàm xử lý thành công và trả về mã 200. (Phần chụp ảnh test dữ liệu sai định dạng sẽ bổ sung ở tuần 4). | [Lambda test](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Lambda%20config%20test.png) |
| API Gateway | Gửi lệnh `curl` POST bật đèn và chỉnh độ sáng | Cập nhật thành công `desired` state | Đạt: Endpoint phản hồi `Shadow desired updated` sau khi sửa lại đúng cú pháp URL. | [API curl](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/API%20gateway%20curl.png) |
| IoT Rule → DynamoDB | Thay đổi trạng thái Shadow | Tự động sinh bản ghi mới trong DynamoDB | Đạt: Rule `SaveShadowToDynamoDBRule` kích hoạt và đẩy dữ liệu sang bảng ngay khi Shadow cập nhật. | [IoT Rule](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/SaveShadowToDynamoDBRule.png), [bản ghi](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/DynamoDB%20shadow%20records.png) |
| Simulator (3 thiết bị) | Điều khiển cả 3 thiết bị cùng lúc | Nhận bản tin `delta` và gửi lại `reported` | Đạt: Log ngày 25/10 xác nhận cả 3 thiết bị nhận `delta` và cập nhật `reported` chính xác. | [Log simulator](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/logs/device_simulator_week3.log), [ảnh kiểm thử 3 thiết bị](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Simulator%203%20devices%20when%20edit%20device%20shadow.png) |
| Web trên S3 | Thao tác bật/tắt trên web và xem lịch sử | Gọi API thành công, bảng lịch sử cập nhật | Đạt: Giao diện web phản hồi nhanh và hiển thị đúng danh sách lịch sử từ DynamoDB. | [Giao diện và kết quả](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png) |
| End-to-end | Luồng Web → API → Lambda → Shadow → Simulator → DynamoDB | Đồng bộ trạng thái xuyên suốt toàn hệ thống | Đạt: Thao tác từ giao diện web truyền lệnh tới simulator và lưu lịch sử về DynamoDB hoạt động trơn tru. | [Ảnh end-to-end](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20Web%20DynamoDB.png), [log PowerShell](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/End%20to%20end%20flow%20PowerShell%20log.png) |
| CloudWatch | Kiểm tra ghi log và trạng thái Alarm | Log ghi nhận request; Alarm hoạt động | Đạt: Log group của Lambda hiển thị đầy đủ; 2 alarm giữ trạng thái `OK`. | [Logs](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20logs.png), [alarms](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Cloudwatch%20alarms.png) |

**Khó khăn/lỗi gặp phải và cách xử lý trong quá trình làm:**

| Lỗi gặp phải | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Khi chạy lệnh `curl` kiểm thử API Gateway trên terminal bị báo lỗi không phân giải được host. | Do copy nhầm biến mẫu `API_URL` và ghép dư tiền tố `https://` hai lần trong câu lệnh. | Sửa lại câu lệnh với đúng địa chỉ `https://xcibzup2li.execute-api.us-east-1.amazonaws.com`, lệnh POST chạy thành công ngay sau đó. |

> Ghi chú: Các kịch bản kiểm thử nâng cao gồm gửi payload sai định dạng để chụp log lỗi 400, ngắt mạng đột ngột để test hàm auto-reconnect của simulator và giả lập lỗi để kích hoạt CloudWatch Alarm chuyển sang trạng thái `IN ALARM` sẽ được nhóm thực hiện trong đợt kiểm thử tổng thể tuần 4.

---

## 4. QUẢN LÝ TÀI NGUYÊN, BẢO MẬT VÀ CHI PHÍ

- **Gắn thẻ tài nguyên (Tagging):** Trong file `iac/template.yaml` đã khai báo bộ tag `Project = SmartHomeIoT`, `Owner1 = SV24110212`, `Owner2 = SV24110263`. Ở tuần 4 nhóm sẽ rà soát và gắn đồng bộ bộ tag này cho toàn bộ các tài nguyên tạo thủ công trên Console.

- **Region và IAM Role:** Toàn bộ hệ thống được triển khai thống nhất tại region `us-east-1` trên môi trường AWS Learner Lab, sử dụng role có sẵn của phòng lab.

- **Bảo mật mã nguồn:** Tập tin `.gitignore` đã chặn toàn bộ thư mục `certs/`, các file khóa `*.pem`, `*.key`, `*.crt` và `.env`. Kiểm tra lịch sử commit trên GitHub hoàn toàn sạch, không lộ khóa bí mật.

- **Bảo mật IoT Policy và Lambda:** IoT Policy đã được thu hẹp quyền theo đúng thiết bị; nhóm sẽ xuất thêm file JSON của policy lưu vào repo trong tuần 4. Hàm Lambda đã có bước kiểm tra đầu vào (validate tên thiết bị và thuộc tính điều khiển), cần cập nhật thêm cấu hình CORS giới hạn về đúng tên miền S3 website.

- **Trạng thái tài nguyên:** Các dịch vụ sử dụng trong dự án (IoT Core, Lambda, API Gateway, DynamoDB On-demand, S3, CloudWatch) đều hoạt động theo mô hình Serverless (chỉ tính phí khi có request), nên không phát sinh chi phí chờ khi không chạy simulator.

- **Chi phí thực tế:** Ảnh chụp trang Billing hiện tại mới chỉ chụp tab Credits (`$0.00`), chưa chụp chi tiết từ mục Cost Explorer/Bills. Nhóm sẽ trích xuất bảng chi phí chi tiết từng dịch vụ trong báo cáo tổng kết tuần 4.  - **Minh chứng:** [CloudFormation tags](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/iac/template.yaml), [ảnh kiểm tra Git](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Git\%20security\%20check.png), [ảnh Billing Credits](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/docs/images/Week3Pic/Billing\%20and\%20Cost\%20Management\%20-\%20Credit.png).
## 5. KHAI BÁO SỬ DỤNG AI

### 5.1. Công cụ và phạm vi sử dụng

#### a. Công cụ 1: GitHub Copilot trong VS Code

- **Mục đích:** Hỗ trợ gợi ý cú pháp Python (Boto3, AWS CRT MQTT), viết hàm callback xử lý kết nối lại trong `simulator.py`, kiểm tra lỗi cú pháp YAML cho CloudFormation (`iac/template.yaml`) và hỗ trợ gỡ lỗi khi chạy kiểm thử.

- **Yêu cầu đã gửi:** Các truy vấn hỗ trợ xử lý callback `on_connection_interrupted` và `on_connection_resumed` của thư viện `awscrt.mqtt`, cách kiểm tra hợp lệ dữ liệu đầu vào trong hàm `lambda_function.py`, và gỡ lỗi lệnh `curl` gọi API Gateway.

#### b. Công cụ 2: Claude (Anthropic)

- **Mục đích:** Tham khảo tài liệu kỹ thuật AWS (cú pháp SQL của AWS IoT Rule với action DynamoDBv2, cấu trúc thuộc tính `AWS::DynamoDB::Table` trong CloudFormation) và hỏi cách cấu hình CORS cho HTTP API Gateway.

- **Yêu cầu đã gửi:** Hỏi cách dùng hàm `topic(3)` trong câu lệnh SQL của IoT Rule để lấy `thingName` từ topic `$aws/things/+/shadow/update/accepted`; tra cứu cú pháp khai báo `BillingMode: PAY_PER_REQUEST` và `DeletionPolicy: Retain` trong CloudFormation template.

### 5.2. Phân định phần AI hỗ trợ và phần sinh viên thực hiện

- **Phạm vi AI hỗ trợ:** Chỉ dừng lại ở việc gợi ý đoạn mã nguồn, hỗ trợ tìm lỗi (debug) khi chạy code/lệnh test và tra cứu nhanh cú pháp cấu hình dịch vụ AWS.

- **Phần sinh viên tự thực hiện:** Sinh viên trực tiếp thiết kế kiến trúc, cấu hình tài nguyên trên AWS Console, viết và chỉnh sửa mã nguồn hoàn chỉnh, chạy kiểm thử thực tế trên máy cá nhân, chụp ảnh minh chứng và **tự viết toàn bộ nội dung báo cáo tiến độ tuần 3** dựa trên kết quả làm việc thực tế của nhóm.

### 5.3. Minh chứng lịch sử làm việc và commit trên GitHub

- **File báo cáo:** https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/blob/main/reports/BaoCaoTuan3.md

- **Danh sách commit:** https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commits/main

- **Commit 1:** [edb9c38 – Them BaoCaoTuan2](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/edb9c38405cb0756de4daf6d300b9dae5d088ef5)

- **Commit 2:** [d18ae53 – Merge pull request #2 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/d18ae5386723f10c58eb91aec57befbc511809e6)

- **Commit 3:** [0649b6b – Add Week3 Screenshots](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/0649b6b7499274161b6ee367ec071ad009b8f5d2)

- **Commit 4:** [cb92671 – Merge pull request #1 from NguyenTrungKien1805/minhhieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/cb92671730fa4d3915139db389edc176cdc42480)

- **Commit 5:** [38111a7 – Cau hinh IoT Rule DynamoDB, nang cap simulator auto-reconnect va IoT Policy quyen toi thieu](https://github.com/NguyenTrungKien1805/aws-iot-device-shadow-smarthome/commit/38111a700964a0b3d9c643fcfadb27dc31634c48)
---

## 6. KẾT LUẬN VÀ KẾ HOẠCH CÔNG VIỆC TUẦN 4

### 6.1. Kết luận tuần 3

Trong tuần 3, nhóm đã hoàn thành việc kết nối toàn bộ luồng điều khiển và lưu trữ lịch sử: từ giao diện Web trên S3 qua API Gateway và Lambda để cập nhật Device Shadow, đồng bộ xuống 3 thiết bị giả lập (`smart-light`, `smart-ac`, `smart-fan`) và tự động ghi lịch sử vào DynamoDB thông qua IoT Rule. Hệ thống giám sát bằng CloudWatch Logs/Alarms và mẫu IaC bằng CloudFormation cũng đã được triển khai và chạy thử thành công. Các hạng mục kiểm thử tình huống lỗi (ngắt mạng đột ngột, gửi dữ liệu sai để kích hoạt Alarm), thu hẹp CORS và trích xuất bảng chi phí từ Cost Explorer sẽ được hoàn tất trong tuần 4.

### 6.2. Kế hoạch công việc tuần 4

**Mục tiêu:** Kiểm thử tổng thể (bao gồm các kịch bản lỗi), tối ưu và thống kê chi phí thực tế, dọn dẹp tài nguyên, hoàn thiện báo cáo cuối kỳ và quay video demo.

**1. Trần Nguyễn Minh Hiếu – MSSV: 24110212**

- Công việc 1: Kiểm thử tổng thể toàn bộ luồng với cả 3 thiết bị (bổ sung test ngắt mạng auto-reconnect, lưu file JSON của IoT Policy vào repo); hoàn thiện mã simulator và tài liệu hướng dẫn chạy. *(4 giờ)*

- Công việc 2: Viết phần báo cáo cuối kỳ về IoT Core, Device Shadow và bảo mật; chuẩn bị kịch bản demo. *(4 giờ)*

**2. Nguyễn Trung Kiên – MSSV: 24110263**

- Công việc 1: Thu hẹp CORS trên Lambda, test kích hoạt CloudWatch Alarm, trích xuất chi phí chi tiết từ Cost Explorer/Bills và dọn dẹp các tài nguyên không cần thiết sau khi demo. *(4 giờ)*

- Công việc 2: Viết phần báo cáo cuối kỳ về kiến trúc, chi phí và kết quả kiểm thử; quay và dựng video demo (≤ 10 phút). *(4 giờ)*

**3. Công việc phối hợp:**

- Diễn tập demo, chụp đầy đủ minh chứng cuối kỳ (Account ID, Region, thời gian), cập nhật Worklog và mã nguồn lên GitHub, chuẩn bị câu hỏi vấn đáp.

**Kết quả đầu ra dự kiến tuần 4:** Hệ thống chạy ổn định end-to-end; báo cáo tổng kết đầy đủ kèm sơ đồ kiến trúc và bảng chi phí thực tế; video demo ≤ 10 phút; toàn bộ tài nguyên được dọn dẹp sạch sẽ sau buổi báo cáo.

> **Lưu ý:** Mỗi thành viên đảm bảo tối thiểu 8 giờ làm việc trong tuần 4; tuân thủ việc sử dụng `LabRole`/`LabInstanceProfile` và tuyệt đối không đẩy private key lên GitHub.

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
