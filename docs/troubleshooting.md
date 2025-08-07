# Troubleshooting Guide

## Quick Diagnosis

### System Health Check
Run this quick health check to identify common issues:

```bash
# Check MQTT broker status
brew services list | grep mosquitto

# Test MQTT connectivity
mosquitto_pub -h localhost -t test/connection -m "health_check"

# Verify Python environment
python3 --version
pip list | grep paho-mqtt

# Check Node-RED status
curl -s http://localhost:1880 > /dev/null && echo "Node-RED: OK" || echo "Node-RED: FAILED"

# Verify dashboard access
curl -s http://localhost:1880/ui > /dev/null && echo "Dashboard: OK" || echo "Dashboard: FAILED"
```

## Common Issues and Solutions

### 1. MQTT Connection Problems

#### Issue: "Connection refused" errors
```
[ERROR] MQTT Connection failed (rc=5)
```

**Diagnosis:**
```bash
# Check if Mosquitto is running
brew services list | grep mosquitto
# or
ps aux | grep mosquitto

# Test direct connection
telnet localhost 1883
```

**Solutions:**
```bash
# Start Mosquitto service
brew services start mosquitto

# If port 1883 is in use
lsof -i :1883
sudo kill -9 <PID>

# Restart with verbose logging
mosquitto -v
```

#### Issue: "Network unreachable" errors
```
socket.gaierror: [Errno 8] nodename nor servname provided
```

**Solutions:**
- Check network connectivity
- Verify broker URL in configuration
- Ensure firewall allows port 1883

```bash
# Test network connectivity
ping localhost

# Check firewall settings (macOS)
sudo pfctl -sr | grep 1883
```

### 2. Python Environment Issues

#### Issue: Module import errors
```
ModuleNotFoundError: No module named 'paho.mqtt'
```

**Diagnosis:**
```bash
# Check virtual environment
which python
echo $VIRTUAL_ENV

# List installed packages
pip list
```

**Solutions:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# If virtual environment is corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Python version compatibility
```
SyntaxError: invalid syntax (Python 2.x detected)
```

**Solutions:**
```bash
# Check Python version
python3 --version

# Ensure Python 3.8+
brew install python@3.9

# Update virtual environment
python3.9 -m venv venv
```

### 3. Node-RED Issues

#### Issue: Node-RED won't start
```
Error: listen EADDRINUSE :::1880
```

**Diagnosis:**
```bash
# Check what's using port 1880
lsof -i :1880
netstat -an | grep 1880
```

**Solutions:**
```bash
# Kill existing Node-RED process
pkill node-red

# Or kill specific process
sudo kill -9 <PID>

# Start with different port
node-red --port 1881
```

#### Issue: Dashboard not loading
The dashboard page shows "Cannot GET /ui"

**Solutions:**
1. **Install dashboard module:**
   ```bash
   npm install -g node-red-dashboard
   ```

2. **Import flows correctly:**
   - Open Node-RED editor: http://localhost:1880
   - Menu → Import → Select flows.json
   - Ensure all nodes are properly connected
   - Click Deploy

3. **Check dashboard configuration:**
   - Verify dashboard nodes have group assignments
   - Check that dashboard is configured in Node-RED settings

#### Issue: Node-RED flow import errors
```
Error: Flow import failed - invalid JSON
```

**Solutions:**
```bash
# Validate JSON format
python3 -m json.tool flows.json

# Check for UTF-8 encoding issues
file flows.json
```

### 4. Sensor Communication Issues

#### Issue: Sensors not publishing data
No output in terminal or dashboard not updating

**Diagnosis:**
```bash
# Monitor MQTT traffic
mosquitto_sub -h localhost -t 'home/security/#' -v

# Check sensor process status
ps aux | grep python
```

**Solutions:**
1. **Verify MQTT client creation:**
   ```python
   # Add debug logging to mqtt_client.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check sensor loop execution:**
   ```python
   # Add print statements in sensor files
   print(f"[DEBUG] Starting sensor loop...")
   print(f"[DEBUG] Publishing: {state}")
   ```

3. **Verify topic subscriptions:**
   ```bash
   # Test manual publishing
   mosquitto_pub -h localhost -t home/security/door -m "TEST"
   ```

#### Issue: Intermittent sensor data loss
Sensors publish but messages don't reach dashboard

**Diagnosis:**
- Check QoS levels
- Monitor network stability
- Verify persistent session configuration

**Solutions:**
```python
# Increase QoS level
client.publish(topic, state, qos=2)  # Exactly once delivery

