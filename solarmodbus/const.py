"""
Global constants for the Solarmodbus integration.
This file centralizes all fixed values used across the integration.
"""

# Home Assistant domain name (must match the folder name in custom_components)
DOMAIN = "solarmodbus"

# Supported connection modes:
# - "modbus" = Modbus TCP (RS485 → Ethernet gateway)
# - "serial" = Modbus RTU over a local USB/RS485 adapter directly connected to the HA server
SUPPORTED_MODES = ["modbus", "serial"]

# Default connection mode (Modbus TCP)
DEFAULT_MODE = "modbus"

# Default Modbus TCP parameters
DEFAULT_HOST = "192.168.1.100"   # Default inverter or RS485-to-TCP gateway IP
DEFAULT_PORT = 502               # Standard Modbus TCP port
DEFAULT_SLAVE_ID = 1             # Modbus slave ID (usually 1)

# Default Serial (USB/RS485) parameters for Modbus RTU
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"   # Typical USB/RS485 adapter path on Linux
DEFAULT_SERIAL_BAUDRATE = 9600         # Common inverter baudrate
DEFAULT_SERIAL_PARITY = "N"            # Parity: N = None, E = Even, O = Odd
DEFAULT_SERIAL_STOPBITS = 1            # Stop bits
DEFAULT_SERIAL_BYTESIZE = 8            # Data bits

# Update interval (seconds)
DEFAULT_SCAN_INTERVAL = 2

# Platforms exposed by the integration
PLATFORMS = ["sensor"]

# Modbus timeout (seconds)
DEFAULT_TIMEOUT = 5

# Delay between Modbus messages (milliseconds)
DEFAULT_MESSAGE_WAIT = 50

# Name used to store the DataUpdateCoordinator inside hass.data
COORDINATOR_NAME = "coordinator"

# Path to YAML inverter definition files
DEFINITIONS_PATH = "custom_components/solarmodbus/inverter_definitions"

# Default inverter model (simple starting point)
DEFAULT_MODEL = "deye_hybrid.yaml"
