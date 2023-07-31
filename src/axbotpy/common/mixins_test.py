import inspect
from enum import Enum

from .mixins import DictConvertMixin


class Color(Enum):
    NONE = "none"
    RED = "red"
    GREEN = "green"


class MyClass(DictConvertMixin):
    def __init__(self, obj: dict = None) -> None:
        # The enum member must have a default value,
        # because DictConvertMixin uses it to identify it as an enumeration.
        self.color = Color.NONE

        super().__init__(obj)


def test_dict_convert_mixin():
    obj = MyClass({"color": "red"})
    assert obj.color == Color.RED
