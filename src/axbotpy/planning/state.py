import json

from axbotpy.common.mixins import DictConvertMixin

from .actions import MoveActionState


class PlanningState(DictConvertMixin):
    """
    Mostly, the state of the current move.
    """

    def __init__(self, obj: dict = None) -> None:
        self.action_id = -1
        self.remaining_distance = 0
        self.move_state = MoveActionState.IDLE
        self.in_elevator = False

        super().__init__(obj)
