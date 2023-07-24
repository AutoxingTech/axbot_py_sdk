import logging
import time

import requests

from .device_info import DeviceInfo
from .exceptions import AxException
from .planning.actions import MoveAction, MoveType
from .planning.state import PlanningState
from .ws_client import TopicName, WsClient


class Client:
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.__base_url = base_url
        self.__ws: WsClient = None
        self.__last_action = None
        self.__action_id = -1
        self.device_info: DeviceInfo = None
        self.planning_state = PlanningState()

    def connect(self):
        info = self.get_device_info()
        if info == None:
            raise AxException(f"Failed to connect to robot at {self.__base_url}")

        self.device_info = info

        def on_topic_received(name: str, msg: dict):
            if name == TopicName.PLANNING_STATE:
                self.planning_state = PlanningState(msg)

        self.__ws = WsClient(on_topic_received, self.__base_url.replace("http://", "ws://"))

    def disconnect(self):
        if self.__ws != None:
            self.__ws.disconnect()
            self.__ws = None

    def get_device_info(self) -> DeviceInfo or None:
        try:
            res = requests.get(self.__base_url + "/device/info")
        except requests.exceptions.ConnectionError:
            logging.error("Failed to get device info")
            return None

        if not res.ok:
            logging.error("Failed to get device info")
            return None

        info = DeviceInfo(res.json())
        return info

    def move(self, action: MoveAction):
        if action.type == MoveType.SLEEP:
            time.sleep(action.sleep_duration)
            return

        request_data = action.make_request_data(self.__last_action)

        r = requests.post(
            self.__base_url + "/chassis/moves",
            json=request_data,
        )

        if not r.ok:
            logging.error("Failed to create move action", r)
            raise AxException("Failed to make the move")

        action.id = r.json()["id"]

        self.__last_action = action
