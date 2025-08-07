# API Documentation

## Overview

This document provides comprehensive API documentation for the IoT Security System Simulation. The system uses MQTT as the primary communication protocol, with Python modules providing the sensor and actuator interfaces.

## MQTT API

### Connection Parameters

#### Default Configuration
```python
BROKER_URL = "localhost"
BROKER_PORT = 1883
PROTOCOL = mqtt.MQTTv311
CLEAN_SESSION = False  # Persistent sessions enabled
QOS_LEVEL = 1         # At least once delivery
```

#### Custom Configuration
```python
from app.mqtt_client import create_client

# Create client with custom settings
client = create_client(
    client_id="my-device-001", 
    clean_session=False
)
```

### Topic Structure

#### Sensor Topics (Publish)
| Topic | Description | Message Format | Update Frequency |
|-------|-------------|----------------|------------------|
| `home/security/door` | Door sensor state | `"OPEN"` or `"CLOSED"` | 3 seconds |
| `home/security/window` | Window sensor state | `"OPEN"` or `"CLOSED"` | 3 seconds |
| `home/security/motion` | Motion detection | `"MOTION"` or `"NO_MOTION"` | 2 seconds |

#### Actuator Topics (Subscribe)
| Topic | Description | Message Format | Response Time |
|-------|-------------|----------------|---------------|
| `home/security/alarm` | Alarm control | `"ON"` or `"OFF"` | <100ms |
| `home/security/light` | Light control | `"ON"` or `"OFF"` | <100ms |

### Message Specifications

#### Sensor Messages
```json
{
  "topic": "home/security/door",
  "payload": "OPEN",
  "qos": 1,
  "retain": false,
  "timestamp": "2025-01-01T12:00:00Z"
}
```

#### Actuator Commands
```json
{
  "topic": "home/security/alarm", 
  "payload": "ON",
  "qos": 1,
  "retain": false
}
```

## Python API

### Core MQTT Client Module

#### `mqtt_client.py`

##### `create_client(client_id, clean_session=False)`
Creates and configures an MQTT client instance.

**Parameters:**
- `client_id` (str): Unique identifier for the MQTT client
- `clean_session` (bool): Whether to use persistent sessions (default: False)

**Returns:**
- `mqtt.Client`: Configured MQTT client instance

**Example:**
```python
from app.mqtt_client import create_client

client = create_client("sensor-001")
client.loop_start()
client.publish("home/security/door", "OPEN", qos=1)
```

##### Connection Callbacks
```python
def on_connect(client, userdata, flags, rc):
    """Called when MQTT client connects to broker"""
    
def on_disconnect(client, userdata, rc):
    """Called when MQTT client disconnects from broker"""
```

### Sensor Modules

#### Door Sensor API

##### `door_sensor.py`

##### `simulate_door_sensor(device_id="door-1", interval=3, qos=1)`
Simulates a door sensor with random state changes.

**Parameters:**
- `device_id` (str): Unique identifier for this sensor instance
- `interval` (int): Seconds between state updates
- `qos` (int): MQTT Quality of Service level (0, 1, or 2)

**States:**
- `"OPEN"`: Door is open (security breach)
- `"CLOSED"`: Door is closed (secure)

**Example Usage:**
```python
from app.door_sensor import simulate_door_sensor

# Run with custom settings
simulate_door_sensor(
    device_id="front-door",
    interval=5,  # Update every 5 seconds
    qos=2       # Exactly once delivery
)
```

#### Window Sensor API

##### `window_sensor.py`

##### `simulate_window_sensor(device_id="window-1", interval=3, qos=1)`
Simulates a window sensor with random state changes.

**Parameters:**
- `device_id` (str): Unique identifier for this sensor instance
- `interval` (int): Seconds between state updates  
- `qos` (int): MQTT Quality of Service level

**States:**
- `"OPEN"`: Window is open (security breach)
- `"CLOSED"`: Window is closed (secure)

