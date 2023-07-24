import inspect
from enum import Enum


class DictConvertMixin:
    def __init__(self, d: dict) -> None:
        for key, value in d.items():
            old_value = getattr(self, key, None)
            if old_value != None and isinstance(old_value, Enum):
                value = old_value.from_string(value)
            setattr(self, key, value)
