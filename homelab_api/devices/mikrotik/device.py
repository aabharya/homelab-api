from homelab_api.configs import settings

from .client import MikrotikClient


class MikrotikDevice:
    def __init__(self):
        self.client = MikrotikClient(
            username=settings.MIKROTIK_USERNAME, password=settings.MIKROTIK_PASSWORD, host=settings.MIKROTIK_HOST
        )

    async def run_script(self, script_name: str) -> None:
        await self.client.run_script(script_name)


mikrotik_device = MikrotikDevice()
