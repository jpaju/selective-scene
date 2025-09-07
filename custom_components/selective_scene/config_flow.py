"""Config flow for Selective Scene integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.core import HomeAssistant

from .const import DOMAIN


class SelectiveSceneConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Selective Scene."""

    VERSION = 1  # Config schema version, different from integration version

    async def async_step_user(self, user_input=None):
        """Handle flow initiated by the user."""
        if user_input is not None:
            return self.async_create_entry(title="Selective Scene", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
