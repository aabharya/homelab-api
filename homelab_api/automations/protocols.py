import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from homelab_api.events.models import Event
from homelab_api.loggings import get_logger

logger = get_logger('automations')


@dataclass(slots=True)
class ActionResult:
    device: str
    action: str
    success: bool


@dataclass(slots=True)
class AutomationResult:
    automation: str
    handled: bool
    actions: list[ActionResult] = field(default_factory=list)


class Automateable(Protocol):
    async def handle(self) -> AutomationResult: ...


class BaseAutomation(Automateable):
    def __init__(self, event: Event) -> None:
        self.event = event
        self.actions = []

    async def handle_event(self) -> AutomationResult:
        pass

    async def run_parallel(self, *automation_tasks) -> tuple[BaseException | Any]:
        tasks = [asyncio.create_task(task) for task in automation_tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def __call__(self) -> AutomationResult:
        start = time.perf_counter()
        try:
            return await self.handle_event()
        finally:
            duration = time.perf_counter() - start
            logger.info('Automation %s took %.3fs', self.__class__.__name__, duration)
