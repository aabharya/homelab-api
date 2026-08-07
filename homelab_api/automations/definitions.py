from homelab_api import devices
from homelab_api.configs import settings
from homelab_api.devices.base import Device
from homelab_api.events.bus import event_handler
from homelab_api.events.enums import EventName
from homelab_api.loggings import get_logger

from . import services
from .protocols import AutomationResult, BaseAutomation

logger = get_logger('automations')


@event_handler(EventName.GAMING_MODE_ON)
class GamingModeEnableAutomation(BaseAutomation):
    mikrotik = Device(devices.mikrotik_device)
    pixoo = Device(devices.pixoo_device)
    tapo_lamp = Device(devices.tapo_lamp_device)
    balanx_led = Device(devices.balanx_device)
    ubuntu_laptop = Device(devices.ubuntu_laptop_device)

    async def handle_event(self):
        tasks = [self.mikrotik.run_script('gaming-on'), self.tapo_lamp.turn_off(), self.pixoo.show_gaming_mode_enable()]
        await self.run_parallel(*tasks)
        music = services.select_random_music(settings.INTRO_MUSIC_PATH)
        music_duration = await services.get_music_duration(music)
        tasks = [
            self.balanx_led.go_rainbow(music_duration),
            self.pixoo.show_visualizer(music_duration),
            self.ubuntu_laptop.play_music(music),
        ]
        await self.run_parallel(*tasks)

        return AutomationResult(automation=self.__class__.__name__, handled=True, actions=self.actions)


@event_handler(EventName.GAMING_MODE_OFF)
class GamingModeDisableAutomation(BaseAutomation):
    mikrotik = Device(devices.mikrotik_device)
    pixoo = Device(devices.pixoo_device)
    tapo_lamp = Device(devices.tapo_lamp_device)
    balanx_led = Device(devices.balanx_device)
    ubuntu_laptop = Device(devices.ubuntu_laptop_device)

    async def handle_event(self):
        tasks = [
            self.mikrotik.run_script('gaming-off'),
            self.tapo_lamp.turn_on(),
            self.pixoo.show_gaming_mode_disable(),
        ]
        await self.run_parallel(*tasks)
        music = services.select_random_music(settings.OUTRO_MUSIC_PATH)
        music_duration = await services.get_music_duration(music)
        tasks = [
            self.balanx_led.go_rainbow(music_duration),
            self.pixoo.show_visualizer(music_duration),
            self.ubuntu_laptop.play_music(music),
        ]
        await self.run_parallel(*tasks)

        return AutomationResult(automation=self.__class__.__name__, handled=True, actions=self.actions)


@event_handler(EventName.ALEXA_HELLO_WORLD)
class AlexaHelloWorldAutomation(BaseAutomation):
    pixoo = Device(devices.pixoo_device)

    async def handle_event(self):
        result = await self.pixoo.show_alexa_hello_world()
        self.actions.append(result)
        return AutomationResult(automation=self.__class__.__name__, handled=True, actions=self.actions)


@event_handler(EventName.DOTA_KILL)
class DotaHeroKillAutomation(BaseAutomation):
    pixoo = Device(devices.pixoo_device)
    ubuntu_laptop = Device(devices.ubuntu_laptop_device)

    async def handle_event(self):
        music = services.select_random_music(settings.KILL_MUSIC_PATH)
        tasks = [self.pixoo.show_dota_kill(), self.ubuntu_laptop.play_music(music)]
        await self.run_parallel(*tasks)

        return AutomationResult(automation=self.__class__.__name__, handled=True, actions=self.actions)


@event_handler(EventName.DOTA_DEATH)
class DotaHeroDeathAutomation(BaseAutomation):
    pixoo = Device(devices.pixoo_device)
    ubuntu_laptop = Device(devices.ubuntu_laptop_device)

    async def handle_event(self):
        music = services.select_random_music(settings.DEATH_MUSIC_PATH)
        tasks = [self.pixoo.show_dota_death(), self.ubuntu_laptop.play_music(music)]
        await self.run_parallel(*tasks)

        return AutomationResult(automation=self.__class__.__name__, handled=True, actions=self.actions)