**Example Usage:**
```python
from app.window_sensor import simulate_window_sensor

# Multiple window sensors
import threading

def start_window_sensor(device_id):
    simulate_window_sensor(device_id=device_id)

# Start multiple sensors in parallel
threads = []
for window_id in ["bedroom", "living-room", "kitchen"]:
    t = threading.Thread(target=start_window_sensor, args=(window_id,))
    t.start()
    threads.append(t)
```

#### Motion Sensor API

##### `motion_sensor.py`

##### `simulate_motion_sensor(device_id="motion-1", interval=2, qos=1)`
Simulates a motion sensor with random detection events.

**Parameters:**
- `device_id` (str): Unique identifier for this sensor instance
- `interval` (int): Seconds between state updates
- `qos` (int): MQTT Quality of Service level

**States:**
- `"MOTION"`: Motion detected (security breach)
- `"NO_MOTION"`: No motion detected (secure)

**Example Usage:**
```python
from app.motion_sensor import simulate_motion_sensor

# High-frequency motion detection
simulate_motion_sensor(
    device_id="hallway-motion",
    interval=1,  # Check every second
    qos=1
)
```

### Actuator Module

#### Actuator Listener API

##### `actuator_listener.py`

##### `listen_to_actuators()`
Subscribes to actuator command topics and responds to control messages.

**Subscribed Topics:**
- `home/security/alarm`
- `home/security/light`

**Message Handler:**
```python
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    # Handle alarm commands
    if topic == "home/security/alarm":
        if payload == "ON":
            print("🚨 Alarm Activated!")
        elif payload == "OFF":
            print("🚨 Alarm Deactivated!")
    
    # Handle light commands  
    elif topic == "home/security/light":
        if payload == "ON":
            print("💡 Light Turned ON!")
        elif payload == "OFF":
            print("💡 Light Turned OFF!")
```

**Example Usage:**
```python
from app.actuator_listener import listen_to_actuators

# Start listening (blocking call)
listen_to_actuators()
```

## Custom Sensor Development

### Creating New Sensor Types

#### Template Structure
```python
import time
import random
from app.mqtt_client import create_client

def simulate_custom_sensor(device_id="custom-1", interval=3, qos=1):
    """
    Template for creating custom sensor simulations.
    
    Args:
        device_id (str): Unique ID for this sensor
        interval (int): Seconds between updates
        qos (int): MQTT Quality of Service
    """
    # Create MQTT client
    client = create_client(client_id=f"custom-{device_id}", clean_session=False)
    client.loop_start()
    
    try:
        while True:
            # Generate sensor data
            sensor_value = generate_sensor_data()
            
            # Publish to MQTT
            topic = f"home/security/{device_id}"
            client.publish(topic, sensor_value, qos=qos)
            
            print(f"[CUSTOM SENSOR] Device: {device_id} | Value: {sensor_value}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"[INFO] {device_id} sensor stopped manually.")
    finally:
        client.loop_stop()
        client.disconnect()

def generate_sensor_data():
    """Implement your sensor logic here"""
    return random.choice(["VALUE1", "VALUE2", "VALUE3"])

if __name__ == "__main__":
    simulate_custom_sensor()
```

#### Example: Temperature Sensor
```python
import time
import random
from app.mqtt_client import create_client

def simulate_temperature_sensor(device_id="temp-1", interval=10, qos=1):
    """Simulates a temperature sensor for security monitoring"""
    client = create_client(client_id=f"temp-{device_id}", clean_session=False)
    client.loop_start()
    
    try:
        while True:
            # Generate realistic temperature reading
            temperature = round(random.uniform(18.0, 25.0), 1)
            
            # Determine security status based on temperature
            if temperature > 30.0 or temperature < 10.0:
                status = "ALERT"  # Potential fire or system failure
            else:
                status = "NORMAL"
            
            # Publish both temperature and status
            client.publish(f"home/security/temperature/{device_id}", f"{temperature}°C", qos=qos)
            client.publish(f"home/security/temp-status/{device_id}", status, qos=qos)
            
            print(f"[TEMP SENSOR] Device: {device_id} | Temp: {temperature}°C | Status: {status}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"[INFO] Temperature sensor {device_id} stopped.")
    finally:
        client.loop_stop()
        client.disconnect()
```

