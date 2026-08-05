import httpx


class PixooRestClient:
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=5)

    async def close(self) -> None:
        await self._client.aclose()

    async def post_json(self, path: str, payload: dict) -> None:
        response = await self._client.post(path, json=payload)
        response.raise_for_status()

    async def post_form(self, path: str, payload: dict) -> None:
        response = await self._client.post(path, data=payload)
        response.raise_for_status()

    async def play_buzzer(self, active_ms: int, inactive_ms: int, total_ms: int) -> None:
        path = '/passthrough/device/playBuzzer'
        payload = {
            'Command': 'Device/PlayBuzzer',
            'ActiveTimeInCycle': active_ms,
            'OffTimeInCycle': inactive_ms,
            'PlayTotalTime': total_ms,
        }

        await self.post_json(path, payload)

    async def set_clock_face(self, clock_face_id=0) -> None:
        path = '/passthrough/channel/setIndex'
        payload = {
            'Command': 'Channel/SetIndex',
            'SelectIndex': clock_face_id,
        }
        await self.post_json(path, payload)

    async def set_custom_clock_face(self, clock_face_id=0) -> None:
        path = '/passthrough/channel/setCustomPageIndex'
        payload = {
            'Command': 'Channel/SetCustomPageIndex',
            'CustomPageIndex': clock_face_id,
        }
        await self.post_json(path, payload)

    async def restore_default_clock_face(self) -> None:
        await self.set_clock_face(clock_face_id=0)

    async def fill_black(self, push=True) -> None:
        path = '/fill'
        payload = {
            'r': '0',
            'g': '0',
            'b': '0',
            'push_immediately': 'true' if push else 'false',
        }

        await self.post_form(path, payload)

    async def show_text(self, text: str, *, r: int, g: int, b: int, x: int = 2, y: int = 30, push=True) -> None:
        path = '/text'
        payload = {
            'text': text,
            'x': x,
            'y': y,
            'r': r,
            'g': g,
            'b': b,
            'push_immediately': 'true' if push else 'false',
        }
        await self.post_form(path, payload)

    async def health(self) -> dict:
        response = await self._client.get('/health')
        response.raise_for_status()
        return response.json()
