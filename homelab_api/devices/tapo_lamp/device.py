from homelab_api.configs import settings

from .client import TapoClient


class TapoLampDevice:
    def __init__(self):
        self.client = TapoClient(settings.TAPO_USERNAME, settings.TAPO_PASSWORD, settings.TAPO_LIGHT_IP)

    async def turn_off(self):
        await self.client.turn_off()

    async def turn_on(self):
        await self.client.turn_on()


tapo_lamp_device = TapoLampDevice()
