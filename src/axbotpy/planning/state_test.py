from .actions import MoveActionState
from .state import PlanningState


def test_planning_state():
    state = PlanningState(
        {
            "action_id": 111,
            "move_state": "moving",
            "remaining_distance": 10.1,
        }
    )
    assert state.move_state == MoveActionState.MOVING
    assert state.action_id == 111
    assert state.remaining_distance == 10.1
