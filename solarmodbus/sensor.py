import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import EntityCategory

from .const import DOMAIN, COORDINATOR_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Solarmodbus sensors from YAML definition."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data[COORDINATOR_NAME]
    definition = data["definition"]

    entities = []

    for group in definition.get("parameters", []):
        group_name = group.get("group", "unknown")

        for item in group.get("items", []):
            entities.append(
                SolarmodbusSensor(
                    coordinator=coordinator,
                    description=item,
                    group=group_name,
                    entry_id=entry.entry_id,
                )
            )

    async_add_entities(entities)
    _LOGGER.info("Solarmodbus: %s sensors loaded", len(entities))


class SolarmodbusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor defined in the YAML file."""

    def __init__(self, coordinator, description, group, entry_id):
        super().__init__(coordinator)

        self._desc = description
        self._group = group
        self._entry_id = entry_id

        name = description["name"]

        # Unique ID
        self._attr_unique_id = f"solarmodbus_{entry_id}_{name.replace(' ', '_')}"
        self._attr_name = name

        # Unit of measurement
        self._attr_native_unit_of_measurement = (
            description.get("uom") or description.get("unit")
        )

        # Device class
        if description.get("class"):
            self._attr_device_class = description["class"]

        # State class
        if description.get("state_class"):
            self._attr_state_class = description["state_class"]

        # Icon
        self._attr_icon = description.get("icon")

        # Category (diagnostic, config…)
        if description.get("category") == "diagnostic":
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the parsed value from the coordinator."""
        val = self.coordinator.data.get(self._desc["name"])
        return val if val is not None else None

    @property
    def available(self):
        """Entity availability based on coordinator success."""
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        """Return device information for grouping sensors."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Solarmodbus Device",
            "manufacturer": "Modbus",
            "model": "Generic Modbus Device",
        }
