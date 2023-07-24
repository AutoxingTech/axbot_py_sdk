from enum import Enum


class MoveActionState(Enum):
    IDLE = "IDLE".lower()
    MOVING = "MOVING".lower()
    OSCILLATING = "OSCILLATING".lower()
    SUCCEEDED = "SUCCEEDED".lower()
    FAILED = "FAILED".lower()
    CANCELLED = "CANCELLED".lower()

    @staticmethod
    def from_string(s: str):
        for state in MoveActionState.__members__.values():
            if state.value == s:
                return state
        raise ValueError("Invalid MovingState string")


class PlanningState:
    def __init__(self, obj: dict = None) -> None:
        self.moving_state = MoveActionState.IDLE
        self.in_elevator = False

        if obj != None:
            for key, value in obj.items():
                setattr(self, key, value)

            # convert string to enum
            self.moving_state = MoveActionState.from_string(self.moving_state)
