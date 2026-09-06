from __future__ import annotations

import asyncio
import logging

import voluptuous as vol

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv

DOMAIN = "soco_remote"

_LOGGER = logging.getLogger(__name__)

VOLUME_STEP_PERCENT = 15

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(vol.DefaultTo(dict), vol.Schema({vol.Optional("line_in_host"): cv.string}))},
    extra=vol.ALLOW_EXTRA,
)


def _resolve_speaker_name(hass: HomeAssistant, entity_id: str) -> str | None:
    state = hass.states.get(entity_id)
    if state is None:
        _LOGGER.error("Entity not found: %s", entity_id)
        return None
    return state.name


def _get_sonos_hosts(config: dict) -> list[str]:
    sonos = config.get("sonos")
    if not isinstance(sonos, dict):
        return []

    media_player = sonos.get("media_player")
    if not isinstance(media_player, dict):
        return []

    hosts = media_player.get("hosts")
    if not isinstance(hosts, list):
        return []

    return [str(h) for h in hosts if h]


def _find_speaker(name: str, sonos_hosts: list[str]):
    from soco import SoCo
    from soco.discovery import by_name

    for host in sonos_hosts:
        try:
            seed = SoCo(host)
            if seed.player_name == name:
                return seed

            for zone in seed.all_zones:
                if zone.player_name == name:
                    return zone
        except Exception:
            continue

    return by_name(name)


def _soco_group_volume_step(name: str, sonos_hosts: list[str], step_percent: int) -> None:
    speaker = _find_speaker(name, sonos_hosts)
    if speaker is None:
        raise RuntimeError(f"Sonos speaker not found: {name}")

    coordinator = speaker.group.coordinator
    for member in coordinator.group.members:
        if getattr(member, "is_visible", True) is False:
            continue
        try:
            current = int(member.volume)
            new_volume = max(0, min(100, current + step_percent))
            member.volume = new_volume
        except Exception as exc:
            _LOGGER.warning("Failed to set volume for %s (%s): %s", member.player_name, member.ip_address, exc)


def _soco_next_track(name: str) -> None:
    from soco.discovery import by_name

    speaker = by_name(name)
    if speaker is None:
        raise RuntimeError(f"Sonos speaker not found by name: {name}")

    speaker.next()


def _soco_toggle_line_in(
    name: str, sonos_hosts: list[str], line_in_host: str, saved_sources: dict
) -> None:
    from soco import SoCo

    speaker = _find_speaker(name, sonos_hosts)
    if speaker is None:
        raise ServiceValidationError(f"Sonos speaker not found: {name}")

    coordinator = speaker.group.coordinator
    uid = coordinator.uid
    media = coordinator.avTransport.GetMediaInfo([("InstanceID", 0)])
    if media["CurrentURI"].startswith("x-rincon-stream:"):
        previous = saved_sources.get(uid)
        if previous and previous["uri"] and (
            not previous["uri"].startswith("x-rincon-queue:") or previous["track"] > 0
        ):
            if previous["uri"].startswith("x-rincon-queue:") and previous["uri"].endswith("#0"):
                coordinator.play_from_queue(previous["track"] - 1, start=False)
                if previous["position"] not in ("", "NOT_IMPLEMENTED"):
                    coordinator.seek(previous["position"])
            else:
                coordinator.play_uri(previous["uri"], previous["metadata"], start=False)
            coordinator.play()
        else:
            # Line-in may already be selected when Home Assistant starts.
            if not coordinator.get_queue(max_items=1):
                raise ServiceValidationError("No saved music or Sonos queue. Start music in Sonos first.")
            coordinator.play_from_queue(0)
        saved_sources.pop(uid, None)
        return

    track = coordinator.get_current_track_info()
    saved_sources[uid] = {
        "uri": media["CurrentURI"],
        "metadata": media["CurrentURIMetaData"],
        "track": int(track["playlist_position"] or 0),
        "position": track["position"],
    }
    coordinator.switch_to_line_in(source=SoCo(line_in_host))
    coordinator.play()


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    sonos_hosts = _get_sonos_hosts(config)
    line_in_host = config[DOMAIN].get("line_in_host")
    saved_sources: dict = {}
    input_lock = asyncio.Lock()

    async def toggle_line_in(call: ServiceCall) -> None:
        if not line_in_host:
            raise ServiceValidationError("Set soco_remote.line_in_host to the speaker with the vinyl input.")
        name = _resolve_speaker_name(hass, call.data[ATTR_ENTITY_ID])
        if name is None:
            raise ServiceValidationError(f"Entity not found: {call.data[ATTR_ENTITY_ID]}")
        async with input_lock:
            await hass.async_add_executor_job(
                _soco_toggle_line_in, name, sonos_hosts, line_in_host, saved_sources
            )

    async def volume_up(call: ServiceCall) -> None:
        entity_id = call.data.get(ATTR_ENTITY_ID)
        if not entity_id:
            _LOGGER.error("%s.%s: missing %s", DOMAIN, call.service, ATTR_ENTITY_ID)
            return

        name = _resolve_speaker_name(hass, entity_id)
        if name is None:
            return

        await hass.async_add_executor_job(_soco_group_volume_step, name, sonos_hosts, VOLUME_STEP_PERCENT)

    async def volume_down(call: ServiceCall) -> None:
        entity_id = call.data.get(ATTR_ENTITY_ID)
        if not entity_id:
            _LOGGER.error("%s.%s: missing %s", DOMAIN, call.service, ATTR_ENTITY_ID)
            return

        name = _resolve_speaker_name(hass, entity_id)
        if name is None:
            return

        await hass.async_add_executor_job(_soco_group_volume_step, name, sonos_hosts, -VOLUME_STEP_PERCENT)

    async def next_track(call: ServiceCall) -> None:
        entity_id = call.data.get(ATTR_ENTITY_ID)
        if not entity_id:
            _LOGGER.error("%s.%s: missing %s", DOMAIN, call.service, ATTR_ENTITY_ID)
            return

        name = _resolve_speaker_name(hass, entity_id)
        if name is None:
            return

        await hass.async_add_executor_job(_soco_next_track, name)

    hass.services.async_register(DOMAIN, "volume_up", volume_up)
    hass.services.async_register(DOMAIN, "volume_down", volume_down)
    hass.services.async_register(DOMAIN, "next_track", next_track)
    hass.services.async_register(
        DOMAIN, "toggle_line_in", toggle_line_in,
        schema=vol.Schema({vol.Required(ATTR_ENTITY_ID): cv.entity_id}),
    )

    _LOGGER.info(
        "Registered services: %s.volume_up, %s.volume_down, %s.next_track, %s.toggle_line_in",
        DOMAIN, DOMAIN, DOMAIN, DOMAIN,
    )
    return True
