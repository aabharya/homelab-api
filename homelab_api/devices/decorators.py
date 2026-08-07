from functools import wraps

from homelab_api.automations.protocols import ActionResult
from homelab_api.loggings import get_logger

logger = get_logger('actions')


def device_action(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        device_name = self.__class__.__name__.replace('Device', '').lower()
        action_name = func.__name__.lower()

        try:
            await func(self, *args, **kwargs)
            logger.info('Device action succeeded: %s.%s', device_name, action_name)
            return ActionResult(device=device_name, action=action_name, success=True)
        except Exception:
            logger.exception('Device action failed: %s.%s', device_name, action_name)
            return ActionResult(device=device_name, action=action_name, success=False)

    return wrapper
