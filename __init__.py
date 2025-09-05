"""The Selective Scene integration."""

from __future__ import annotations
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)

from .const import DOMAIN, LOGGER


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Selective Scene integration."""

    async def dummy_service(call: ServiceCall) -> ServiceResponse:
        """A dummy service that returns test data."""
        LOGGER.info("Dummy service called with data: %s", call.data)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Dummy service called at {current_time}"
        return {"message": message, "timestamp": current_time}

    hass.services.async_register(
        DOMAIN,
        "dummy_service",
        dummy_service,
        supports_response=SupportsResponse.ONLY,
    )

    return True
