"""Service implementations for Selective Scene integration."""

from __future__ import annotations
from collections.abc import Iterable
from typing import cast

from homeassistant.components.homeassistant.scene import HomeAssistantScene
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.helpers.state import async_reproduce_state
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    State,
)

from .const import DATA_PLATFORM


async def activate_scene(call: ServiceCall) -> ServiceResponse:
    """Activate one or more scenes."""
    hass: HomeAssistant = call.hass
    platform: EntityPlatform = hass.data[DATA_PLATFORM]

    scene_ids = call.data.get("entity_id")
    entity_filter = call.data.get("entity_filter")
    transition = call.data.get("transition")

    if not scene_ids:
        return {"error": "No target/entity_id provided"}

    scene_states = _get_scene_states(platform, scene_ids)
    scene_states = _apply_entity_filter(scene_states, entity_filter)

    reproduce_options = {"transition": transition} if transition is not None else {}

    await async_reproduce_state(
        hass,
        scene_states,
        context=call.context,
        reproduce_options=reproduce_options,
    )


def _get_scene_states(
    platform: EntityPlatform,
    scene_ids: list[str],
) -> list[State]:
    """Collect all states from the given scenes ids."""
    all_states: list[State] = []

    for scene_id in scene_ids:
        scene = cast(HomeAssistantScene | None, platform.entities.get(scene_id))
        if not scene:
            continue

        scene_states = scene.scene_config.states.values()
        all_states.extend(scene_states)

    return all_states


def _apply_entity_filter(
    scene_states: list[State],
    entity_filter: list[str] | None = None,
) -> list[State]:
    """Remove states that are not in the entity filter."""
    return (
        [state for state in scene_states if state.entity_id in entity_filter]
        if entity_filter
        else scene_states
    )
