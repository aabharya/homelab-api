import asyncio

from homelab_api.configs import settings
from homelab_api.devices.base import BaseDevice
from homelab_api.devices.decorators import device_action

from .client import PixooRestClient


class PixooDevice(BaseDevice):
    def __init__(self, serialize_actions=True):
        super().__init__(serialize_actions)
        self.client = PixooRestClient(base_url=settings.PIXO_REST_URL)

    @device_action
    async def show_gaming_mode_enable(self):
        await self.client.fill_black()
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.play_buzzer(100, 100, 1000)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.show_text('GAMING MODE ON!', r=255, g=0, b=0)

    @device_action
    async def show_gaming_mode_disable(self):
        await self.client.fill_black()
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.play_buzzer(500, 500, 1000)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.show_text('GAMING MODE OFF!', r=0, g=255, b=0)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)

    @device_action
    async def show_alexa_hello_world(self):
        await self.client.fill_black()
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.show_text('HELLO ALEXA!', r=0, g=255, b=0)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.restore_default_clock_face()

    @device_action
    async def show_dota_kill(self):
        await self.client.set_custom_clock_face(clock_face_id=1)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.play_buzzer(500, 500, 1000)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.set_clock_face(clock_face_id=3)
        await asyncio.sleep(5)
        await self.client.restore_default_clock_face()

    @device_action
    async def show_dota_death(self):
        await self.client.set_custom_clock_face(clock_face_id=0)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.play_buzzer(100, 100, 1000)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.set_clock_face(clock_face_id=3)
        await asyncio.sleep(5)
        await self.client.restore_default_clock_face()

    @device_action
    async def show_visualizer(self, delay: int | None = None):
        await self.client.set_clock_face(clock_face_id=2)
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        if delay is not None:
            await asyncio.sleep(delay)
            await self.client.restore_default_clock_face()
            await asyncio.sleep(settings.PIXO_REQUEST_DELAY)

    @device_action
    async def hide_visualizer(self):
        await asyncio.sleep(settings.PIXO_REQUEST_DELAY)
        await self.client.restore_default_clock_face()

    async def health(self):
        try:
            result = await self.client.health()
            return {'status': 'ok', 'pixoo': result}

        except Exception as exc:
            return {'status': 'error', 'error': str(exc)}


pixoo_device = PixooDevice(serialize_actions=True)
