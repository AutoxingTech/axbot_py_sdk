#!/usr/bin/env python3
import json
import time

import requests

from axbotpy.app_framework import App, Rate
from axbotpy.client import Client
from axbotpy.planning.actions import MoveActionState, MoveType

from .actions.obstacle import ACTIONS

# pylint:disable=no-self-use


def die(msg: str, res: requests.Response = None):
    if isinstance(res, requests.Response):
        res_text = json.dumps(res.json())
        print(f"{msg}. Response = {res_text}")
    else:
        print(msg)
    App.shutdown(1)


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

    App.init_node("patrol_node")
    client = Client("http://localhost:8000")

    client.connect()

    while App.ok():
        for action in ACTIONS:
            if not App.ok():
                break

            if action.type == MoveType.SLEEP:
                time.sleep(action.sleep_duration)
                continue

            if not client.move(action):
                die("Failed to create move action")
                return

            print(f"Action {action.id} {action} created")

            # wait for action to finish
            rate = Rate(4)
            while rate.ok():
                planning_state = client.planning_state
                if planning_state.action_id != action.id:
                    # other action, ignore
                    print(f"\r  Waiting...", end="")
                    continue

                if planning_state.move_state in [MoveActionState.IDLE, MoveActionState.MOVING]:
                    print(
                        f"\r  {planning_state.move_state.value} ... {progress}, distance = {round(client.planning_state.remaining_distance, 2)}",
                        end="",
                    )
                    continue

                if planning_state.move_state == MoveActionState.SUCCEEDED:
                    print(" succeeded")
                    break

                die(f"Action {action.id} {planning_state.move_state.value}")
                break

    client.disconnect()
    return App.shutdown_code()


if __name__ == "__main__":
    main()
