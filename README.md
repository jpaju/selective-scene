# Selective Scene

A Home Assistant custom integration that enables selective scene activation: apply scenes to only specific entities or areas instead of all entities in the scene.

## Motivation

Using built-in scenes with selective filtering provides several advantages:

- **Scene Editor Integration**: Create and modify scenes using Home Assistant's built-in scene editor UI
- **Avoid Scene Duplication**: Without filtering, you'd need separate scenes like `scene.evening_lights_all`, `scene.evening_lights_living_room`, `scene.evening_lights_kitchen`, etc. With selective scenes, one `scene.evening_lights` can serve multiple purposes
- **Dynamic Area-based Control**: Apply the same scene to different areas based on context (motion sensors, time of day, etc.)
- **Maintainability**: Update lighting states in one place while using them in multiple automations with different scopes

This allows you to store and manage lighting states in built-in scenes but use them more expressively in automations.

## Usage

This integration provides a drop-in replacement for the built-in `scene.turn_on` service with the ability to activate scenes selectively.
Instead of applying a scene to all entities, you can filter which entities are affected using entity IDs or areas.

### Service: `selective_scene.turn_on`

The service accepts the same parameters as `scene.turn_on` plus additional filtering options:

| Parameter       | Type        | Description                                                                              |
| --------------- | ----------- | ---------------------------------------------------------------------------------------- |
| `entity_id`     | string/list | Scene(s) to activate                                                                     |
| `transition`    | number      | Transition time in seconds                                                               |
| `entity_filter` | list        | List of entity IDs to apply the scene to (only these entities will be affected)          |
| `area_filter`   | list        | List of area names to apply the scene to (only entities in these areas will be affected) |

### Examples

**Apply scene only to specific entities:**

```yaml
action: selective_scene.turn_on
target:
  entity_id: scene.evening_lights
data:
  entity_filter:
    - light.living_room
    - light.kitchen
```

**Apply scene only to specific areas:**

```yaml
action: selective_scene.turn_on
target:
  entity_id: scene.evening_lights
data:
  area_filter:
    - living_room
    - kitchen
```

**Motion-activated lighting automation:**

```yaml
automation:
  - alias: "Motion activated lights"
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion_living_room
        to: "on"
    actions:
      - action: selective_scene.turn_on
        target:
          entity_id: scene.evening_lights
        data:
          area_filter:
            - living_room
```

## Installation

**Quick install** (skip to step 5)
<br>
[![Open Selective Scene on Home Assistant Community Store (HACS).](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jpaju&repository=selective-scene)

**Manual steps**

1. Open HACS in your Home Assistant instance
2. Click the three dots menu (⋮) and select "Custom repositories"
3. Add `https://github.com/jpaju/selective-scene` as repository with category `Integration`
4. Search and open "Selective Scene " from HACS repositories
5. Click "Download"
6. Restart Home Assistant
7. Go to Settings → Devices & Services → Integrations and click "Add Integration"
8. Search for "Selective Scene" and add it
