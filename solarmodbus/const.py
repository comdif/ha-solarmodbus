"""
Global constants for the Solarmodbus integration.
This file centralizes all fixed values used across the integration.
"""

DOMAIN = "solarmodbus"

SUPPORTED_MODES = ["modbus", "serial", "solarman"]

DEFAULT_MODE = "modbus"

DEFAULT_HOST = "192.168.1.100"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1

DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_SERIAL_BAUDRATE = 9600
DEFAULT_SERIAL_PARITY = "N"
DEFAULT_SERIAL_STOPBITS = 1
DEFAULT_SERIAL_BYTESIZE = 8

DEFAULT_SCAN_INTERVAL = 2

PLATFORMS = ["sensor"]

DEFAULT_TIMEOUT = 5
DEFAULT_MESSAGE_WAIT = 50

COORDINATOR_NAME = "coordinator"

DEFINITIONS_PATH = "custom_components/solarmodbus/inverter_definitions"

DEFAULT_MODEL = "deye_hybrid.yaml"
