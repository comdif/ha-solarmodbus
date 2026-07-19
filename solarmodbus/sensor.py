from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, COORDINATOR_NAME


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data[COORDINATOR_NAME]
    definition = data["definition"]

    entities = []

    for group in definition.get("parameters", []):
        for item in group.get("items", []):

            key = item["name"]

            is_text = (
                item.get("class") not in ("energy", "power", "voltage", "current")
                and not item.get("state_class")
                and not item.get("uom")
            )

            entities.append(
                SolarmodbusSensor(
                    coordinator=coordinator,
                    yaml=item,
                    is_text=is_text,
                )
            )

    async_add_entities(entities)


class SolarmodbusSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, yaml, is_text):
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.yaml = yaml
        self.is_text = is_text

        name = yaml["name"]

        self._attr_name = name

        if coordinator.mode == "solarman":
            self._attr_unique_id = (
                f"{coordinator.config_entry.entry_id}_{name}"
            )
        else:
            self._attr_unique_id = f"{DOMAIN}_{name}"

        if self.is_text:
            self._attr_device_class = None
            self._attr_state_class = None
            self._attr_native_unit_of_measurement = None

        else:
            self._attr_device_class = yaml.get("class")
            self._attr_state_class = yaml.get("state_class")
            self._attr_native_unit_of_measurement = (
                yaml.get("uom") or yaml.get("unit")
            )

        self._attr_icon = yaml.get("icon")

        if yaml.get("category") == "diagnostic":
            from homeassistant.const import EntityCategory
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "solarmodbus_device")},
            name="Solarmodbus Device",
            manufacturer="Solarmodbus",
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self.yaml["name"])
