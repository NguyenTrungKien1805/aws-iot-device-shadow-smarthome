import json
import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

IOT_ENDPOINT = os.environ.get("IOT_ENDPOINT", "a1vt5536hy0pad-ats.iot.us-east-1.amazonaws.com")
TABLE_NAME = os.environ.get("TABLE_NAME", "SmartHomeDeviceHistory")
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

iot = boto3.client("iot-data", endpoint_url=f"https://{IOT_ENDPOINT}")
dynamodb = boto3.resource("dynamodb")

ALLOWED_SPEC = {
    "smart-light": {"power": ["ON", "OFF"], "brightness": (0, 100)},
    "smart-ac": {"power": ["ON", "OFF"], "temperature": (16, 30), "mode": ["cool", "dry", "fan"]},
    "smart-fan": {"power": ["ON", "OFF"], "speed": (1, 3)}
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

def resp(code, obj):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(obj, cls=DecimalEncoder)
    }

def validate_payload(thing, body):
    spec = ALLOWED_SPEC.get(thing)
    if not spec or not isinstance(body, dict) or not body:
        return False, "Invalid device or empty payload"
    for k, v in body.items():
        if k not in spec:
            return False, f"Invalid attribute: {k}"
        rule = spec[k]
        if isinstance(rule, list) and v not in rule:
            return False, f"Attribute {k} must be one of {rule}"
        if isinstance(rule, tuple):
            if not isinstance(v, (int, float)) or not (rule[0] <= v <= rule[1]):
                return False, f"Attribute {k} must be between {rule[0]} and {rule[1]}"
    return True, "OK"

def lambda_handler(event, context):
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method", "POST")
    if method == "OPTIONS":
        return resp(200, {"message": "CORS preflight OK"})

    path_params = event.get("pathParameters") or {}
    thing = path_params.get("thingName")
    raw_path = event.get("rawPath") or event.get("path") or ""

    if thing not in ALLOWED_SPEC:
        return resp(400, {"message": f"Invalid thingName: {thing}"})

    # 1. GET /devices/{thingName}/history -> Đọc lịch sử từ DynamoDB
    if method == "GET" and "history" in raw_path:
        table = dynamodb.Table(TABLE_NAME)
        result = table.query(
            KeyConditionExpression=Key("deviceId").eq(thing),
            ScanIndexForward=False,
            Limit=10
        )
        return resp(200, {"thing": thing, "history": result.get("Items", [])})

    # 2. GET /devices/{thingName}/shadow -> Đọc trạng thái Shadow hiện tại
    if method == "GET":
        shadow = iot.get_thing_shadow(thingName=thing)
        payload = json.loads(shadow["payload"].read().decode("utf-8"))
        return resp(200, {"thing": thing, "state": payload.get("state", {})})

    # 3. POST /devices/{thingName}/control -> Cập nhật desired lên Device Shadow
    body_str = event.get("body") or "{}"
    body = json.loads(body_str) if isinstance(body_str, str) else body_str

    ok, msg = validate_payload(thing, body)
    if not ok:
        return resp(400, {"message": msg})

    iot.update_thing_shadow(
        thingName=thing,
        payload=json.dumps({"state": {"desired": body}})
    )
    return resp(200, {"thing": thing, "desired": body, "status": "Shadow desired updated"})