# Development

## TODO

- [x] Add description
- [x] Add docs
- [ ] Add tests
- [ ] Create logo and add to `home-assistant/brands` repo
- [ ] Configure GitHub releases, see [docs](https://www.hacs.xyz/docs/publish/integration/#github-releases-optional)
- [x] Support transitions
- [x] Support empty `entity_filter`
- [x] Support multiple scenes/targets
- [x] Support `area_filter` in addition to `entity_filter`
- [ ] Support `labels` in addition to `entity_filter`
- [ ] Resolve individual entities from entity groups when using filters. For example if scene state contains light group, "flatten" the group recursively to individual light entities
- [ ] Refactor to extend the existing `HomeAssistantScene` class?
