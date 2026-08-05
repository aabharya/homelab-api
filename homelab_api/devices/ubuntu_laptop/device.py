from asyncio import subprocess

from homelab_api.configs import settings

from .client import UbuntuLaptopClient


class UbuntuLaptopDevice:
    def __init__(self):
        self.client = UbuntuLaptopClient(username=settings.UBUNTU_USERNAME, password=settings.UBUNTU_PASSWORD)

    async def play_music(self, path: str) -> None:
        command = f'ffplay -nodisp -autoexit {path}'
        process = await subprocess.create_subprocess_shell(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        await process.wait()


ubuntu_laptop_device = UbuntuLaptopDevice()
