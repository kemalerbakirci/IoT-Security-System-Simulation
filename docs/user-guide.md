# User Guide

## Getting Started

This guide will help you understand and operate the IoT Security System Simulation effectively. The system simulates a home security setup with sensors, actuators, and a centralized dashboard for monitoring and control.

## System Overview

The IoT Security System consists of:
- **3 Sensor Types**: Door, Window, and Motion sensors
- **2 Actuator Types**: Alarm and Smart Light
- **Dashboard Interface**: Real-time monitoring and manual controls
- **MQTT Communication**: Reliable message passing between components

## Dashboard Interface

### Accessing the Dashboard
1. Ensure all services are running (see [Installation Guide](installation.md))
2. Open your web browser
3. Navigate to: `http://localhost:1880/ui`

### Dashboard Components

#### 📊 Sensor Status Panel
- **Door Sensor**: Shows current state (OPEN/CLOSED)
- **Window Sensor**: Shows current state (OPEN/CLOSED)  
- **Motion Sensor**: Shows current state (MOTION/NO_MOTION)
- **Last Updated**: Timestamp of the most recent sensor reading

#### 🚨 Security Status Panel
- **System Status**: Overall security state (SECURE/BREACH)
- **Alert Message**: Displays active security alerts
- **Breach Counter**: Number of security violations detected

#### 🎛️ Manual Controls Panel
- **Alarm Toggle**: ON/OFF switch for the alarm system
- **Light Toggle**: ON/OFF switch for security lighting
- **System Reset**: Clear all alerts and reset counters

## Operating the System

### Normal Operation

#### Starting the System
1. **Launch Core Services**:
   ```bash
   # Start MQTT broker
   brew services start mosquitto
   
   # Start Node-RED
   node-red
   ```

2. **Start Sensor Simulations**:
   ```bash
   # In separate terminals:
   python -m app.door_sensor
   python -m app.window_sensor  
   python -m app.motion_sensor
   ```

3. **Start Actuator Listener**:
   ```bash
   python -m app.actuator_listener
   ```

#### Monitoring Sensor Data
- Sensor states update automatically every 2-3 seconds
- Green indicators show secure states (CLOSED, NO_MOTION)
- Red indicators show potential security breaches (OPEN, MOTION)
- Timestamps help track when events occurred

### Security Event Handling

#### Automatic Intrusion Detection
The system automatically detects security breaches when:
- Door sensor reports "OPEN"
- Window sensor reports "OPEN"  
- Motion sensor reports "MOTION"

#### Automatic Response Actions
When a breach is detected:
1. System status changes to "BREACH"
2. Alert message displays the breach type
3. Alarm can be automatically activated (if configured)
4. Security light can be automatically turned on

#### Manual Response Actions
Use the dashboard controls to:
- **Activate Alarm**: Click the alarm toggle to turn on/off
- **Control Lighting**: Click the light toggle for manual control
- **Reset System**: Clear alerts and reset breach counters

### Advanced Features

#### Persistent Session Management
- The system uses persistent MQTT sessions
- Sensor data is retained even if dashboard disconnects temporarily
- Messages are queued and delivered when connections restore

#### Quality of Service (QoS)
- All security-critical messages use QoS level 1
- Ensures "at least once" delivery for reliable operation
- Prevents message loss during network issues

## Customization Options

### Sensor Configuration

#### Adjusting Update Intervals
Modify the `interval` parameter in sensor files:
```python
# Faster updates for critical areas
simulate_motion_sensor(interval=1)  # Update every 1 second

# Slower updates for less critical sensors  
simulate_door_sensor(interval=5)    # Update every 5 seconds
```

#### Multiple Sensor Instances
Run multiple instances with unique IDs:
```bash
# Terminal 1: Front door
python -c "from app.door_sensor import simulate_door_sensor; simulate_door_sensor('front-door')"

# Terminal 2: Back door  
python -c "from app.door_sensor import simulate_door_sensor; simulate_door_sensor('back-door')"
```

### Dashboard Customization

#### Modifying Node-RED Flow
1. Open Node-RED editor: `http://localhost:1880`
2. Double-click any node to modify its properties
3. Add new nodes by dragging from the palette
4. Click "Deploy" to save changes

#### Adding New Dashboard Elements
- Drag dashboard nodes from the palette
- Configure node properties (title, layout, etc.)
- Connect to MQTT input/output nodes
- Deploy the updated flow

### MQTT Topic Structure

#### Standard Topics
```
home/security/door     # Door sensor states
home/security/window   # Window sensor states  
home/security/motion   # Motion sensor states
home/security/alarm    # Alarm control commands
home/security/light    # Light control commands
```

#### Custom Topics
Add new device types by modifying the topic structure:
```python
# Example: Adding a temperature sensor
client.publish("home/security/temperature", temperature_value)
```

## Monitoring and Logging

### Real-time Message Monitoring
Monitor all MQTT traffic:
```bash
# Subscribe to all security topics
mosquitto_sub -h localhost -t 'home/security/#' -v
```

### Python Application Logs
Each Python component outputs status messages:
```
[DOOR SENSOR] Device: door-1 | State: OPEN
[MOTION SENSOR] Device: motion-1 | State: MOTION
🚨 Alarm Activated!
💡 Light Turned ON!
```

### Node-RED Debug Output
View message flow in Node-RED:
1. Add debug nodes to your flow
2. View output in the debug panel (right sidebar)
3. Monitor message timestamps and content

## Best Practices

### System Operation
- Always start MQTT broker before other components
- Monitor sensor output for proper connectivity
- Use manual controls to test actuator responses
- Regularly check dashboard for system health

### Development & Testing
- Test individual sensors before running full system
- Use MQTT monitoring tools for debugging
- Implement gradual changes to Node-RED flows
- Keep backup copies of working configurations

### Performance Optimization
- Adjust sensor intervals based on requirements
- Monitor system resource usage
- Consider message retention policies for high-traffic scenarios
- Implement proper error handling in custom modifications

## Troubleshooting Quick Reference

### Dashboard Not Updating
1. Check MQTT broker status
2. Verify sensor processes are running
3. Refresh browser page
4. Check Node-RED debug output

### Sensors Not Publishing
1. Verify MQTT broker connection
2. Check virtual environment activation
3. Confirm Python dependencies installed
4. Review Python error messages

### Actuators Not Responding
1. Check actuator listener is running
2. Verify MQTT topic subscriptions
3. Test manual commands from dashboard
4. Monitor MQTT message flow

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting.md).

## Support and Resources

### Documentation
- [Installation Guide](installation.md) - Setup instructions
- [Architecture Guide](architecture.md) - System design details
- [API Documentation](api-documentation.md) - Developer reference

### Community Resources
- MQTT Protocol Documentation
- Node-RED User Guide  
- Python paho-mqtt Library Documentation

### Getting Help
- Check logs for error messages
- Use MQTT monitoring tools for debugging
- Refer to component-specific documentation
- Review example configurations and flows