### Custom Actuator Development

#### Template Structure
```python
import paho.mqtt.client as mqtt
from app.mqtt_client import create_client

def on_message(client, userdata, msg):
    """Handle incoming actuator commands"""
    topic = msg.topic
    payload = msg.payload.decode()
    
    # Parse topic to determine actuator type
    actuator_type = topic.split('/')[-1]
    
    # Implement actuator logic
    handle_actuator_command(actuator_type, payload)

def handle_actuator_command(actuator_type, command):
    """Process actuator commands"""
    if actuator_type == "sirens":
        if command == "ON":
            print("🔊 Siren Activated!")
            # Add hardware control logic here
        elif command == "OFF":
            print("🔊 Siren Deactivated!")
    
def listen_to_custom_actuators():
    """Subscribe to custom actuator topics"""
    client = create_client("custom-actuator-listener", clean_session=False)
    client.on_message = on_message
    
    # Subscribe to custom topics
    client.subscribe("home/security/sirens", qos=1)
    client.subscribe("home/security/locks", qos=1)
    
    client.loop_forever()

if __name__ == "__main__":
    listen_to_custom_actuators()
```

## Integration Examples

### External System Integration

#### Database Logging
```python
import sqlite3
import json
from datetime import datetime

def log_sensor_data_to_db(topic, payload):
    """Log sensor data to SQLite database"""
    conn = sqlite3.connect('security_system.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic TEXT,
            payload TEXT
        )
    ''')
    
    # Insert sensor data
    cursor.execute('''
        INSERT INTO sensor_logs (timestamp, topic, payload) 
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), topic, payload))
    
    conn.commit()
    conn.close()

# Modified on_message handler
def on_message_with_logging(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    # Log to database
    log_sensor_data_to_db(topic, payload)
    
    # Continue with normal processing
    handle_actuator_command(topic, payload)
```

#### REST API Integration
```python
import requests
import json

def send_alert_to_api(sensor_type, status):
    """Send security alerts to external REST API"""
    alert_data = {
        "sensor_type": sensor_type,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "location": "home"
    }
    
    try:
        response = requests.post(
            "https://api.security-service.com/alerts",
            json=alert_data,
            headers={"Authorization": "Bearer YOUR_API_TOKEN"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"[API] Alert sent successfully: {sensor_type} - {status}")
        else:
            print(f"[API] Failed to send alert: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[API] Network error: {e}")

# Usage in sensor code
def enhanced_door_sensor():
    # ... existing sensor code ...
    
    if state == "OPEN":
        send_alert_to_api("door", "breach")
```

## Error Handling

### Connection Error Handling
```python
import time
from app.mqtt_client import create_client

def robust_sensor_with_retry(device_id, max_retries=5):
    """Sensor with connection retry logic"""
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            client = create_client(client_id=f"sensor-{device_id}")
            client.loop_start()
            
            # Main sensor loop
            while True:
                # Sensor logic here
                state = random.choice(["OPEN", "CLOSED"])
                client.publish("home/security/door", state, qos=1)
                time.sleep(3)
                
        except Exception as e:
            print(f"[ERROR] Sensor failed: {e}")
            retry_count += 1
            time.sleep(5 * retry_count)  # Exponential backoff
            
        finally:
            try:
                client.loop_stop()
                client.disconnect()
            except:
                pass
                
    print(f"[ERROR] Max retries exceeded for sensor {device_id}")
```

