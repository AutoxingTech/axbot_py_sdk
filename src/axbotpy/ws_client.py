import json
import threading
from enum import Enum
from typing import Callable

import websocket


class TopicName:
    PLANNING_STATE = "/planning_state"


class WsClient:
    """
    The websocket client which receives realtime information of the robot
    """

    def __init__(self, on_topic_received: Callable[[str, dict], None], base_url: str = "ws://localhost:8000") -> None:
        self.__on_topic_received = on_topic_received
        self.__url = base_url + "/ws/v2/topics"
        self.__thread = None
        self.__ws: websocket.WebSocketApp = None

        self.__thread = threading.Thread(target=self.__thread_func)
        self.__thread.start()

    def __thread_func(self):
        def __on_message(_ws, message):
            msg = json.loads(message)
            if "topic" in msg:
                self.__on_topic_received(msg["topic"], msg)

        def __on_error(_ws, error):
            print(error)

        def __on_close(_ws, _close_status_code, _close_msg):
            print("### closed ###")

        def __on_open(ws: websocket.WebSocketApp):
            print("Opened connection")
            ws.send(json.dumps({"enable_topic": TopicName.PLANNING_STATE}))

        self.__ws = websocket.WebSocketApp(
            self.__url,
            on_open=__on_open,
            on_message=__on_message,
            on_error=__on_error,
            on_close=__on_close,
        )
        self.__ws.run_forever()

    def disconnect(self):
        self.__ws.close()
        self.__thread.join()
