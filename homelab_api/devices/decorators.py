from functools import wraps

from homelab_api.automations.protocols import ActionResult
from homelab_api.loggings import get_logger

from .base import BaseDevice

logger = get_logger('actions')


def device_action(func):
    @wraps(func)
    async def wrapper(self: BaseDevice, *args, **kwargs):
        device_name = self.device_name
        action_name = func.__name__.lower()

        if not await self.acquire():
            logger.warning('Device action dropped (busy): %s.%s', device_name, action_name)
            return ActionResult(device=device_name, action=action_name, success=False)

        try:
            await func(self, *args, **kwargs)
            logger.info('Device action succeeded: %s.%s', device_name, action_name)
            return ActionResult(device=device_name, action=action_name, success=True)
        except Exception:
            logger.exception('Device action failed: %s.%s', device_name, action_name)
            return ActionResult(device=device_name, action=action_name, success=False)
        finally:
            self.release()

    return wrapper
