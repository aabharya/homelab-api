from homelab_api.configs import settings
from homelab_api.devices.base import BaseDevice
from homelab_api.devices.decorators import device_action

from .client import MikrotikClient


class MikrotikDevice(BaseDevice):
    def __init__(self, serialize_actions=False):
        super().__init__(serialize_actions)
        self.client = MikrotikClient(
            username=settings.MIKROTIK_USERNAME, password=settings.MIKROTIK_PASSWORD, host=settings.MIKROTIK_HOST
        )

    @device_action
    async def run_script(self, script_name: str) -> None:
        await self.client.run_script(script_name)


mikrotik_device = MikrotikDevice()
