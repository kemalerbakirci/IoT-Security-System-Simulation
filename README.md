# IoT Security System Simulation

## 📌 Overview
This project demonstrates a **professional IoT-based Home Security System** using **MQTT** for communication and **Node-RED** for visualization and control. It simulates a complete security infrastructure with **door, window, and motion sensors**, intelligent intrusion detection, and automated response systems through virtual actuators (**alarm and smart lighting**).

The system showcases real-world IoT architecture patterns, including persistent messaging, quality of service guarantees, and scalable device management - making it an excellent learning platform for IoT development and a solid foundation for production security systems.

---

## � Key Features
✅ **Multi-Sensor Integration**: Door, window, and motion sensors with real-time state monitoring  
✅ **Reliable Communication**: Persistent MQTT sessions with QoS level 1 for guaranteed message delivery  
✅ **Interactive Dashboard**: Professional Node-RED interface with live sensor visualization  
✅ **Intelligent Detection**: Advanced intrusion detection logic with customizable alert thresholds  
✅ **Automated Response**: Smart actuator control (alarm systems and security lighting)  
✅ **Manual Override**: Dashboard controls for system testing and emergency operations  
✅ **Production-Ready Code**: Modular, documented, and extensible Python architecture  
✅ **Comprehensive Documentation**: Full API reference, troubleshooting guides, and learning materials  

---

## 📂 Project Structure
```
IoT-Security-System-Simulation/
├── app/                       # Core application modules
│   ├── mqtt_client.py         # Reusable MQTT client with connection management
│   ├── door_sensor.py         # Door sensor simulation with state tracking
│   ├── window_sensor.py       # Window sensor with security monitoring
│   ├── motion_sensor.py       # PIR motion detection simulation
│   └── actuator_listener.py   # Actuator command processor
├── docs/                      # Complete documentation suite
│   ├── installation.md        # Step-by-step setup guide
│   ├── user-guide.md          # Operating instructions and best practices
│   ├── architecture.md        # System design and technical overview
│   ├── api-documentation.md   # Developer API reference
│   ├── troubleshooting.md     # Issue resolution and debugging
│   └── learning-guide.md      # Comprehensive IoT and MQTT tutorial
├── assets/                    # Visual documentation
│   ├── dashboard_example.png  # Dashboard screenshot
│   └── node_red_flow.png      # Flow diagram
├── requirements.txt           # Python dependencies
├── flows.json                 # Node-RED flow configuration
├── Learning_Guide_IoT_Security.txt  # Legacy learning material
└── LICENSE                    # MIT license

---

## �️ System Architecture

### Communication Flow
```
[Sensors] → [MQTT Broker] → [Node-RED Dashboard] → [Decision Logic] → [Actuators]
     ↓              ↓               ↓                    ↓              ↓
[Python Scripts] [Mosquitto] [Real-time UI] [Intrusion Detection] [Response Systems]
```

### Technology Stack
- **Backend**: Python 3.8+ with paho-mqtt library
- **Message Broker**: Eclipse Mosquitto MQTT broker
- **Frontend**: Node-RED dashboard with real-time visualization
- **Protocol**: MQTT with QoS level 1 for reliable delivery
- **Architecture**: Publish-Subscribe pattern with persistent sessions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ (for Node-RED)
- Mosquitto MQTT broker

### Installation
```bash
# Clone the repository
git clone <your-repository-url>
cd IoT-Security-System-Simulation

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install and start MQTT broker (macOS)
brew install mosquitto
brew services start mosquitto

# Install Node-RED
npm install -g node-red
```

### Running the System
```bash
# Terminal 1: Start Node-RED
node-red

# Terminal 2-4: Start sensors (separate terminals)
python -m app.door_sensor
python -m app.window_sensor
python -m app.motion_sensor

