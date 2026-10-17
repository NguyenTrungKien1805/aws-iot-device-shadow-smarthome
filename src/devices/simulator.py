import json
import os
import time
from datetime import datetime
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# Endpoint thực tế của tài khoản AWS Learner Lab
IOT_ENDPOINT = os.environ.get("IOT_ENDPOINT", "a1vt5536hy0pad-ats.iot.us-east-1.amazonaws.com")

# Trạng thái khởi tạo mặc định của 3 thiết bị theo đúng thiết kế báo cáo
DEVICES_STATE = {
    "smart-light": {"power": "OFF", "brightness": 0},
    "smart-ac": {"power": "OFF", "temperature": 24, "mode": "cool"},
    "smart-fan": {"power": "OFF", "speed": 1}
}

connections = {}

def log_event(thing_name, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{thing_name}] {message}"
    print(log_line)
    os.makedirs("logs", exist_ok=True)
    with open("logs/device_simulator.log", "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def create_device_connection(thing_name):
    cert_path = f"certs/{thing_name}.cert.pem"
    key_path = f"certs/{thing_name}.private.key"
    ca_path = "certs/AmazonRootCA1.pem"

    mqtt_conn = mqtt_connection_builder.mtls_from_path(
        endpoint=IOT_ENDPOINT,
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        ca_filepath=ca_path,
        client_id=thing_name,
        clean_session=False,
        keep_alive_secs=30
    )

    log_event(thing_name, f"Dang ket noi toi AWS IoT Core ({IOT_ENDPOINT})...")
    mqtt_conn.connect().result()
    log_event(thing_name, "Ket noi THANH CONG!")

    def on_delta(topic, payload, dup, qos, retain, **kwargs):
        payload_str = payload.decode("utf-8")
        log_event(thing_name, f"Nhan ban tin DELTA tu topic '{topic}': {payload_str}")
        
        data = json.loads(payload_str)
        delta = data.get("state", {})
        
        if delta:
            DEVICES_STATE[thing_name].update(delta)
            log_event(thing_name, f"Da cap nhat trang thai thiet bi thanh: {json.dumps(DEVICES_STATE[thing_name])}")
            
            report_payload = {"state": {"reported": DEVICES_STATE[thing_name]}}
            update_topic = f"$aws/things/{thing_name}/shadow/update"
            mqtt_conn.publish(
                topic=update_topic,
                payload=json.dumps(report_payload),
                qos=mqtt.QoS.AT_LEAST_ONCE
            )
            log_event(thing_name, f"Da publish REPORTED len Shadow: {json.dumps(report_payload)}")

    # Subscribe vào topic delta của thiết bị với chuẩn mqtt.QoS.AT_LEAST_ONCE
    delta_topic = f"$aws/things/{thing_name}/shadow/update/delta"
    subscribe_future, _ = mqtt_conn.subscribe(
        topic=delta_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_delta
    )
    subscribe_future.result()
    log_event(thing_name, f"Dang lang nghe lenh dieu khien tai: {delta_topic}")

    # Gửi trạng thái khởi tạo (reported) lần đầu tiên
    initial_report = {"state": {"reported": DEVICES_STATE[thing_name]}}
    publish_future, _ = mqtt_conn.publish(
        topic=f"$aws/things/{thing_name}/shadow/update",
        payload=json.dumps(initial_report),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    publish_future.result()
    log_event(thing_name, f"Da dong bo trang thai ban dau (reported): {json.dumps(DEVICES_STATE[thing_name])}")

    return mqtt_conn

if __name__ == "__main__":
    print("=== KHOI DONG HE THONG MO PHONG THIET BI SMART HOME ===")
    try:
        for thing in DEVICES_STATE.keys():
            connections[thing] = create_device_connection(thing)
        print("\n>>> Ca 3 thiet bi dang hoat dong va cho lenh tu AWS IoT Shadow. Nhan Ctrl+C de dung. <<<\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDang ngat ket noi cac thiet bi...")
        for thing, conn in connections.items():
            conn.disconnect().result()
            log_event(thing, "Da ngat ket noi an toan.")