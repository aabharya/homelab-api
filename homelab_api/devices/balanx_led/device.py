import asyncio

from homelab_api.configs import settings

from .client import SP621EClient


class BalanXLedDevice:
    def __init__(self):
        self.client = SP621EClient(settings.BALANX_LED_MAC)

    async def scene_gradient(self):
        """Gradient (Effect 142)."""
        await self.client.scene(effect=0x8E)

    async def scene_fire(self):
        """Fire Red/Yellow (Effect 5)."""
        await self.client.scene(effect=0x05)

    async def go_rainbow(self, delay: int) -> None:
        await self.scene_fire()
        await asyncio.sleep(delay)
        await self.scene_gradient()


balanx_device = BalanXLedDevice()
