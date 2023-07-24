import logging
import time

import requests

from .planning.actions import MoveAction, MoveType
from .planning.state import PlanningState
from .ws_client import TopicName, WsClient


class Client:
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.__base_url = base_url
        self.__ws: WsClient
        self.__last_action = None
        self.__action_id = -1
        self.__planning_state = PlanningState()

    def connect(self):
        def on_topic_received(name: str, msg: str):
            if msg["topic"] == TopicName.PLANNING_STATE:
                self.__planning_state = PlanningState(msg)

        self.__ws = WsClient(on_topic_received, self.__base_url.replace("http://", "ws://"))

    def disconnect(self):
        self.__ws.disconnect()
        self.__ws = None

    @property
    def planning_state(self) -> PlanningState:
        return self.__planning_state

    def device_info() -> DeviceInfo:
        r = requests.post(
            "http://127.0.0.1:8000/chassis/moves",
            json=request_data,
        )

    def move(self, action: MoveAction) -> bool:
        if action.type == MoveType.SLEEP:
            time.sleep(action.sleep_duration)
            return

        request_data = action.make_request_data(self.__last_action)

        r = requests.post(
            "http://127.0.0.1:8000/chassis/moves",
            json=request_data,
        )

        if not r.ok:
            logging.error("Failed to create move action", r)
            return False

        self.__action_id = r["id"]

        return True
