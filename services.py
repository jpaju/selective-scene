"""Service implementations for Selective Scene integration."""

from __future__ import annotations
from typing import cast

from homeassistant.components.homeassistant.scene import HomeAssistantScene
from homeassistant.helpers.entity_registry import (
    async_entries_for_area as async_entities_for_area,
    async_entries_for_device as async_entities_for_device,
    async_get as async_get_entity_registry,
)
from homeassistant.helpers.device_registry import (
    async_entries_for_area as async_device_entries_for_area,
    async_get as async_get_device_registry,
)
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
    area_filter = call.data.get("area_filter")
    transition = call.data.get("transition")

    if not scene_ids:
        return {"error": "No target/entity_id provided"}

    scene_states = _get_scene_states(platform, scene_ids)
    scene_states = _apply_area_filter(hass, scene_states, area_filter)
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


def _apply_area_filter(
    hass: HomeAssistant,
    scene_states: list[State],
    area_filter: list[str] | None,
) -> list[State]:
    """Remove states that are not in the area filter."""
    if not area_filter:
        return scene_states

    area_entity_ids = _resolve_area_entity_ids(hass, area_filter)
    return [state for state in scene_states if state.entity_id in area_entity_ids]


def _apply_entity_filter(
    scene_states: list[State],
    entity_filter: list[str] | None,
) -> list[State]:
    """Remove states that are not in the entity filter."""
    if not entity_filter:
        return scene_states

    return [state for state in scene_states if state.entity_id in entity_filter]


def _resolve_area_entity_ids(hass: HomeAssistant, area_ids: list[str]) -> set[str]:
    """Return a set of entity_ids for the given area_ids."""
    entity_registry = async_get_entity_registry(hass)
    device_registry = async_get_device_registry(hass)

    result: set[str] = set()

    for area_id in area_ids:
        # Get entities directly assigned to the area
        entities = async_entities_for_area(entity_registry, area_id)
        result.update(entity.entity_id for entity in entities)

        # Get entities belonging to devices assigned to the area
        devices = async_device_entries_for_area(device_registry, area_id)
        device_entities = [
            entity
            for device in devices
            for entity in async_entities_for_device(entity_registry, device.id)
        ]
        result.update(entity.entity_id for entity in device_entities)

    return result
