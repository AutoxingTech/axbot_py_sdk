from typing import List

from axbotpy.planning import AlongGivenRouteMoveAction, MoveAction

ACTIONS: List[MoveAction] = [
    MoveAction(target=[12.4, 20.14]),
    AlongGivenRouteMoveAction(
        coordinates=[
            [-5.98, -11.49],
        ]
    ),
    AlongGivenRouteMoveAction(
        coordinates=[
            [12.4, 20.14],
        ]
    ),
]
