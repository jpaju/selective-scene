"""Tests for Selective Scene services."""

from collections.abc import Iterator
from contextlib import nullcontext
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import Context, HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.selective_scene.const import DOMAIN


async def test_turn_on_updates_scene_activation_timestamp(hass: HomeAssistant) -> None:
    """Test turning on a scene records its activation timestamp."""
    # Given a scene that has never been activated
    scene_state = hass.states.get("scene.test")
    assert scene_state is not None
    assert scene_state.state == STATE_UNKNOWN

    now = dt_util.utcnow()

    # When the scene is activated with selective_scene
    await _call_selective_scene_turn_on(hass, activation_time=now)

    # Then the scene state contains the activation timestamp
    scene_state = hass.states.get("scene.test")
    assert scene_state is not None
    assert scene_state.state == now.isoformat()


async def _call_selective_scene_turn_on(
    hass: HomeAssistant,
    *,
    context: Context | None = None,
    activation_time: datetime | None = None,
) -> None:
    time_patch = (
        patch("homeassistant.core.dt_util.utcnow", return_value=activation_time)
        if activation_time is not None
        else nullcontext()
    )
    with time_patch:
        await hass.services.async_call(
            DOMAIN,
            "turn_on",
            {"entity_id": ["scene.test"]},
            blocking=True,
            context=context,
        )


@pytest.fixture(autouse=True)
def mock_scene_state_reproduction() -> Iterator[None]:
    with patch(
        "custom_components.selective_scene.services.async_reproduce_state",
        new_callable=AsyncMock,
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_integration(
    hass: HomeAssistant, enable_custom_integrations: None
) -> None:
    """Set up Selective Scene with a test scene."""
    assert await async_setup_component(
        hass,
        "scene",
        {
            "scene": [
                {
                    "name": "test",
                    "entities": {"light.test": "on"},
                }
            ]
        },
    )
    await hass.async_block_till_done()

    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
