from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


@dataclass(frozen=True)
class Event:
    name: str
    source: str
    created_at: datetime
    payload: dict


class GamingModeRequest(BaseModel):
    latency_ms: int | None = None
