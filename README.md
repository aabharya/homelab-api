# Druid Home Lab API

Home lab automation gateway — receives events via REST and fans them out to physical devices through an in-process event bus.

## Stack

- **Python 3.12** + **FastAPI** + **Uvicorn**
- **httpx** — async HTTP (Pixoo display, device health)
- **bleak** — Bluetooth LE (Balanx LED controller)
- **tapo** — TP-Link smart bulb control
- **pydantic-settings** — env-based configuration
- **rich** — colored logging
- **ruff** — linting & formatting
- **uv** — package management


## Architecture

```
HTTP Request
    │
    ▼
FastAPI Routes
    │
    ▼
Event dataclass created
    │
    ▼
event_bus.publish(event)
    │
    ▼
EventBus dispatches to registered automation classes
(via @event_handler decorator)
    │
    ▼
Automation.handle_event() → device calls
    │
    ▼
Device clients (BLE / REST / SSH / subprocess)
```

### Core patterns

| Pattern | What it does |
|---|---|
| **Event bus** | Routes never touch devices directly. Every action goes through `event_bus.publish()`, which fans out to registered automation handlers. |
| **Decorator registration** | `@event_handler(EventName.X)` on an automation class auto-registers it — no central registry to maintain. |
| **Device descriptors** | `Device(devices.pixoo_device)` as a class attribute gives automation instances `self.pixoo` access without `__init__` wiring. |
| **Singleton devices** | One instance per device type, created at import time. `.env` must be valid on startup or the app crashes. |
| **Fire-and-forget tasks** | `publish()` creates `asyncio.Task`s per handler. `shutdown()` gathers all pending tasks before exit. |

## Configuration

All config lives in `.env` (loaded by pydantic-settings):

| Variable | Purpose |
|---|---|
| `MIKROTIK_HOST` | Router IP |
| `MIKROTIK_USERNAME` / `MIKROTIK_PASSWORD` | SSH credentials for router |
| `TAPO_USERNAME` / `TAPO_PASSWORD` / `TAPO_LIGHT_IP` | TP-Link smart bulb credentials |
| `PIXO_REST_URL` | Pixoo REST API base URL |
| `PIXO_REQUEST_DELAY` | Delay between Pixoo REST calls (default `0.8`) |
| `UBUNTU_USERNAME` / `UBUNTU_PASSWORD` | Laptop SSH credentials |
| `INTRO_MUSIC_PATH` / `OUTRO_MUSIC_PATH` | Gaming mode music directories |
| `KILL_MUSIC_PATH` / `DEATH_MUSIC_PATH` | Dota 2 event music directories |
| `BALANX_LED_MAC` | Bluetooth MAC for LED controller |

## API Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET` | `/api/health/` | Health check |
| `POST` | `/api/events/gaming/on/` | Triggers gaming mode enable sequence |
| `POST` | `/api/events/gaming/off/` | Triggers gaming mode disable sequence |
| `GET` | `/api/devices/pixoo/health/` | Pixoo display health check |
| `POST` | `/api/devices/alexa/` | Alexa skill endpoint → shows "HELLO ALEXA!" |
| `POST` | `/api/devices/tuf/games/dota2/` | Dota 2 webhook → kill/death animations |

## Events

| Event | Trigger | Actions |
|---|---|---|
| `GAMING_MODE_ON` | `/api/events/gaming/on/` | MikroTik gaming script, lamp off, Pixoo text, LED fire→rainbow, random intro music |
| `GAMING_MODE_OFF` | `/api/events/gaming/off/` | MikroTik normal script, lamp on, Pixoo text, outro music |
| `ALEXA_HELLO_WORLD` | `/api/devices/alexa/` | Pixoo "HELLO ALEXA!" |
| `DOTA_KILL` | `/api/devices/tuf/games/dota2/` (type=kill) | Pixoo kill animation + kill music |
| `DOTA_DEATH` | `/api/devices/tuf/games/dota2/` (type=death) | Pixoo death animation + death music |

## Running

```bash
# install deps
uv sync

# run the server
uvicorn homelab_api.main:app --reload
```

