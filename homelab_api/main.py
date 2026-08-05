from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from homelab_api import configs, devices
from homelab_api.events.bus import event_bus
from homelab_api.events.enums import EventName
from homelab_api.events.models import Event, GamingModeRequest
from homelab_api.loggings import get_logger
from homelab_api.middlewares import LoggingMiddleware

logger = get_logger('homelab_api')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from homelab_api.automations import definitions  # noqa

    yield
    await devices.pixoo_device.client.close()
    await devices.balanx_device.client.disconnect()
    await event_bus.shutdown()


def get_application() -> FastAPI:
    app = FastAPI(**configs.app_configs, lifespan=lifespan)
    return app


api = get_application()
api.add_middleware(LoggingMiddleware)


@api.get('/api/health/')
async def api_health():
    return {'status': 'ok'}


@api.post('/api/events/gaming/on/')
async def gaming_mode_on(payload: GamingModeRequest):
    event_context = {
        'name': EventName.GAMING_MODE_ON,
        'source': 'api',
        'created_at': datetime.now(),
        'payload': payload.model_dump(),
    }
    event = Event(**event_context)

    event_bus.publish(event)

    return {'status': 'ok', 'event': event_context['name']}


@api.post('/api/events/gaming/off/')
async def gaming_mode_off(payload: GamingModeRequest):
    event_context = {
        'name': EventName.GAMING_MODE_OFF,
        'source': 'api',
        'created_at': datetime.now(),
        'payload': payload.model_dump(),
    }
    event = Event(**event_context)

    event_bus.publish(event)

    return {'status': 'ok', 'event': event_context['name']}


@api.get('/api/devices/pixoo/health/')
async def pixoo_health():
    result = await devices.pixoo_device.health()
    if result['status'] != 'ok':
        raise HTTPException(status_code=503, detail=result)
    return result


@api.post('/api/devices/alexa/')
async def alexa(request: Request):
    payload = await request.json()
    logger.info(f'Alexa request payload: {payload}')
    event_context = {
        'name': EventName.ALEXA_HELLO_WORLD,
        'source': 'api',
        'created_at': datetime.now(),
        'payload': payload,
    }
    event = Event(**event_context)

    event_bus.publish(event)

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Hello World from Druid Home! I am ready to serve you master, God Blesses you my Lord.',
            },
            'shouldEndSession': True,
        },
    }


@api.post('/api/devices/tuf/games/dota2/')
async def dota_event(request: Request):
    payload = await request.json()
    logger.info(f'Gaming laptop dota 2 request payload: {payload}')
    event_context = {
        'source': 'tuff',
        'created_at': datetime.now(),
        'payload': payload,
    }
    event_type = payload.get('type', '')
    if event_type == 'kill':
        event_context['name'] = EventName.DOTA_KILL
    if event_type == 'death':
        event_context['name'] = EventName.DOTA_DEATH

    event = Event(**event_context)
    event_bus.publish(event)

    return {'status': 'ok', 'event': event_type}
