import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC_TEMPERATURE = "home/sensor/temperature"
TOPIC_HUMIDITY = "home/sensor/humidity"
TOPIC_PM25 = "home/sensor/pm25"

def generate_sensor_data():
    temperature = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(40.0, 60.0), 2)
    pm25 = round(random.uniform(0, 100), 2)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "pm25": pm25,
        "timestamp": datetime.now().isoformat()
    }


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker: {rc}")

def main():
    client = mqtt.Client("SensorSimulator")
    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("센서 시뮬레이터 시작...")

    try:
        while True:
            data = generate_sensor_data()

            client.publish(TOPIC_TEMPERATURE, json.dumps({
                "value": data["temperature"],
                "timestamp": data["timestamp"]
            }))
            
            client.publish(TOPIC_HUMIDITY, json.dumps({
                "value": data["humidity"],
                "timestamp": data["timestamp"]
            }))
            
            client.publish(TOPIC_PM25, json.dumps({
                "value": data["pm25"],
                "timestamp": data["timestamp"]
            }))

            print(f"발행됨: 온도={data['temperature']}°C, "
                  f"습도={data['humidity']}%, PM2.5={data['pm25']}")
            
            time.sleep(60)
    
    except KeyboardInterrupt:
        print("센서 시뮬레이터 종료...")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