# Enable message logging
def on_publish(client, userdata, mid):
    print(f"[MQTT] Message {mid} published successfully")

client.on_publish = on_publish
```

### 5. Dashboard Display Issues

#### Issue: Dashboard shows old data
Real-time updates not working properly

**Solutions:**
1. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R)
   - Clear browser cache and cookies

2. **Check MQTT node configuration:**
   - Verify MQTT input nodes are connected
   - Check topic subscription patterns
   - Ensure QoS settings match sensor publishing

3. **Restart Node-RED flow:**
   ```bash
   # In Node-RED editor
   # Click Deploy → Full Deploy
   ```

#### Issue: Controls not working
Manual alarm/light controls don't respond

**Diagnosis:**
```bash
# Monitor actuator commands
mosquitto_sub -h localhost -t 'home/security/alarm' -v
mosquitto_sub -h localhost -t 'home/security/light' -v
```

**Solutions:**
1. **Check actuator listener:**
   ```bash
   # Ensure actuator_listener.py is running
   python -m app.actuator_listener
   ```

2. **Verify MQTT output nodes:**
   - Check Node-RED MQTT output configuration
   - Ensure correct topic names
   - Verify QoS settings

### 6. Performance Issues

#### Issue: High CPU usage
System becomes slow with multiple sensors running

**Diagnosis:**
```bash
# Monitor system resources
top
htop

# Check Python process usage
ps aux | grep python | sort -k3 -nr
```

**Solutions:**
1. **Adjust sensor intervals:**
   ```python
   # Increase interval to reduce CPU load
   simulate_door_sensor(interval=10)  # Update every 10 seconds
   ```

2. **Optimize MQTT settings:**
   ```python
   # Reduce QoS for non-critical sensors
   client.publish(topic, state, qos=0)  # Fire and forget
   ```

3. **Implement connection pooling:**
   ```python
   # Share MQTT client between sensors (advanced)
   ```

#### Issue: Memory leaks
Memory usage increases over time

**Solutions:**
```python
# Add garbage collection
import gc

def sensor_with_gc():
    message_count = 0
    while True:
        # Normal sensor logic
        publish_data()
        
        message_count += 1
        if message_count % 1000 == 0:
            gc.collect()
```

### 7. Network and Connectivity Issues

#### Issue: "Address already in use" errors
Port conflicts preventing service startup

**Diagnosis:**
```bash
# Check all ports in use
netstat -tulpn | grep LISTEN

# Check specific ports
lsof -i :1883  # MQTT
lsof -i :1880  # Node-RED
```

**Solutions:**
```bash
# Kill processes using ports
sudo kill -9 $(lsof -t -i:1883)
sudo kill -9 $(lsof -t -i:1880)

# Use alternative ports
mosquitto -p 1884
node-red --port 1881
```

#### Issue: Firewall blocking connections
Services start but can't communicate

**Solutions (macOS):**
```bash
# Check firewall status
sudo pfctl -s info

# Allow specific ports
sudo pfctl -f /etc/pf.conf
```

## Advanced Troubleshooting

### Debug Mode Configuration

#### Enable MQTT Debug Logging
```python
# Add to mqtt_client.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable paho-mqtt debug
import paho.mqtt.client as mqtt
mqtt.enable_logger(logging.getLogger("paho"))
```

#### Node-RED Debug Output
1. Add debug nodes to your flow
2. Connect debug nodes to message paths
3. View output in debug panel (right sidebar)
4. Use console.log() in function nodes:
   ```javascript
   console.log("Debug message:", msg.payload);
   return msg;
   ```

### System Monitoring Tools

#### MQTT Traffic Analysis
```bash
# Monitor all MQTT traffic with timestamps
mosquitto_sub -h localhost -t '#' -v -F '@Y-@m-@d @H:@M:@S: %t %p'

# Count messages per topic
mosquitto_sub -h localhost -t '#' | sort | uniq -c

# Monitor specific sensor
mosquitto_sub -h localhost -t 'home/security/door' -v
```

#### Performance Monitoring
```bash
# Monitor system resources continuously
watch -n 1 'ps aux | grep -E "(python|node-red|mosquitto)" | head -10'

# Network connection monitoring
watch -n 1 'netstat -an | grep -E "(1880|1883)"'

# Memory usage tracking
watch -n 5 'free -h'  # Linux
watch -n 5 'vm_stat'  # macOS
```

### Log File Analysis

#### Node-RED Logs
```bash
# Find Node-RED log location
node-red --help | grep -i log

