import paho.mqtt.client as mqtt
import json
from django.conf import settings
from .models import WaterLevel

# Variabel penampung data sementara
latest_data = {
    "distance": None,
    "ph": None,
    "tds": None,
    "status": None
}

def save_if_complete():
    """Menyimpan ke database jika ketiga nilai utama tersedia"""
    if all([latest_data["distance"] is not None,
            latest_data["ph"] is not None,
            latest_data["tds"] is not None]):
        WaterLevel.objects.create(
            distance=latest_data["distance"],
            ph_value=latest_data["ph"],
            tds_value=latest_data["tds"]
        )
        print(f"Data saved: {latest_data}")
        # Reset data setelah disimpan
        latest_data["distance"] = None
        latest_data["ph"] = None
        latest_data["tds"] = None

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with code {rc}")
    client.subscribe("sensor/ultrasonic/distance")
    client.subscribe("sensor/ph/value")
    client.subscribe("watermonitor/sensor/tds")
    client.subscribe("watermonitor/status")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    try:
        if topic == "sensor/ultrasonic/distance":
            latest_data["distance"] = float(payload)
        elif topic == "sensor/ph/value":
            latest_data["ph"] = float(payload)
        elif topic == "watermonitor/sensor/tds":
            latest_data["tds"] = float(payload)
        elif topic == "watermonitor/status":
            latest_data["status"] = payload  # jika ingin disimpan, sesuaikan modelnya

        print(f"Received [{topic}]: {payload}")
        save_if_complete()
    except Exception as e:
        print(f"Error processing MQTT: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
