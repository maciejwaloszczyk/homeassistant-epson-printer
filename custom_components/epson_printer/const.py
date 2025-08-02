"""Constants for the Epson Printer integration."""

DOMAIN = "epson_printer"

# Configuration keys
CONF_HOST = "host"
CONF_UPDATE_INTERVAL = "update_interval"

# Default values
DEFAULT_UPDATE_INTERVAL = 3600  # seconds (1 hour)

# Sensor types
SENSOR_TYPES = {
    "black": {
        "name": "Black Ink",
        "icon": "mdi:printer-3d-nozzle",
        "unit": "%",
        "device_class": None,
    },
    "magenta": {
        "name": "Magenta Ink",
        "icon": "mdi:printer-3d-nozzle",
        "unit": "%",
        "device_class": None,
    },
    "cyan": {
        "name": "Cyan Ink",
        "icon": "mdi:printer-3d-nozzle",
        "unit": "%",
        "device_class": None,
    },
    "yellow": {
        "name": "Yellow Ink",
        "icon": "mdi:printer-3d-nozzle",
        "unit": "%",
        "device_class": None,
    },
    "clean": {
        "name": "Cleaning Cartridge",
        "icon": "mdi:printer-3d-nozzle-heat",
        "unit": "%",
        "device_class": None,
    },
}