# Typical log locations:
tail -f ~/.node-red/node-red.log
```

#### System Logs (macOS)
```bash
# Console application logs
log show --predicate 'subsystem == "com.apple.network"' --last 1h

# Mosquitto logs (if configured)
tail -f /usr/local/var/log/mosquitto/mosquitto.log
```

### Configuration Validation

#### MQTT Configuration Test
```python
#!/usr/bin/env python3
"""MQTT Configuration Validator"""

import paho.mqtt.client as mqtt
import sys
import time

def test_mqtt_connection():
    """Test basic MQTT connectivity"""
    print("Testing MQTT connection...")
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ MQTT connection successful")
            client.publish("test/config", "validation_test")
        else:
            print(f"❌ MQTT connection failed (rc={rc})")
            sys.exit(1)
    
    def on_message(client, userdata, msg):
        print(f"✅ Message received: {msg.topic} = {msg.payload.decode()}")
        client.disconnect()
    
    client = mqtt.Client("config_validator")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect("localhost", 1883, 60)
        client.subscribe("test/config")
        client.loop_start()
        time.sleep(2)
        client.loop_stop()
        print("✅ MQTT configuration valid")
    except Exception as e:
        print(f"❌ MQTT configuration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_mqtt_connection()
```

#### Node-RED Flow Validation
```bash
# Validate flows.json syntax
python3 -c "
import json
try:
    with open('flows.json', 'r') as f:
        data = json.load(f)
    print('✅ flows.json is valid JSON')
    print(f'📊 Contains {len(data)} nodes')
except Exception as e:
    print(f'❌ flows.json error: {e}')
"
```

## Recovery Procedures

### Complete System Reset
```bash
#!/bin/bash
# complete_reset.sh - Reset entire system to working state

echo "🔄 Performing complete system reset..."

# Stop all services
echo "Stopping services..."
brew services stop mosquitto
pkill node-red
pkill -f "python.*sensor"
pkill -f "python.*actuator"

# Clean temporary files
echo "Cleaning temporary files..."
rm -rf ~/.node-red/node_modules/.cache
rm -rf /tmp/mosquitto*

# Reset virtual environment
echo "Resetting Python environment..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Restart services
echo "Restarting services..."
brew services start mosquitto
sleep 2
node-red &
sleep 5

# Verify system
echo "Verifying system health..."
curl -s http://localhost:1880 && echo "✅ Node-RED OK" || echo "❌ Node-RED Failed"
mosquitto_pub -h localhost -t test -m "ok" && echo "✅ MQTT OK" || echo "❌ MQTT Failed"

echo "🎉 System reset complete"
```

### Backup and Restore
```bash
# Create system backup
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
cp flows.json backups/$(date +%Y%m%d_%H%M%S)/
cp -r ~/.node-red backups/$(date +%Y%m%d_%H%M%S)/node-red-config
cp requirements.txt backups/$(date +%Y%m%d_%H%M%S)/

# Restore from backup
BACKUP_DIR="backups/20241201_120000"  # Adjust date
cp $BACKUP_DIR/flows.json .
cp -r $BACKUP_DIR/node-red-config ~/.node-red
```

## Getting Help

### Documentation Resources
- [Installation Guide](installation.md) - Setup procedures
- [User Guide](user-guide.md) - Operating instructions
- [Architecture Guide](architecture.md) - System design
- [API Documentation](api-documentation.md) - Technical reference

### Community Support
- **MQTT Resources**: [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- **Node-RED Community**: [Node-RED Forum](https://discourse.nodered.org/)
- **Python MQTT**: [paho-mqtt Documentation](https://pypi.org/project/paho-mqtt/)

### Debugging Checklist
Before seeking help, ensure you have:
- [ ] Checked all service status (MQTT, Node-RED)
- [ ] Verified network connectivity
- [ ] Reviewed error logs
- [ ] Tested with minimal configuration
- [ ] Attempted system restart
- [ ] Checked documentation for similar issues

### Creating Support Requests
When reporting issues, include:
1. **System Information**:
   - Operating system and version
   - Python version (`python3 --version`)
   - Node.js version (`node --version`)
   - Mosquitto version (`mosquitto --help`)

2. **Error Details**:
   - Complete error messages
   - Steps to reproduce
   - Expected vs. actual behavior

3. **Configuration**:
   - Modified settings
   - Custom code changes
   - Environment variables

4. **Logs**:
   - MQTT broker logs
   - Node-RED output
   - Python error traces
   - System resource usage
