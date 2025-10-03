# AGENTS.md - Development Guidelines

## Project Type

Home Assistant custom integration (Python) for selective scene activation.

## Build/Test Commands

- **Validation**: Use GitHub Actions CI (HACS validation + hassfest)
- **HACS Validation**: `hacs/action@main` with category `integration`
- **Hassfest Validation**: `home-assistant/actions/hassfest@master`
- **No local test runner**: Integration testing happens via Home Assistant dev environment

## Code Style Guidelines

### Imports

- Use `from __future__ import annotations` first
- Standard library imports, then third-party, then Home Assistant imports
- Use specific imports: `from homeassistant.core import HomeAssistant`

### Formatting & Types

- Type hints required: `async def func(hass: HomeAssistant, call: ServiceCall) -> ServiceResponse`
- Use `|` union syntax: `list[str] | None`
- Private functions prefix with `_`: `def _apply_entity_filter()`

### Naming Conventions

- Snake_case for functions/variables: `activate_scene`, `entity_filter`
- PascalCase for classes: `SelectiveSceneConfigFlow`
- Constants in UPPER_CASE: `DOMAIN`, `DATA_PLATFORM`

### Error Handling

- Return dict with error key: `return {"error": "No target/entity_id provided"}`
- Use LOGGER from const.py for logging
