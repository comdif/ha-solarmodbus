from __future__ import annotations

import logging
import socket
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    DOMAIN,
    DEFAULT_MODE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_SERIAL_PORT,
    SUPPORTED_MODES,
)

_LOGGER = logging.getLogger(__name__)

CONF_MODE = "mode"
CONF_SLAVE_ID = "slave_id"
CONF_SERIAL_PORT = "serial_port"


def _test_tcp_connection(host: str, port: int, timeout: float = 2.0) -> bool:
    """Simple TCP connection test."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Solarmodbus integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """First step: choose connection mode."""
        errors = {}

        if user_input is not None:
            mode = user_input[CONF_MODE]

            if mode == "modbus":
                return await self.async_step_modbus()
            else:
                return await self.async_step_serial()

        schema = vol.Schema({
            vol.Required(CONF_MODE, default=DEFAULT_MODE): vol.In({
                "modbus": "Modbus TCP (Ethernet / LAN)",
                "serial": "Modbus RTU (USB/RS485)",
            })
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_modbus(self, user_input=None):
        """Configure Modbus TCP."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            ok = await self.hass.async_add_executor_job(
                _test_tcp_connection, host, port
            )

            if ok:
                user_input[CONF_MODE] = "modbus"
                return self.async_create_entry(
                    title=f"Solarmodbus TCP ({host})",
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        })

        return self.async_show_form(
            step_id="modbus",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_serial(self, user_input=None):
        """Configure Modbus RTU over USB/RS485."""
        errors = {}

        if user_input is not None:
            user_input[CONF_MODE] = "serial"
            return self.async_create_entry(
                title=f"Solarmodbus Serial ({user_input[CONF_SERIAL_PORT]})",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT): str,
            vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        })

        return self.async_show_form(
            step_id="serial",
            data_schema=schema,
            errors=errors,
        )
