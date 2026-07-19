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
)

from .coordinator import SolarmodbusCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True


def load_yaml_file(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    mode = entry.data.get("mode")
    host = entry.data.get("host")
    port = entry.data.get("port")
    serial_port = entry.data.get("serial_port")
    model = entry.data.get("model")

    # --- Solarman logger serial (must be int) ---
    if mode == "solarman":
        serial_number_raw = entry.data.get("logger_serial_number")
        try:
            serial_number = int(serial_number_raw)
        except Exception:
            raise ConfigEntryNotReady(
                f"Invalid Solarman serial number (must be integer): {serial_number_raw}"
            )
    else:
        serial_number = entry.data.get("slave_id")

    # --- Load YAML definition ---
    yaml_path = os.path.join(
        hass.config.path(DEFINITIONS_PATH),
        model,
    )
    definition = await hass.async_add_executor_job(load_yaml_file, yaml_path)

    # --- Coordinator creation ---
    coordinator = SolarmodbusCoordinator(
        hass=hass,
        mode=mode,
        host=host,
        port=port,
        serial_port=serial_port,
        slave_id=serial_number,
        definition=definition,
    )

    # --- First refresh ---
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Unable to initialize Solarmodbus connection: %s", err)
        raise ConfigEntryNotReady from err

    # --- Store coordinator ---
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR_NAME: coordinator,
        "definition": definition,
    }

    # --- Write register service ---
    async def async_write_register(call):
        address = call.data["address"]
        value = call.data["value"]
        result = await hass.async_add_executor_job(
            coordinator.write_register, address, value
        )
        _LOGGER.info("Write result: %s", result)

    hass.services.async_register(DOMAIN, "write_register", async_write_register)

    # --- Forward platforms ---
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Solarmodbus integration initialized successfully")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
