#!/usr/bin/env python3
from enum import Enum
from typing import List


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


class MoveType(Enum):
    STANDARD = "STANDARD".lower()
    PARKING = "PARKING".lower()
    ALONG_CENTRAL_LINE = "ALONG_CENTRAL_LINE".lower()
    ALONG_GIVEN_ROUTE = "ALONG_GIVEN_ROUTE".lower()
    SLEEP = "SLEEP".lower()


class MoveAction:
    def __init__(
        self,
        target: List[float] = None,
        type: MoveType = MoveType.STANDARD,
        coordinates: List[List[float]] = None,
        target_ori=None,
        detour_tolerance=None,
    ) -> None:
        self.target = target
        self.type = type
        self.coordinates = coordinates
        self.sleep_duration = 0
        self.target_ori = target_ori
        self.detour_tolerance = detour_tolerance

    def to_json(self) -> any:
        rtn = {"type": self.type.value}
        if self.target != None:
            rtn = {
                **rtn,
                "target_x": self.target[0],
                "target_y": self.target[1],
                "target_z": 0,
            }

        if self.target_ori != None:
            rtn = {**rtn, "target_ori": self.target_ori}

        if self.coordinates != None:
            coords = []
            for point in self.coordinates:
                coords.append(str(point[0]))
                coords.append(str(point[1]))
            rtn = {**rtn, "route_coordinates": ",".join(coords)}

        if self.detour_tolerance != None:
            rtn = {**rtn, "detour_tolerance": self.detour_tolerance}

        # add accuracy
        rtn = {**rtn, "target_accuracy": 0.01}

        return rtn

    def make_request_data(self, last_action: "MoveAction") -> any:
        data = self.to_json()
        if last_action == None or self.coordinates == None:
            return data

        # add last action's point to the first point
        if last_action.coordinates != None:
            last_point = last_action.coordinates[-1]
        elif last_action.target != None:
            last_point = last_action.target
        else:
            last_point = None

        if last_point == None:
            return data

        data["route_coordinates"] = f"{last_point[0]},{last_point[1]}," + data["route_coordinates"]
        return data

    def __repr__(self) -> str:
        if self.coordinates != None:
            return f"Action({self.type.value}, coordinates={self.target})"
        elif self.target != None and self.target_ori != None:
            return f"Action({self.type.value}, target={self.target})"

        return f"Action({self.type.value}, target={self.target})"


class AlongGivenRouteMoveAction(MoveAction):
    def __init__(self, coordinates: List[List[float]], detour_tolerance=0) -> None:
        super().__init__(
            None, type=MoveType.ALONG_GIVEN_ROUTE, coordinates=coordinates, detour_tolerance=detour_tolerance
        )


class AlongCentralLineMoveAction(MoveAction):
    def __init__(self, coordinates: List[List[float]]) -> None:
        super().__init__(None, type=MoveType.ALONG_CENTRAL_LINE, coordinates=coordinates, detour_tolerance=0)


class SleepAction(MoveAction):
    def __init__(self, duration: float) -> None:
        super().__init__(None, type=MoveType.SLEEP, coordinates=None)
        self.sleep_duration = duration


class ParkingAction(MoveAction):
    def __init__(self, target: List[float] = None, target_ori=None) -> None:
        super().__init__(target=target, type=MoveType.PARKING, coordinates=None, target_ori=target_ori)
