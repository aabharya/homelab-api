from asyncio import subprocess

from homelab_api.configs import settings
from homelab_api.devices.base import BaseDevice
from homelab_api.devices.decorators import device_action

from .client import UbuntuLaptopClient


class UbuntuLaptopDevice(BaseDevice):
    def __init__(self, serialize_actions=False):
        super().__init__(serialize_actions)
        self.client = UbuntuLaptopClient(username=settings.UBUNTU_USERNAME, password=settings.UBUNTU_PASSWORD)

    @device_action
    async def play_music(self, path: str) -> None:
        command = f'ffplay -nodisp -autoexit {path}'
        process = await subprocess.create_subprocess_shell(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        await process.wait()


ubuntu_laptop_device = UbuntuLaptopDevice()
