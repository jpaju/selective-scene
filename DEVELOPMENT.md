# Development

## Requirements

- nix
- direnv
- uv (included in flake.nix dev shell)

## Setup

1. **Create venv**: Create virtual environment

   ```bash
   uv venv
   ```

2. **Install deps**: Sync project dependencies

   ```bash
   uv sync
   ```

3. **Allow direnv**: Enable automatic activation (first time only)
   ```bash
   direnv allow
   ```

Direnv activates virtual environment automatically when entering the project directory.

## TODO

- [x] Add description
- [x] Add docs
- [x] Add CI
- [x] Add license
- [ ] Add tests
  - [Tutorial](https://aarongodfrey.dev/home%20automation/building_a_home_assistant_custom_component_part_2/)
- [x] Create logo and add to `home-assistant/brands` repo
- [x] Configure GitHub releases, see [docs](https://www.hacs.xyz/docs/publish/integration/#github-releases-optional)
- [x] Support transitions
- [x] Support empty `entity_filter`
- [x] Support multiple scenes/targets
- [x] Support `area_filter` in addition to `entity_filter`
- [ ] Support `labels` in addition to `entity_filter`
- [ ] Refactor to extend the existing `HomeAssistantScene` class?