# Terminal 5: Start actuator listener
python -m app.actuator_listener
```

### Access Points
- **Node-RED Editor**: http://localhost:1880
- **Security Dashboard**: http://localhost:1880/ui

---

## 📚 Documentation

### Complete Documentation Suite
Our comprehensive documentation covers everything from basic setup to advanced customization:

- **[Installation Guide](docs/installation.md)** - Detailed setup instructions for all platforms
- **[User Guide](docs/user-guide.md)** - Complete operating instructions and best practices
- **[System Architecture](docs/architecture.md)** - Technical overview and design patterns
- **[API Documentation](docs/api-documentation.md)** - Developer reference and code examples
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- **[Learning Guide](docs/learning-guide.md)** - Comprehensive IoT and MQTT tutorial

### Quick References
- **MQTT Topics**: `home/security/{door|window|motion}` for sensors, `home/security/{alarm|light}` for actuators
- **Message Format**: Plain text (`"OPEN"`, `"CLOSED"`, `"MOTION"`, `"NO_MOTION"`, `"ON"`, `"OFF"`)
- **QoS Level**: 1 (at least once delivery)
- **Session Type**: Persistent (`clean_session=False`)

---

## 🖥️ Dashboard Interface

![Node-RED Dashboard](assets/dashboard_example.png)

### Features
- **Real-time Sensor Monitoring**: Live updates from all connected sensors
- **Security Status Panel**: Overall system state and breach detection
- **Manual Controls**: Emergency override switches for testing and control
- **Visual Indicators**: Color-coded status lights and alerts
- **Historical Data**: Event logging and system activity tracking

---

## 🔧 Customization and Extension

### Adding New Sensors
```python
# Example: Temperature sensor
from app.mqtt_client import create_client

def simulate_temperature_sensor():
    client = create_client("temp-sensor-001")
    # Sensor implementation here
```

### Custom Actuators
Extend the system with additional actuator types by modifying `actuator_listener.py` and adding corresponding MQTT topics.

### Dashboard Customization
Import the `flows.json` file into Node-RED and customize:
- Add new dashboard widgets
- Modify sensor layouts
- Implement custom logic nodes
- Create additional visualizations

---

## 🎯 Use Cases and Applications

### Educational Applications
- **IoT Learning Platform**: Hands-on experience with MQTT, sensors, and dashboards
- **System Integration**: Understanding pub-sub patterns and distributed systems
- **Security Concepts**: Learning about intrusion detection and automated response

### Development Platform
- **Prototyping**: Foundation for real-world security system development
- **Testing**: Simulation environment for algorithm testing
- **Integration**: Base for connecting real hardware sensors

### Production Foundation
- **Smart Homes**: Home automation and security systems
- **Commercial Security**: Office and retail monitoring systems
- **Industrial IoT**: Equipment monitoring and facility security

---
## 🤝 Contributing

We welcome contributions to improve this IoT security system! Here's how you can help:

### Types of Contributions
- **Bug Reports**: Found an issue? Let us know!
- **Feature Requests**: Ideas for new capabilities
- **Code Improvements**: Performance optimizations and refactoring
- **Documentation**: Help improve our guides and examples
- **New Sensors/Actuators**: Extend the system with additional devices

### Development Setup
```bash
# Fork the repository and clone your fork
git clone <your-fork-url>
cd IoT-Security-System-Simulation

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and test thoroughly
python -m pytest tests/  # Run tests if available

# Submit a pull request
```

### Code Standards
- Follow PEP 8 for Python code
- Add documentation for new features
- Include examples for new sensors/actuators
- Test your changes thoroughly

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Commercial use allowed
- ✅ Modification and distribution permitted
- ✅ Private use welcome
- ✅ No warranty provided

---

## 🔗 Related Projects and Resources

### Learning Resources
- **[MQTT.org](https://mqtt.org/)** - Official MQTT protocol documentation
- **[Node-RED Documentation](https://nodered.org/docs/)** - Complete Node-RED guide
- **[paho-mqtt](https://pypi.org/project/paho-mqtt/)** - Python MQTT client library

### Similar Projects
- **Home Assistant** - Open-source home automation platform
- **OpenHAB** - Vendor-neutral home automation system
- **ThingsBoard** - IoT platform for data collection and visualization

### Hardware Integration
- **Raspberry Pi** - Popular platform for IoT projects
- **Arduino** - Microcontroller platform for sensors
- **ESP32/ESP8266** - WiFi-enabled microcontrollers

---

## 📞 Support and Community

### Getting Help
1. **Check Documentation**: Start with our comprehensive [docs](docs/) folder
2. **Search Issues**: Look through existing GitHub issues
3. **Create an Issue**: Report bugs or request features
4. **Community Forums**: Join IoT and MQTT communities

### Stay Connected
- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and community interaction
- **Wiki**: Additional documentation and examples

---

## 🎉 Acknowledgments

Special thanks to:
- **Eclipse Mosquitto** team for the excellent MQTT broker
- **Node-RED** community for the powerful visual programming platform
- **paho-mqtt** developers for the reliable Python MQTT client
- **IoT community** for inspiration and best practices

Built with ❤️ for the IoT community
