# Installation & Setup Guide

## Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: Version 3.8 or higher
- **Node.js**: Version 14 or higher (for Node-RED)
- **Memory**: Minimum 2GB RAM
- **Network**: Local network access

### Required Software
- Python 3.8+
- pip (Python package manager)
- Node.js and npm
- Git (for cloning repository)

## Step-by-Step Installation

### 1. Environment Setup

#### Clone the Repository
```bash
git clone https://github.com/your-username/IoT-Security-System-Simulation.git
cd IoT-Security-System-Simulation
```

#### Create Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. MQTT Broker Installation

#### Option A: Using Homebrew (macOS)
```bash
# Install Mosquitto MQTT broker
brew install mosquitto

# Start Mosquitto service
brew services start mosquitto

# Verify installation
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```

#### Option B: Using Docker
```bash
# Pull and run Mosquitto container
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto

# Or with persistent storage
docker run -it -p 1883:1883 -p 9001:9001 \
  -v mosquitto.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto
```

#### Option C: Manual Installation (Linux)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Start service
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### 3. Node-RED Installation

#### Install Node-RED Globally
```bash
npm install -g node-red
```

#### Install Required Node-RED Modules
```bash
# Install dashboard module
npm install -g node-red-dashboard

# Install MQTT module (usually pre-installed)
npm install -g node-red-contrib-mqtt-broker
```

#### Start Node-RED
```bash
node-red
```

Access Node-RED at: `http://localhost:1880`

### 4. Project Configuration

#### Environment Configuration
Create a configuration file (if not using default settings):
```bash
mkdir -p config
cat > config/settings.env << EOF
BROKER_URL=localhost
BROKER_PORT=1883
EOF
```

#### Import Node-RED Flow
1. Open Node-RED in browser: `http://localhost:1880`
2. Click on the hamburger menu (three lines) → Import
3. Select the `flows.json` file from the project root
4. Click "Deploy" to activate the flow

### 5. Verification

#### Test MQTT Connectivity
```bash
# Terminal 1: Subscribe to test topic
mosquitto_sub -h localhost -t test/message

# Terminal 2: Publish test message
mosquitto_pub -h localhost -t test/message -m "Connection successful"
```

#### Test Python MQTT Client
```bash
# Run a quick sensor test
python3 -c "
from app.mqtt_client import create_client
import time

client = create_client('test-client')
client.loop_start()
client.publish('test/python', 'Python MQTT working')
time.sleep(1)
client.loop_stop()
client.disconnect()
print('Python MQTT client test completed')
"
```

## Running the System

### 1. Start Core Services
```bash
# Start MQTT broker (if not already running)
brew services start mosquitto

# Start Node-RED (if not already running)
node-red
```

### 2. Launch Sensor Simulations
Open separate terminal windows for each sensor:

```bash
# Terminal 1: Door sensor
source venv/bin/activate
python -m app.door_sensor

# Terminal 2: Window sensor
source venv/bin/activate
python -m app.window_sensor

# Terminal 3: Motion sensor
source venv/bin/activate
python -m app.motion_sensor

# Terminal 4: Actuator listener
source venv/bin/activate
python -m app.actuator_listener
```

### 3. Access Dashboard
Open your web browser and navigate to:
- **Node-RED Editor**: `http://localhost:1880`
- **Dashboard**: `http://localhost:1880/ui`

## Troubleshooting

### Common Issues

#### MQTT Connection Failed
```bash
# Check if Mosquitto is running
brew services list | grep mosquitto

# Test broker connectivity
telnet localhost 1883
```

#### Python Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### Node-RED Dashboard Not Loading
```bash
# Restart Node-RED
pkill node-red
node-red

# Check Node-RED logs for errors
# Logs are typically displayed in the terminal where node-red was started
```

#### Port Conflicts
```bash
# Check what's using port 1883
lsof -i :1883

# Check what's using port 1880
lsof -i :1880
```

### Debugging Tips

#### Enable Debug Logging
Modify Python scripts to enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### MQTT Message Monitoring
```bash
# Monitor all MQTT messages
mosquitto_sub -h localhost -t '#' -v
```

#### Check System Resources
```bash
# Monitor CPU and memory usage
top
# or
htop
```

## Configuration Options

### Sensor Configuration
Modify sensor behavior by editing the Python files:

```python
# In door_sensor.py, window_sensor.py, motion_sensor.py
def simulate_sensor(device_id="sensor-1", interval=3, qos=1):
    # interval: seconds between state changes
    # qos: MQTT Quality of Service level (0, 1, or 2)
    # device_id: unique identifier for the sensor
```

### MQTT Broker Configuration
For advanced configurations, create a custom Mosquitto config file:

```bash
# Create mosquitto.conf
cat > mosquitto.conf << EOF
listener 1883
allow_anonymous true
persistence true
persistence_location /tmp/mosquitto/
log_dest file /tmp/mosquitto.log
EOF

# Start with custom config
mosquitto -c mosquitto.conf
```

### Node-RED Configuration
Node-RED settings can be modified in `~/.node-red/settings.js`

## Next Steps
After successful installation, refer to:
- [User Guide](user-guide.md) for operating the system
- [API Documentation](api-documentation.md) for customization
- [Troubleshooting Guide](troubleshooting.md) for issue resolution
