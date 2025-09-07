"""Service implementations for Selective Scene integration."""

from __future__ import annotations

from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.state import async_reproduce_state
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
)

from .const import LOGGER, DATA_PLATFORM


async def activate_scene(call: ServiceCall) -> ServiceResponse:
    """Activate a scene."""
    hass: HomeAssistant = call.hass
    platform: EntityPlatform = hass.data[DATA_PLATFORM]

    entity_ids = call.data.get("entity_id")
    entity_filter = call.data.get("entity_filter", [])
    transition = call.data.get("transition")

    entity_id = entity_ids[0]
    LOGGER.warning("entity_ids: %s", entity_ids)
    if not entity_ids:
        return {"error": "No entity_id provided"}

    scene_data = platform.entities.get(entity_id)
    scene_states = scene_data.scene_config.states.values()
    LOGGER.warning("scene_data: %s", scene_data)
    LOGGER.warning("scene_states: %s", scene_states)

    scene_states_filtered = [
        state for state in scene_states if state.entity_id in entity_filter
    ]
    LOGGER.warning("scene_states_filtered: %s", scene_states_filtered)

    reproduce_options = {"transition": transition} if transition is not None else {}

    await async_reproduce_state(
        hass,
        scene_states_filtered,
        context=call.context,
        reproduce_options=reproduce_options,
    )
