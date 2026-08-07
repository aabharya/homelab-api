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
    @property
    def device_name(self):
        return self.__class__.__name__.replace('Device', '').lower()
