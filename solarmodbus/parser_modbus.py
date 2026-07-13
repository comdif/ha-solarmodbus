import logging
_LOGGER = logging.getLogger(__name__)

class ModbusValueParser:
    """
    Modbus parser compatible with Deye/Solarman YAML rules.
    Handles:
    - uint16
    - int16
    - uint32 (big/little endian)
    - Deye rule-3 inconsistency
    - strings
    - bitmask
    - time-of-use HH:MM
    - offsets
    - lookups
    - scaling
    - customrule (hhmm)
    """

    def __init__(self, definition: dict):
        self.definition = definition

    def _to_signed_16(self, v: int) -> int:
        return v - 65536 if v > 32767 else v

    def apply_customrule(self, value, rule):
        if rule == "hhmm":
            try:
                value = int(value)
                hh = value // 100
                mm = value % 100
                return f"{hh:02d}:{mm:02d}"
            except Exception:
                return value

        return value

    def parse_item(self, item: dict, raw_registers: dict):
        """Parse a single YAML-defined item."""

        # 1) Resolve register list
        regs = item.get("registers")
        if regs is None:
            reg = item.get("register")
            if isinstance(reg, int):
                regs = [reg]
            else:
                regs = reg or []

        values = []
        for r in regs:
            if r not in raw_registers:
                raise KeyError(f"Register {hex(r)} not found in raw_registers")
            values.append(raw_registers[r])

        # 2) Apply rule
        rule = item.get("rule", 1)
        customrule = item.get("customrule", None)

        if rule == 1:
            # uint16
            val = values[0]

        elif rule == 2:
            # int16 signed
            val = self._to_signed_16(values[0])

        elif rule == 3:
            # Deye inconsistency: some rule-3 fields are big-endian, others little-endian
            if len(values) == 1:
                val = values[0]

            elif len(values) == 2:
                first_reg = regs[0]

                # If register >= 0x0060 → big endian (Total Production)
                # Else → little endian (Battery Charge/Discharge)
                if first_reg >= 0x0060:
                    val = (values[0] << 16) | values[1]
                else:
                    val = (values[1] << 16) | values[0]

            else:
                raise ValueError("Rule 3 supports 1 or 2 registers")

        elif rule == 4:
            # uint32 little endian
            if len(values) < 2:
                raise ValueError("Rule 4 requires 2 registers")
            val = (values[1] << 16) | values[0]

        elif rule == 5:
            # string (2 chars per register)
            chars = []
            for v in values:
                chars.append((v >> 8) & 0xFF)
                chars.append(v & 0xFF)
            val = bytes(chars).decode(errors="ignore").strip("\x00").strip()

        elif rule == 6:
            # bitmask
            mask = item.get("mask", 1)
            val = values[0] & mask

        elif rule == 9:
            # time-of-use (HH:MM encoded in one register)
            raw = values[0]
            hours = (raw >> 8) & 0xFF
            minutes = raw & 0xFF
            val = f"{hours:02d}:{minutes:02d}"

        else:
            # fallback: first raw register
            val = values[0]

        # 3) Apply custom rule (hhmm, etc.)
        if customrule:
            val = self.apply_customrule(val, customrule)

        # 4) Optional offset
        if "offset" in item:
            try:
                val = val - item["offset"]
            except Exception:
                _LOGGER.debug("Offset not applicable on %s", item.get("name"))

        # 5) Optional lookup (numeric -> text)
        if item.get("isstr") and "lookup" in item:
            for entry in item["lookup"]:
                if entry["key"] == val:
                    val = entry["value"]
                    break

        # 6) Scale
        scale = item.get("scale", 1)
        try:
            val = val * scale
        except Exception:
            _LOGGER.debug("Scale not applicable on %s", item.get("name"))

        return val

    def parse_all(self, raw_registers: dict) -> dict:
        """Parse all items defined in the YAML."""
        results = {}

        for group in self.definition.get("parameters", []):
            for item in group.get("items", []):
                name = item["name"]
                try:
                    results[name] = self.parse_item(item, raw_registers)
                except Exception as e:
                    _LOGGER.debug("Error parsing %s: %s", name, e)
                    results[name] = None

        return results
