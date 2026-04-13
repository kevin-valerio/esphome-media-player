# ESPHome Media Controller for Home Assistant

A touchscreen media controller that shows full-screen album art and lets you control media from any Home Assistant media player. Supports the **4"** panel. Built with [ESPHome](https://esphome.io/) and [LVGL](https://lvgl.io/); tested with Google and Sonos speakers.

![guition-esp32-s3-4848s040](docs/images/guition-esp32-s3-4848s040-example1.jpg)

---

## Features

- **Album art** — Full-screen cover art from Home Assistant, with smooth transitions between tracks
- **Accent color** — Dominant color extracted from album art, applied to the UI and exposed as an HA light entity
- **Now playing** — 4" shows cover-only UI; if artwork is unavailable, it shows the track title
- **Touch controls** — 4": volume down, volume up, next track buttons (over the cover art)
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
