"""The Selective Scene integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Selective Scene integration."""

    return True
