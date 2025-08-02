import time
import random
from app.mqtt_client import create_client

def simulate_motion_sensor(device_id="motion-1", interval=2, qos=1):
    """
    Simulates a motion sensor that randomly detects motion (MOTION/NO_MOTION).

    Args:
        device_id (str): Unique ID for this motion sensor
        interval (int): Seconds between state updates
        qos (int): MQTT Quality of Service (1 = at least once)
    """
    client = create_client(client_id=f"motion-{device_id}", clean_session=False)
    client.loop_start()

    try:
        while True:
            state = random.choice(["MOTION", "NO_MOTION"])
            topic = "home/security/motion"
            client.publish(topic, state, qos=qos)
            print(f"[MOTION SENSOR] Device: {device_id} | State: {state}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("[INFO] Motion sensor stopped manually.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_motion_sensor()