import asyncio

from homelab_api.configs import settings
from homelab_api.devices.base import BaseDevice
from homelab_api.devices.decorators import device_action

from .client import SP621EClient


class BalanXLedDevice(BaseDevice):
    def __init__(self, serialize_actions=False):
        super().__init__(serialize_actions)
        self.client = SP621EClient(settings.BALANX_LED_MAC)

    @device_action
    async def scene_gradient(self):
        """Gradient (Effect 142)."""
        await self.client.scene(effect=0x8E)

    @device_action
    async def scene_fire(self):
        """Fire Red/Yellow (Effect 5)."""
        await self.client.scene(effect=0x05)

    @device_action
    async def go_rainbow(self, delay: int) -> None:
        await self.scene_fire()
        await asyncio.sleep(delay)
        await self.scene_gradient()


balanx_device = BalanXLedDevice()
