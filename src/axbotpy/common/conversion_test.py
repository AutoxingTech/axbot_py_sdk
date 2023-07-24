import inspect
from enum import Enum

from .conversion import DictConvertMixin


class Color(Enum):
    RED = "red"
    GREEN = "green"


class MyClass(DictConvertMixin):
    def __init__(self, obj: dict = None) -> None:
        self.color = Color.RED

        super().__init__(obj)


def test_dict_convert_mixin():
    obj = MyClass({"color": "red"})
    assert obj.color == Color.RED
