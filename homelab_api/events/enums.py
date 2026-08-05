from enum import StrEnum


class EventName(StrEnum):
    GAMING_MODE_ON = 'gaming_mode_on'
    GAMING_MODE_OFF = 'gaming_mode_off'
    ALEXA_HELLO_WORLD = 'alexa_hello_world'
    DOTA_KILL = 'dota_hero_kill'
    DOTA_DEATH = 'dota_hero_death'
