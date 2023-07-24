import inspect
from enum import Enum


def enum_from_string(cls: Enum, s: str):
    for state in cls.__members__.values():
        if state.value == s:
            return state
    raise ValueError(f"Invalid {cls.name} string")


class DictConvertMixin:
    def __init__(self, d: dict) -> None:
        for key, value in d.items():
            old_value = getattr(self, key, None)
            if old_value != None and isinstance(old_value, Enum):
                value = enum_from_string(old_value.__class__, value)
            setattr(self, key, value)


class StringEnumMixin:
    @classmethod
    def from_string(cls, s: str):
        return enum_from_string(cls, s)
