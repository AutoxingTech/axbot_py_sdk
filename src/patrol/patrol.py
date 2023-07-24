#!/usr/bin/env python3
import json
import time

import requests
import rospy

from axbotpy.planning import MoveAction, MoveType
from src.axbotpy.ws_client import WsClient

from .actions.obstacle import ACTIONS

# pylint:disable=no-self-use


def die(msg: str, res: requests.Response = None):
    if isinstance(res, requests.Response):
        res_text = json.dumps(res.json())
        print(f"{msg}. Response = {res_text}")
    else:
        print(msg)
    rospy.signal_shutdown(msg)


class Progress:
    step = 0
    icons = "/-\\|/-\\|"

    def __repr__(self) -> str:
        self.step += 1
        if self.step >= len(self.icons):
            self.step = 0
        return self.icons[self.step]


def main():
    progress = Progress()
    headers = {"Secret": "dRw6JGyzFFwKNfFPQ8FFF"}

    rospy.init_node("patrol_node")
    ws = WsClient()

    last_action: MoveAction = None
    while not rospy.is_shutdown():
        for action in ACTIONS:
            if rospy.is_shutdown():
                break

            if action.type == MoveType.SLEEP:
                time.sleep(action.sleep_duration)
                continue

            request_data = action.make_request_data(last_action)

            r = requests.post(
                "http://127.0.0.1:8000/chassis/moves",
                headers=headers,
                json=request_data,
            )

            if not r.ok:
                die("Failed to create move action", r)
            else:
                action_id = r.json()["id"]
                print(f"Action {action_id} {action} ...", end="")

            # wait for action to finish
            while not rospy.is_shutdown():
                r = requests.get(
                    f"http://127.0.0.1:8000/chassis/moves/{action_id}",
                    headers=headers,
                )
                if not r.ok:
                    die("Failed to get move action", r)

                data = r.json()
                state = data["state"]

                if state == "moving":
                    print(
                        f"\rAction {action_id} {action} ... {progress}, distance = {ws.planning_state.remaining_distance}",
                        end="",
                    )
                    continue
                if state == "succeeded":
                    print("succeeded")
                    break
                die(f"Action {action_id} {state}")
                break

            last_action = action

    ws.disconnect()


if __name__ == "__main__":
    main()
