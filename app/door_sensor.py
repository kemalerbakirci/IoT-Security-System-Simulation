import time
import random
from app.mqtt_client import create_client

def simulate_door_sensor(device_id="door-1", interval=3, qos=1):
    """
    Simulates a door sensor that randomly changes state (OPEN/CLOSED).
    
    Args:
        device_id (str): Unique ID for this door sensor
        interval (int): Seconds between state updates
        qos (int): MQTT Quality of Service (1 = at least once)
    """
    # Create persistent MQTT client
    client = create_client(client_id=f"door-{device_id}", clean_session=False)
    client.loop_start()

    try:
        while True:
            # Randomly pick door state
            state = random.choice(["OPEN", "CLOSED"])
            topic = "home/security/door"
            client.publish(topic, state, qos=qos)
            print(f"[DOOR SENSOR] Device: {device_id} | State: {state}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("[INFO] Door sensor stopped manually.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_door_sensor()
