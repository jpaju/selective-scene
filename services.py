"""Service implementations for Selective Scene integration."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.state import async_reproduce_state
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
)

from .const import DATA_PLATFORM


async def activate_scene(call: ServiceCall) -> ServiceResponse:
    """Activate one or more scenes."""
    hass: HomeAssistant = call.hass
    platform: EntityPlatform = hass.data[DATA_PLATFORM]

    targets = call.data.get("entity_id")
    entity_filter = call.data.get("entity_filter")
    transition = call.data.get("transition")

    if not targets:
        return {"error": "No target/entity_id provided"}

    scene_states = _collect_scene_states(platform, targets, entity_filter)

    reproduce_options = {"transition": transition} if transition is not None else {}

    await async_reproduce_state(
        hass,
        scene_states,
        context=call.context,
        reproduce_options=reproduce_options,
    )


def _collect_scene_states(
    platform: EntityPlatform,
    entity_ids: Iterable[str],
    entity_filter: list[str] | None = None,
) -> list[Any]:
    """Collect all states from the given scenes, while applying filters."""
    all_states: list[Any] = []

    for entity_id in entity_ids:
        scene_data = platform.entities.get(entity_id)
        if not scene_data:
            continue

        scene_states = list(scene_data.scene_config.states.values())
        if entity_filter:
            scene_states = [
                state for state in scene_states if state.entity_id in entity_filter
            ]
        all_states.extend(scene_states)

    return all_states
