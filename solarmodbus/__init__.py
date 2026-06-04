import logging
import os
import yaml

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    DOMAIN,
    PLATFORMS,
    COORDINATOR_NAME,
    DEFINITIONS_PATH,
    DEFAULT_MODEL,
)
from .coordinator import SolarmodbusCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration from configuration.yaml (not used)."""
    hass.data.setdefault(DOMAIN, {})
    return True


def load_yaml_file(path: str):
    """Load a YAML file from disk."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a Solarmodbus config entry."""
    mode = entry.data.get("mode")          # "modbus" or "serial"
    host = entry.data.get("host")          # Only for TCP
    port = entry.data.get("port")          # TCP port
    serial_port = entry.data.get("serial_port")  # Only for RTU
    slave_id = entry.data.get("slave_id")

    # Load inverter definition YAML
    yaml_path = os.path.join(
        hass.config.path(DEFINITIONS_PATH),
        DEFAULT_MODEL,
    )

    definition = await hass.async_add_executor_job(load_yaml_file, yaml_path)

    # Create coordinator
    coordinator = SolarmodbusCoordinator(
        hass=hass,
        mode=mode,
        host=host,
        port=port,
        serial_port=serial_port,
        slave_id=slave_id,
        definition=definition,
    )

    # First data refresh
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Unable to initialize Solarmodbus connection: %s", err)
        raise ConfigEntryNotReady from err

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR_NAME: coordinator,
        "definition": definition,
    }

    # Load platforms (sensor)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Solarmodbus integration initialized successfully")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
