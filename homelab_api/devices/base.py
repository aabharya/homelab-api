import asyncio
from typing import Generic, TypeVar

T = TypeVar('T')


class Device(Generic[T]):
    def __init__(self, instance: T):
        self.instance = instance
        self.name: str | None = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner) -> T:
        return self.instance


class BaseDevice:
    def __init__(self, serialize_actions=False):
        self.serialize_actions = serialize_actions
        self._lock = asyncio.Lock() if self.serialize_actions else None

    async def acquire(self) -> bool:
        if self._lock is None:
            return True
        if self._lock.locked():
            return False
        await self._lock.acquire()
        return True

    def release(self) -> None:
        if self._lock is not None and self._lock.locked():
            self._lock.release()

    @property
    def device_name(self):
        return self.__class__.__name__.replace('Device', '').lower()
