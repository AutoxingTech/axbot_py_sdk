import math
from typing import List

from axbotpy.planning.actions import AlongGivenRouteMoveAction, MoveAction, SleepAction

# hh-19
ACTIONS: List[MoveAction] = [
    MoveAction(target=[3.68, -13.05], target_ori=3.14),
    MoveAction(target=[4.12, 2.96], target_ori=math.pi * 3 / 2),
]

# ACTIONS: List[MoveAction] = [
#     MoveAction(target=[-0.64, 3.49], target_ori=-1.3965926),
#     AlongCentralLineMoveAction(coordinates=[[-0.44, 2.43]]),
#     SleepAction(1.0),
#     AlongCentralLineMoveAction(coordinates=[[-0.27, 1.32]]),
#     SleepAction(1.0),
#     AlongCentralLineMoveAction(coordinates=[[-0.03, -0.01]]),
#     SleepAction(1.0),
#     AlongCentralLineMoveAction(coordinates=[[-0.27, 1.32]]),
#     SleepAction(1.0),
#     AlongCentralLineMoveAction(coordinates=[[-0.44, 2.43]]),
#     SleepAction(1.0),
#     AlongCentralLineMoveAction(coordinates=[[-0.64, 3.49]]),
# ]

# ACTIONS: List[MoveAction] = [
#     MoveAction(target=[1.37, 0.48], target_ori=1.745),
#     AlongCentralLineMoveAction(coordinates=[[0.81, 3.6]]),
#     MoveAction(target=[-0.64, 3.49], target_ori=-1.3965926),
#     AlongCentralLineMoveAction(coordinates=[[0.03, 0.05]]),
#     MoveAction(target=[-1.35, -0.29], target_ori=1.745),
#     AlongCentralLineMoveAction(coordinates=[[-1.97, 3.27]]),
#     MoveAction(target=[-3.34, 3.19], target_ori=-1.3965926),
#     AlongCentralLineMoveAction(coordinates=[[-2.82, -0.05]]),
# ]
