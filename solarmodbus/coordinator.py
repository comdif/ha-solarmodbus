from __future__ import annotations
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pysolarmanv5 import PySolarmanV5

from .const import DEFAULT_TIMEOUT
from .parser_modbus import ModbusValueParser

LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=2)


class SolarmodbusCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        mode: str,
        host: str | None,
        port: int | None,
        serial_port: str | None,
        slave_id: int,
        definition: dict,
    ):
        super().__init__(
            hass,
            logger=LOGGER,
            name="Solarmodbus Coordinator",
            update_interval=SCAN_INTERVAL,
        )

        self.mode = mode
        self.host = host
        self.port = port or 8899
        self.serial_port = serial_port
        self.slave_id = int(slave_id)
        self.definition = definition

        self.parser = ModbusValueParser(definition)
        self.requests = self._extract_register_blocks(definition)

        if self.mode == "modbus":
            self._client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=DEFAULT_TIMEOUT,
            )

        elif self.mode == "serial":
            self._client = ModbusSerialClient(
                port=self.serial_port,
                baudrate=9600,
                parity="N",
                stopbits=1,
                bytesize=8,
                timeout=DEFAULT_TIMEOUT,
            )

        elif self.mode == "solarman":
            self._client = PySolarmanV5(
                self.host,
                self.slave_id,
                port=self.port,
                mb_slave_id=1,
                socket_timeout=60,
                v5_error_correction=False
            )

    # ---------------------------------------------------------
    # WRITE REGISTER — MODBUS / SERIAL / SOLARMAN V5
    # ---------------------------------------------------------
    def write_register(self, address, value):
        # SOLARMAN V5 → FC16 (write multiple)
        if self.mode == "solarman":
            return self._client.write_multiple_holding_registers(
                register_addr=address,
                values=[value],
            )

        # MODBUS / SERIAL → version stable, inchangée
        try:
            self._client.close()
        except Exception:
            pass

        if not self._client.connect():
            raise Exception("Unable to connect for write")

        rr = self._client.write_registers(address, [value])

        self._client.close()
        return rr

    def _extract_register_blocks(self, definition: dict):
        blocks = []

        for group in definition.get("parameters", []):
            for item in group.get("items", []):
                reg = item.get("register")
                regs = item.get("registers")

                if isinstance(reg, int):
                    blocks.append((reg, reg))
                elif isinstance(regs, list) and len(regs) > 0:
                    blocks.append((min(regs), max(regs)))

        blocks = list(set(blocks))
        blocks.sort(key=lambda x: x[0])
        return blocks

    def _read_block_modbus(self, client, start: int, end: int):
        values = {}

        try:
            for addr in range(start, end + 1):
                resp = client.read_holding_registers(addr)

                if resp.isError():
                    continue

                if not hasattr(resp, "registers") or not resp.registers:
                    continue

                values[addr] = resp.registers[0]

            return values

        except Exception as e:
            LOGGER.error(f"[Solarmodbus] Exception reading block {start}-{end}: {e}")
            return None

    def _read_block_solarman(self, start: int, end: int):
        count = end - start + 1
        try:
            regs = self._client.read_holding_registers(start, count)
            return {start + i: regs[i] for i in range(count)}
        except Exception as e:
            LOGGER.error(f"[Solarman] Error reading {start}-{end}: {e}")
            return None

    async def _async_update_data(self):
        merged = {}

        if self.mode in ("modbus", "serial"):
            client = self._client

            try:
                client.close()
            except Exception:
                pass

            if not client.connect():
                LOGGER.error("[Solarmodbus] Unable to connect to Modbus device")
                return {}

            try:
                for start, end in self.requests:
                    block = await self.hass.async_add_executor_job(
                        self._read_block_modbus, client, start, end
                    )
                    if block:
                        merged.update(block)
            finally:
                client.close()

        elif self.mode == "solarman":
            for start, end in self.requests:
                block = self._read_block_solarman(start, end)
                if block:
                    merged.update(block)

        if not merged:
            LOGGER.error("[Solarmodbus] No registers read")
            return {}

        return self.parser.parse_all(merged)
