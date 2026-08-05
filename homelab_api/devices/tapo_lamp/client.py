from tapo import ApiClient


class TapoClient:
    def __init__(self, username: str, password: str, ip: str):
        self.client = ApiClient(username, password)
        self.tapo_ip = ip

    async def turn_off(self):
        device = await self.client.l510(self.tapo_ip)
        await device.off()

    async def turn_on(self):
        device = await self.client.l510(self.tapo_ip)
        await device.on()
