import time
import random
from app.mqtt_client import create_client

def simulate_window_sensor(device_id="window-1", interval=3, qos=1):
    """
    Simulates a window sensor that randomly changes state (OPEN/CLOSED).

    Args:
        device_id (str): Unique ID for this window sensor
        interval (int): Seconds between state updates
        qos (int): MQTT Quality of Service (1 = at least once)
    """
    client = create_client(client_id=f"window-{device_id}", clean_session=False)
    client.loop_start()

    try:
        while True:
            state = random.choice(["OPEN", "CLOSED"])
            topic = "home/security/window"
            client.publish(topic, state, qos=qos)
            print(f"[WINDOW SENSOR] Device: {device_id} | State: {state}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("[INFO] Window sensor stopped manually.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_window_sensor()