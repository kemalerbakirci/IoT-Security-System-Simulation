# System Architecture

## Overview

The IoT Security System Simulation follows a distributed architecture pattern using MQTT as the communication backbone. This design ensures scalability, reliability, and real-time data exchange between sensors, actuators, and the control interface.

## Architecture Components

### 1. MQTT Broker (Mosquitto)
- **Role**: Central message hub for all IoT communications
- **Configuration**: Local instance running on port 1883
- **Features**: 
  - Message persistence
  - QoS level support (0, 1, 2)
  - Retained messages for device state
  - Session persistence for reliable delivery

### 2. Sensor Layer
The sensor layer consists of three primary components:

#### Door Sensor (`door_sensor.py`)
- **Topic**: `home/security/door`
- **States**: `OPEN`, `CLOSED`
- **Publishing Interval**: 3 seconds
- **QoS Level**: 1 (At least once delivery)

#### Window Sensor (`window_sensor.py`)
- **Topic**: `home/security/window`
- **States**: `OPEN`, `CLOSED`
- **Publishing Interval**: 3 seconds
- **QoS Level**: 1 (At least once delivery)

#### Motion Sensor (`motion_sensor.py`)
- **Topic**: `home/security/motion`
- **States**: `MOTION`, `NO_MOTION`
- **Publishing Interval**: 2 seconds (more frequent for security)
- **QoS Level**: 1 (At least once delivery)

### 3. Control & Visualization Layer (Node-RED)
- **Dashboard UI**: Real-time sensor monitoring
- **Business Logic**: Intrusion detection algorithms
- **Manual Controls**: Alarm and light toggle switches
- **Data Processing**: Message filtering and state management

### 4. Actuator Layer
The actuator listener (`actuator_listener.py`) subscribes to control commands:

#### Alarm System
- **Topic**: `home/security/alarm`
- **Commands**: `ON`, `OFF`
- **Trigger Conditions**: Any sensor breach

#### Smart Lighting
- **Topic**: `home/security/light`
- **Commands**: `ON`, `OFF`
- **Usage**: Security lighting activation

## Data Flow

```
[Sensors] → [MQTT Broker] → [Node-RED Dashboard]
                ↓
[Actuator Listener] ← [MQTT Broker] ← [Control Logic]
```

### Message Flow Sequence

1. **Sensor Data Publishing**:
   ```
   Sensor → MQTT Broker (topic: home/security/{sensor_type})
   ```

2. **Dashboard Subscription**:
   ```
   MQTT Broker → Node-RED (displays real-time status)
   ```

3. **Intrusion Detection**:
   ```
   Node-RED Logic → Decision Making → Actuator Commands
   ```

4. **Actuator Control**:
   ```
   Node-RED → MQTT Broker → Actuator Listener
   ```

## Communication Protocol

### MQTT Topic Structure
```
home/security/
├── door          # Door sensor states
├── window        # Window sensor states
├── motion        # Motion detection
├── alarm         # Alarm control commands
└── light         # Light control commands
```

### Message Format
All messages are published as plain text strings for simplicity:
- Sensor messages: `"OPEN"`, `"CLOSED"`, `"MOTION"`, `"NO_MOTION"`
- Actuator commands: `"ON"`, `"OFF"`

### Quality of Service (QoS)
- **QoS 1**: Used for all security-critical messages
- **Persistent Sessions**: Enabled (`clean_session=False`)
- **Retained Messages**: Not used in current implementation

## Scalability Considerations

### Horizontal Scaling
- Multiple sensor instances can be deployed with unique client IDs
- Node-RED can handle multiple dashboard instances
- MQTT broker can be clustered for high availability

### Vertical Scaling
- Sensor publishing intervals can be adjusted based on requirements
- Buffer sizes and connection pools can be optimized
- Database integration can be added for historical data

## Security Considerations

### Current Implementation
- Local network communication only
- No authentication/authorization
- Plain text message format

### Production Recommendations
- Enable MQTT authentication (username/password)
- Implement TLS/SSL encryption
- Use certificate-based authentication
- Add message payload encryption
- Implement access control lists (ACLs)

## Performance Characteristics

### Latency
- Sensor to dashboard: < 100ms (local network)
- Command to actuator: < 50ms (local network)

### Throughput
- Current load: ~1 message/second per sensor
- Broker capacity: 1000+ messages/second (Mosquitto)

### Resource Usage
- Memory: ~10MB per sensor process
- CPU: Minimal (<1% per sensor)
- Network: ~1KB/minute per sensor
