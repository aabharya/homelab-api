from homelab_api.configs import settings
from homelab_api.devices.base import BaseDevice
from homelab_api.devices.decorators import device_action

from .client import TapoClient


class TapoLampDevice(BaseDevice):
    def __init__(self, serialize_actions=False):
        super().__init__(serialize_actions)
        self.client = TapoClient(settings.TAPO_USERNAME, settings.TAPO_PASSWORD, settings.TAPO_LIGHT_IP)

    @device_action
    async def turn_off(self):
        await self.client.turn_off()

    @device_action
    async def turn_on(self):
        await self.client.turn_on()


tapo_lamp_device = TapoLampDevice()
