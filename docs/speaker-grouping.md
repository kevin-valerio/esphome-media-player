# Speaker Grouping

Control multi-room speaker groups directly from the touchscreen panel. The settings panel (swipe down) shows a speaker list on the right side where you can add or remove speakers from the group and adjust individual volumes.

Speaker grouping requires speakers that support the `media_player.join` and `media_player.unjoin` services in Home Assistant.

## How it works

- The panel auto-discovers all speakers from the configured integration in your Home Assistant instance
- The currently selected speaker is shown first
- The main volume adjusts all grouped speakers proportionally, keeping their relative balance
- Per-speaker `−` / `+` buttons let you fine-tune individual volumes within the group
- The toggle states update automatically when the group changes

## Compatibility

This feature relies on Home Assistant's `media_player.join` and `media_player.unjoin` services. These are only available on speaker platforms that support grouping. If your speakers don't support these services, the grouping controls will not work.


| Platform             | Supported | Integration name     |
| -------------------- | --------- | -------------------- |
| Bang & Olufsen       | Yes       | `bang_olufsen`       |
| Bluesound            | Yes       | `bluesound`          |
| Google Cast          | Yes       | `cast`               |
| Heos                 | Yes       | `heos`               |
| LinkPlay             | Yes       | `linkplay`           |
| Sonos                | Yes       | `sonos`              |
| Yamaha               | Yes       | `yamaha_musiccast`   |


## Setup

One template sensor helper needs to be created in Home Assistant. This is done entirely through the UI — no YAML editing required. 

### Create the Speaker Group sensor

1. Go to **Settings → Devices & Services → Helpers** tab
2. Click **+ Create Helper** → **Template** → **Template a sensor**
3. Set the **Name** to `Speaker Group`
4. Paste into the **State template** field

```
{%- set s = integration_entities("sonos") | select("match", "media_player") | list -%}
{{ s | map("replace", "media_player.", "") | join(",") }}|{{ s | map("state_attr", "friendly_name") | join(",") }}|{{ s | map("state_attr", "volume_level") | join(",") }}
```

::: info
If you're using a different platform, replace `"sonos"` with your integration name from the table above.
:::

5. Leave all other fields as default and click **Submit**.

### Verify

Go to **Developer Tools → States** and search for `sensor.speaker_group`. It should show a pipe-delimited string containing short entity IDs (without the `media_player.` prefix), friendly names, and volume levels, e.g.:

```
office,kitchen|Office,Kitchen|0.45,0.6
```

The device subscribes to this sensor automatically at boot. If the speaker page is empty, reboot the screen to see the update.

## Behavior

- The speaker list appears in the settings panel (swipe down) when there are at least two speakers from the configured integration
