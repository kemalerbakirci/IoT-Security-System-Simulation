import paho.mqtt.client as mqtt
from app.mqtt_client import create_client

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    if topic == "home/security/alarm":
        if payload == "ON":
            print("🚨 Alarm Activated!")
        elif payload == "OFF":
            print("🚨 Alarm Deactivated!")

    elif topic == "home/security/light":
        if payload == "ON":
            print("💡 Light Turned ON!")
        elif payload == "OFF":
            print("💡 Light Turned OFF!")

def listen_to_actuators():
    client = create_client("actuator-listener", clean_session=False)
    client.on_message = on_message

    client.subscribe("home/security/alarm", qos=1)
    client.subscribe("home/security/light", qos=1)

    client.loop_forever()

if __name__ == "__main__":
    listen_to_actuators()
