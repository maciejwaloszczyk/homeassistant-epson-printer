"""Sensor platform for Epson Printer integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, SENSOR_TYPES, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    host = config_entry.data[CONF_HOST]
    update_interval = config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    
    coordinator = EpsonPrinterDataUpdateCoordinator(
        hass, host, timedelta(seconds=update_interval)
    )

    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(EpsonPrinterSensor(coordinator, sensor_type, host))

    async_add_entities(entities)


class EpsonPrinterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Epson printer."""

    def __init__(self, hass: HomeAssistant, host: str, update_interval: timedelta) -> None:
        """Initialize."""
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            from epsonprinter_pkg import EpsonPrinterAPI
            
            def get_printer_data():
                api = EpsonPrinterAPI(self.host)
                api.update()
                
                data = {}
                for sensor_type in SENSOR_TYPES:
                    try:
                        value = api.getSensorValue(sensor_type)
                        # Convert to percentage if needed
                        if isinstance(value, (int, float)):
                            data[sensor_type] = value
                        else:
                            # Try to parse if it's a string
                            try:
                                data[sensor_type] = float(value)
                            except (ValueError, TypeError):
                                data[sensor_type] = None
                    except Exception as e:
                        _LOGGER.warning(f"Could not get {sensor_type} value: {e}")
                        data[sensor_type] = None
                
                return data
            
            return await self.hass.async_add_executor_job(get_printer_data)
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with printer: {err}") from err


class EpsonPrinterSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Epson Printer sensor."""

    def __init__(
        self,
        coordinator: EpsonPrinterDataUpdateCoordinator,
        sensor_type: str,
        host: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._host = host
        
        # Create English entity names
        entity_names = {
            "black": "black_ink",
            "magenta": "magenta_ink", 
            "cyan": "cyan_ink",
            "yellow": "yellow_ink",
            "clean": "cleaning_cartridge"
        }
        
        entity_name = entity_names.get(sensor_type, sensor_type)
        
        self._attr_name = f"Epson Printer {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"epson_printer_{host}_{entity_name}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_device_class = SENSOR_TYPES[sensor_type]["device_class"]

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": f"Epson Printer ({self._host})",
            "manufacturer": "Epson",
            "model": "Network Printer",
            "sw_version": "1.0",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._sensor_type)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None
