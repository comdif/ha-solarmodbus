import logging
_LOGGER = logging.getLogger(__name__)

class ModbusValueParser:
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

        rule = item.get("rule", 1)
        customrule = item.get("customrule", None)

        if rule == 1:
            val = values[0]
        elif rule == 2:
            val = self._to_signed_16(values[0])
        elif rule == 3:
            val = 0
            for v in values:
                val = (val << 16) | v
        elif rule == 4:
            if len(values) < 2:
                raise ValueError("Rule 4 requires 2 registers")
            val = (values[1] << 16) | values[0]
        elif rule == 5:
            chars = []
            for v in values:
                chars.append((v >> 8) & 0xFF)
                chars.append(v & 0xFF)
            val = bytes(chars).decode(errors="ignore").strip("\x00").strip()
        elif rule == 6:
            mask = item.get("mask", 1)
            val = values[0] & mask
        elif rule == 9:
            raw = values[0]
            hours = (raw >> 8) & 0xFF
            minutes = raw & 0xFF
            val = f"{hours:02d}:{minutes:02d}"
        else:
            val = values[0]

        if customrule:
            val = self.apply_customrule(val, customrule)

        if "offset" in item:
            try:
                val = val - item["offset"]
            except Exception:
                _LOGGER.debug("Offset not applicable on %s", item.get("name"))

        if item.get("isstr") and "lookup" in item:
            for entry in item["lookup"]:
                if entry["key"] == val:
                    val = entry["value"]
                    break

        if item.get("class") == "enum" and "lookup" in item:
            original_val = val
            matched = False
            for entry in item["lookup"]:
                if "key" in entry and entry["key"] == original_val:
                    val = entry["value"]
                    matched = True
                    break
            if not matched:
                for entry in item["lookup"]:
                    if "bit" in entry:
                        bit = entry["bit"]
                        if original_val & (1 << bit):
                            val = entry["value"]
                            matched = True
                            break
            if not matched:
                for entry in item["lookup"]:
                    if entry.get("key") == "default":
                        val = entry["value"]
                        break

        scale = item.get("scale", 1)
        try:
            val = val * scale
        except Exception:
            _LOGGER.debug("Scale not applicable on %s", item.get("name"))

        if item.get("isstr"):
            val = str(val)

        return val

    def parse_all(self, raw_registers: dict) -> dict:
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
