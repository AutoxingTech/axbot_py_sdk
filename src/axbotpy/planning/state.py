import inspect
from enum import Enum

from src.axbotpy.common.mixins import DictConvertMixin

from .actions import MoveActionState


class PlanningState(DictConvertMixin):
    def __init__(self, obj: dict = None) -> None:
        self.action_id = -1
        self.remaining_distance = 0
        self.moving_state = MoveActionState.IDLE
        self.in_elevator = False

        super().__init__(obj)
