# mqtt_listener.py
import json
import threading
import paho.mqtt.client as mqtt

from camera_manager import system_on, system_off
from stream_server import run_stream_server
from mission import start_mission, stop_mission

AGV_ID = "AGV1"
MQTT_HOST = "172.20.10.6"
MQTT_PORT = 1883

RUN_TOPIC = f"agv/{AGV_ID}/run"
CMD_TOPIC = f"agv/{AGV_ID}/cmd"

_stream_thread = None

def on_connect(client, userdata, flags, rc):
    print("MQTT connected:", rc)
    client.subscribe(RUN_TOPIC)
    client.subscribe(CMD_TOPIC)

def on_message(client, userdata, msg):
    global _stream_thread
    data = json.loads(msg.payload.decode())

    # ------------------
    # SYSTEM ON/OFF
    # ------------------
    if msg.topic == RUN_TOPIC:
        running = data.get("running")
        print(f"[RUN] received: {running}")

        if running:
            system_on()
            if _stream_thread is None:
                _stream_thread = threading.Thread(
                    target=run_stream_server,
                    daemon=True
                )
                _stream_thread.start()
        else:
            stop_mission()
            system_off()


    # ------------------
    # MISSION START
    # ------------------
    elif msg.topic == CMD_TOPIC:
        if data.get("type") == "start":
            cycle_id = data.get("cycle_id")
            start_mission(cycle_id)

def start_mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()