### Message Validation
```python
def validate_sensor_message(topic, payload):
    """Validate incoming sensor messages"""
    # Validate topic format
    if not topic.startswith("home/security/"):
        return False, "Invalid topic format"
    
    # Validate payload content
    valid_states = {
        "door": ["OPEN", "CLOSED"],
        "window": ["OPEN", "CLOSED"],
        "motion": ["MOTION", "NO_MOTION"],
        "alarm": ["ON", "OFF"],
        "light": ["ON", "OFF"]
    }
    
    sensor_type = topic.split('/')[-1]
    if sensor_type in valid_states:
        if payload not in valid_states[sensor_type]:
            return False, f"Invalid state '{payload}' for {sensor_type}"
    
    return True, "Valid message"

# Usage in message handler
def on_message_with_validation(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    is_valid, error_msg = validate_sensor_message(topic, payload)
    
    if is_valid:
        # Process message normally
        handle_message(topic, payload)
    else:
        print(f"[VALIDATION ERROR] {error_msg}")
```

## Performance Considerations

### Message Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_messages_per_minute=60):
        self.max_messages = max_messages_per_minute
        self.message_times = defaultdict(list)
    
    def can_send_message(self, client_id):
        now = time.time()
        minute_ago = now - 60
        
        # Remove old message timestamps
        self.message_times[client_id] = [
            t for t in self.message_times[client_id] 
            if t > minute_ago
        ]
        
        # Check if under limit
        if len(self.message_times[client_id]) < self.max_messages:
            self.message_times[client_id].append(now)
            return True
        
        return False

# Usage in sensor code
rate_limiter = RateLimiter(max_messages_per_minute=30)

def rate_limited_sensor(device_id):
    client = create_client(f"sensor-{device_id}")
    
    while True:
        if rate_limiter.can_send_message(device_id):
            state = generate_sensor_data()
            client.publish("home/security/sensor", state)
        
        time.sleep(1)  # Check every second
```

### Memory Management
```python
import gc
import psutil
import os

def monitor_memory_usage():
    """Monitor and report memory usage"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    # Force garbage collection if memory usage is high
    if memory_info.rss > 100 * 1024 * 1024:  # 100 MB threshold
        gc.collect()
        print("Garbage collection performed")

# Call periodically in long-running sensors
def memory_efficient_sensor():
    message_count = 0
    
    while True:
        # Normal sensor logic
        publish_sensor_data()
        
        # Monitor memory every 100 messages
        message_count += 1
        if message_count % 100 == 0:
            monitor_memory_usage()
```

## Security Best Practices

### Authentication (Production)
```python
import ssl

def create_secure_client(client_id, username, password, ca_cert_path):
    """Create MQTT client with authentication and TLS"""
    client = mqtt.Client(client_id=client_id)
    
    # Set username and password
    client.username_pw_set(username, password)
    
    # Configure TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(ca_cert_path)
    client.tls_set_context(context)
    
    # Connect to secure port
    client.connect("secure-broker.example.com", 8883, 60)
    
    return client
```

### Message Encryption
```python
import json
from cryptography.fernet import Fernet

class MessageEncryption:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_message(self, message):
        """Encrypt a message payload"""
        message_bytes = json.dumps(message).encode()
        encrypted = self.cipher.encrypt(message_bytes)
        return encrypted
    
    def decrypt_message(self, encrypted_message):
        """Decrypt a message payload"""
        decrypted_bytes = self.cipher.decrypt(encrypted_message)
        return json.loads(decrypted_bytes.decode())

# Usage
encryptor = MessageEncryption()

def secure_publish(client, topic, data):
    """Publish encrypted message"""
    encrypted_data = encryptor.encrypt_message(data)
    client.publish(topic, encrypted_data)

def secure_on_message(client, userdata, msg):
    """Handle encrypted incoming messages"""
    try:
        decrypted_data = encryptor.decrypt_message(msg.payload)
        # Process decrypted data
        handle_message(msg.topic, decrypted_data)
    except Exception as e:
        print(f"[ENCRYPTION ERROR] Failed to decrypt message: {e}")
```
