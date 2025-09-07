# Selective Scene

A Home Assistant custom integration that enables selective scene activation: apply scenes to only specific entities or areas instead of all entities in the scene.

This integration implements the functionality proposed in https://github.com/home-assistant/core/pull/132636.

## TODO

- [x] Add description
- [x] Support transitions
- [x] Support empty `entity_filter`
- [x] Support multiple scenes/targets
- [x] Support `area_filter` in addition to `entity_filter`
- [ ] Support `labels` in addition to `entity_filter`
- [ ] Resolve individual entities from entity groups when using filters. For example if scene state contains light group, "flatten" the group recursively to individual light entities
- [ ] Add tests
- [ ] Add docs
- [ ] Create logo and add to `home-assistant/brands` repo
- [ ] Configure GitHub releases, see [docs](https://www.hacs.xyz/docs/publish/integration/#github-releases-optional)
- [ ] Refactor to extend the existing `HomeAssistantScene` class?
