"""The Selective Scene integration."""

from __future__ import annotations
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .services import activate_scene


async def async_setup_entry(hass: HomeAssistant, _: ConfigEntry) -> bool:
    """Set up Selective Scene integration."""

    hass.services.async_register(
        DOMAIN,
        "turn_on",
        activate_scene,
        schema=vol.Schema(
            {
                vol.Required("entity_id"): cv.entity_ids,
                vol.Optional("entity_filter"): cv.entity_ids,
            }
        ),
    )

    return True
