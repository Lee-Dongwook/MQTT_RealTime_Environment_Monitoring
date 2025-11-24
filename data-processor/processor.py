import paho.mqtt.client as mqtt
import json
from collections import deque
from datetime import datetime

# MQTT 설정
BROKER = "localhost"
PORT = 1883
TOPICS = [
    "home/sensor/temperature",
    "home/sensor/humidity",
    "home/sensor/pm25"
]
# 데이터 저장소 (최근 100개)
data_storage = {
    "temperature": deque(maxlen=100),
    "humidity": deque(maxlen=100),
    "pm25": deque(maxlen=100)
}

def is_outlier(value, sensor_type):
    """이상치 감지"""
    if sensor_type == "temperature":
        return value < -10 or value > 50
    elif sensor_type == "humidity":
        return value < 0 or value > 100
    elif sensor_type == "pm25":
        return value < 0 or value > 500
    return False

def process_data(sensor_type, data):
    """데이터 처리 및 필터링"""
    value = data.get("value")
    timestamp = data.get("timestamp")
    
    if is_outlier(value, sensor_type):
        print(f"⚠️ 이상치 감지: {sensor_type}={value}")
        return None
    
    # 정상 데이터 저장
    data_storage[sensor_type].append({
        "value": value,
        "timestamp": timestamp
    })
    
    return data


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT 브로커에 연결됨")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"토픽 구독: {topic}")
    else:
        print(f"연결 실패, 코드: {rc}")


def on_message(client, userdata, msg):
    """메시지 수신 시 처리"""
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    
    # 센서 타입 추출
    sensor_type = topic.split('/')[-1]
    
    # 데이터 처리
    processed = process_data(sensor_type, payload)
    
    if processed:
        print(f"✓ {sensor_type}: {payload['value']} ({payload['timestamp']})")
        
        # 통계 출력
        if len(data_storage[sensor_type]) >= 5:
            values = [d["value"] for d in data_storage[sensor_type]]
            avg = sum(values) / len(values)
            print(f"  평균: {avg:.2f}, 최근 {len(values)}개 데이터")



def main():
    client = mqtt.Client("DataProcessor")
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(BROKER, PORT, 60)
    
    print("데이터 프로세서 시작...")
    client.loop_forever()

if __name__ == "__main__":
    main()
