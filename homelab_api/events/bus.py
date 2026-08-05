import asyncio
from collections import defaultdict

from homelab_api.automations.protocols import BaseAutomation
from homelab_api.events.enums import EventName
from homelab_api.events.models import Event
from homelab_api.loggings import get_logger

logger = get_logger('events')


class EventBus:
    def __init__(self):
        self.tasks: set[asyncio.Task] = set()
        self.handlers: dict[EventName, list[type[BaseAutomation]]] = defaultdict(list)

    def register_handler(self, event_name: EventName, automation_cls: type[BaseAutomation]) -> None:
        if automation_cls in self.handlers[event_name]:
            raise RuntimeError(
                f'Automation "{automation_cls.__module__}.{automation_cls.__name__}" '
                f'is already registered for "{event_name}".'
            )

        self.handlers[event_name].append(automation_cls)
        logger.info(
            "Registered automation '%s.%s' for event '%s'",
            automation_cls.__module__,
            automation_cls.__name__,
            event_name,
        )

    def publish(self, event: Event) -> None:
        for automation_cls in self.handlers[event.name]:
            logger.info('Handling event %s with automation %s', event.name, automation_cls.__name__)

            task = asyncio.create_task(run_automation(automation_cls, event))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

    async def shutdown(self) -> None:
        if self.tasks:
            await asyncio.gather(*self.tasks)


event_bus = EventBus()


def event_handler(event_name: EventName):
    def decorator(automation_cls: type[BaseAutomation]):
        event_bus.register_handler(event_name, automation_cls)
        return automation_cls

    return decorator


async def run_automation(automation_cls: type[BaseAutomation], event: Event) -> None:
    try:
        automation = automation_cls(event)
        result = await automation()

        logger.info(
            'Automation %s completed: handled=%s actions=%d', result.automation, result.handled, len(result.actions)
        )

    except Exception:
        logger.exception('Automation failed: %s', automation_cls.__name__)
