import asyncio

from bleak import BleakClient, BleakError, BleakScanner

from homelab_api.loggings import get_logger

logger = get_logger('balanx_led')


class SP621EClient:
    WRITE_UUID = '0000ffe1-0000-1000-8000-00805f9b34fb'

    def __init__(self, address: str, adapter: str = 'hci0'):
        self.address = address
        self.adapter = adapter
        self.client: BleakClient | None = None

    async def connect(self):
        if self.client and self.client.is_connected:
            return

        device = await BleakScanner.find_device_by_address(self.address, timeout=5, adapter=self.adapter)
        if device is None:
            raise BleakError(f'SP621E {self.address} not found')

        self.client = BleakClient(device, adapter=self.adapter)
        await self.client.connect()
        logger.info(f'Connected to BanlanX SP621E on {self.address} via {self.adapter}')

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def _ensure_connected(self):
        if not self.client or not self.client.is_connected:
            await self.connect()

    async def send(self, payload: bytes):
        await self._ensure_connected()
        await self.client.write_gatt_char(self.WRITE_UUID, payload, response=False)

    async def power(self, state: bool):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x62,
                    0x01,
                    0x01 if state else 0x00,
                ]
            )
        )

    async def effect(self, effect_id: int):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x63,
                    0x01,
                    effect_id & 0xFF,
                ]
            )
        )

    async def brightness(self, level: int):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x66,
                    0x01,
                    level & 0xFF,
                ]
            )
        )

    async def effect_speed(self, speed: int):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x67,
                    0x01,
                    speed & 0xFF,
                ]
            )
        )

    async def effect_length(self, length: int):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x68,
                    0x01,
                    length & 0xFF,
                ]
            )
        )

    async def rgb(self, r: int, g: int, b: int, brightness: int = 255):
        await self.send(
            bytes(
                [
                    0xA0,
                    0x69,
                    0x04,
                    r & 0xFF,
                    g & 0xFF,
                    b & 0xFF,
                    brightness & 0xFF,
                ]
            )
        )

    async def scene(self, effect: int, brightness: int = 255, length: int = 80, speed: int = 10):
        try:
            await self._ensure_connected()
            await self.power(True)
            await asyncio.sleep(0.5)
            await self.effect(effect)
            await asyncio.sleep(0.05)

            await self.brightness(brightness)
            await asyncio.sleep(0.05)

            await self.effect_length(length)
            await asyncio.sleep(0.05)

            await self.effect_speed(speed)
        except BleakError as e:
            logger.error(f'Balanx LED got an error: {e}')
