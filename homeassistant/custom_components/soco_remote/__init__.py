from __future__ import annotations

import logging

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall

DOMAIN = "soco_remote"

_LOGGER = logging.getLogger(__name__)

VOLUME_STEP_PERCENT = 15


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


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    sonos_hosts = _get_sonos_hosts(config)

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

    _LOGGER.info("Registered services: %s.volume_up, %s.volume_down, %s.next_track", DOMAIN, DOMAIN, DOMAIN)
    return True
