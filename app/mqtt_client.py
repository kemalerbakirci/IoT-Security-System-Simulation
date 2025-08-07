import os
import logging
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load environment variables (broker URL & port)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))
BROKER_URL = os.getenv("BROKER_URL", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def create_client(client_id: str, clean_session: bool = False) -> mqtt.Client:
    """
    Creates and returns an MQTT client with persistent session support.
    client_id: Unique ID for the device (must be unique per sensor/actuator)
    clean_session: If False, broker remembers subscriptions & queued messages.
    """
    client = mqtt.Client(client_id=client_id, clean_session=clean_session, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(BROKER_URL, BROKER_PORT)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"[MQTT] Connected successfully as {client._client_id.decode()}")
    else:
        logger.error(f"[MQTT] Connection failed (rc={rc})")

def on_disconnect(client, userdata, rc):
    logger.info(f"[MQTT] Disconnected (rc={rc})")
