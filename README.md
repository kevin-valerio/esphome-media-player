# ESPHome Media Controller for Home Assistant

A touchscreen media controller that shows full-screen album art and lets you control media from any Home Assistant media player. Supports the **4"** panel. Built with [ESPHome](https://esphome.io/) and [LVGL](https://lvgl.io/); tested with Google and Sonos speakers.

![guition-esp32-s3-4848s040](docs/images/guition-esp32-s3-4848s040-example1.jpg)

---

## Features

- **Album art** — Full-screen cover art from Home Assistant, with smooth transitions between tracks
- **Accent color** — Dominant color extracted from album art, applied to the UI and exposed as an HA light entity
- **Now playing** — 4" shows cover-only UI; if artwork is unavailable, it shows the track title
- **Touch controls** — 4": next track button (bottom of the screen)
- **Linked media player** — Automatically shows now-playing from a linked media player when the speaker switches to a TV or Line-in input
- **Screensaver** — Day/night aware dimming and screen-off when paused
- **Configurable from Home Assistant** — Media player, brightness, timeouts, track info duration; no reflashing

*Full details: [Features](https://jtenniswood.github.io/esphome-media-player/features)*


---

## Supported Screens

| Device | Size | Buy |
|--------|------|-----|
| [Guition ESP32-S3 4848S040](https://jtenniswood.github.io/esphome-media-player/devices/esp32-s3-4848s040) | 4" (480×480) | [AliExpress](https://s.click.aliexpress.com/e/_c3sIhvBv) |

---

## Support This Project

If you find this project useful, consider buying me a coffee to support ongoing development!

<a href="https://www.buymeacoffee.com/jtenniswood">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50" />
</a>

---

## Getting Started

The [documentation site](https://jtenniswood.github.io/esphome-media-player/) has the install guide, configurable settings, manual setup (ESPHome dashboard), and troubleshooting.

<a href="https://jtenniswood.github.io/esphome-media-player/">
  <img src="https://img.shields.io/badge/Open_Documentation_%26_Installer-blue?style=for-the-badge&logo=esphome&logoColor=white" alt="Open Documentation & Installer" />
</a>

---

## Optional: SoCo helper (Sonos)

This repo includes a tiny Home Assistant custom integration at `homeassistant/custom_components/soco_remote` that exposes these services:

- `soco_remote.volume_up`
- `soco_remote.volume_down`
- `soco_remote.next_track`

`volume_up` / `volume_down` adjust the volume of all **visible members** of the target Sonos group by **15%** per click.

Install it by copying `homeassistant/custom_components/soco_remote` into your Home Assistant config folder at `/config/custom_components/soco_remote`, add `soco_remote:` to `configuration.yaml`, then restart Home Assistant.

Note: the upstream firmware auto-updater overwrites custom firmware. In this fork it’s disabled for the 4" build (see `guition-esp32-s3-4848s040/packages.yaml`). Update the device using `esphome upload ...` (OTA) instead.

Note: the current ESP32 UI in this fork has no volume buttons (volume +/- was unreliable), so this SoCo helper is optional and not used by the device UI.

If you still want to use the SoCo-based approach, add 2 scripts to your Home Assistant `scripts.yaml` (replace `f6bc10` with your device suffix):

```yaml
sonos_volume_up_all:
  alias: "Sonos volume up (all speakers)"
  mode: single
  sequence:
    - service: soco_remote.volume_up
      data:
        entity_id: "{{ states('text.media_player_f6bc10_media_player') }}"

sonos_volume_down_all:
  alias: "Sonos volume down (all speakers)"
  mode: single
  sequence:
    - service: soco_remote.volume_down
      data:
        entity_id: "{{ states('text.media_player_f6bc10_media_player') }}"
```

---

## Work log (this fork)

This repo is a customized fork (based on `jtenniswood/esphome-media-player`) for a Guition ESP32‑S3 4848S040 (4") panel + Sonos.

### UI changes (ESP32)

The now-playing screen was simplified to only show:

- Full-screen album art
- 1 button at the bottom: **next track**

Behavior:

- Buttons are slightly bigger and flash **orange** on press.
- If album art is missing or can’t load (common with local MP3), the screen shows the **track title** instead of an empty cover.

Main files:

- `guition-esp32-s3-4848s040/device/lvgl.yaml`
- `shared/device/sensors.yaml`
- `shared/device/media_player_select.yaml`
- `shared/addon/music.yaml`

### Sonos group volume (Home Assistant + SoCo)

Problem:

- The volume slider in the original firmware worked for a single speaker, but we could not get reliable volume +/- buttons on the minimal UI.

Current status:

- Volume +/- buttons were removed from the minimal UI.

SoCo (still included, optional):

- There is also an optional Home Assistant custom integration: `homeassistant/custom_components/soco_remote`
- It uses the Python library `SoCo` to apply **±15%** volume to **all visible group members** of the target speaker.

### Preventing “reverting” to upstream firmware

What happened:

- The upstream project includes an OTA updater that installs firmware from `jtenniswood/esphome-media-player`.
- When enabled, it can overwrite this fork’s custom firmware and make the device look like “original firmware”.

What we changed:

- Disabled the upstream firmware updater for the 4" build by removing it from `guition-esp32-s3-4848s040/packages.yaml`.
- Switched the `online_image` component and placeholder image to use **local files** (so we don’t pull UI/assets from upstream at build time):
  - `shared/addon/music.yaml`

### Local deploy notes (this workspace)

- ESPHome build file: `builds/guition-esp32-s3-4848s040.yaml`
- OTA target (device IP): `192.168.178.37`
- Upload command:

```bash
esphome upload builds/guition-esp32-s3-4848s040.yaml --device 192.168.178.37
```

### Home Assistant Docker notes (this machine)

- Container: `homeassistant` (`ghcr.io/home-assistant/homeassistant:stable`)
- Config bind mount: `/Users/kevinvalerio/homeassistant` → `/config`
- Sonos integration uses static speaker IPs (Docker on macOS can break Sonos discovery):
  - `/Users/kevinvalerio/homeassistant/configuration.yaml`

## Feedback

If you have any feedback or suggestions, please open an [issue](https://github.com/jtenniswood/esphome-media-player/issues).

---

## Gallery

### Guition ESP32-S3 4848S040 (4")

![Guition ESP32-S3 example 1](docs/images/guition-esp32-s3-4848s040-example1.jpg)
![Guition ESP32-S3 example 2](docs/images/guition-esp32-s3-4848s040-example2.jpg)
![Guition ESP32-S3 example 3](docs/images/guition-esp32-s3-4848s040-example3.jpg)
![Guition ESP32-S3 example 4](docs/images/guition-esp32-s3-4848s040-example4.jpg)
![Guition ESP32-S3 volume controls](docs/images/guition-esp32-s3-4848s040-volume.jpg)

More screenshots in the [documentation](https://jtenniswood.github.io/esphome-media-player/).
