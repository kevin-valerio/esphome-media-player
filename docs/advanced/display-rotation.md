# Display Rotation

The ESP32-S3 4848S040 supports display rotation for different mounting orientations (for example to change which side the power cable exits from). Set `display_rotation`; LVGL rotates the display and touch input together.

## ESP32-S3 4848S040

The 480×480 square display supports all four rotations.

| `display_rotation` | Orientation |
| ------------------- | ----------- |
| `"0"` (default)     | Default panel orientation |
| `"90"`              | Rotated 90 degrees |
| `"180"`             | Rotated 180 degrees |
| `"270"`             | Rotated 270 degrees |

### Example: 90-degree rotation

```yaml
substitutions:
  name: "music-dashboard"
  friendly_name: "Music Dashboard"
  display_rotation: "90"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

packages:
  music_dashboard:
    url: https://github.com/jtenniswood/esphome-media-player
    files: [guition-esp32-s3-4848s040/packages.yaml]
    ref: main
    refresh: 1s
```

### Example: 270-degree rotation

```yaml
substitutions:
  name: "music-dashboard"
  friendly_name: "Music Dashboard"
  display_rotation: "270"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

packages:
  music_dashboard:
    url: https://github.com/jtenniswood/esphome-media-player
    files: [guition-esp32-s3-4848s040/packages.yaml]
    ref: main
    refresh: 1s
```
