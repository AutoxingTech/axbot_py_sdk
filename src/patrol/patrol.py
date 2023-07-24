#!/usr/bin/env python3
import itertools
import sys

from axbotpy import exceptions
from axbotpy.app_framework import App, Rate
from axbotpy.client import Client
from axbotpy.planning.actions import MoveActionState

from .actions.obstacle import ACTIONS


class Progress:
    step = 0
    icons = "/-\\|/-\\|"

    def __repr__(self) -> str:
        self.step += 1
        if self.step >= len(self.icons):
            self.step = 0
        return self.icons[self.step]


class PatrolApp:
    def __init__(self) -> None:
        App.init_node("patrol_node")
        self.client = Client("http://localhost:8000")

    def run_forever(self):
        progress = Progress()

        self.client.connect()

        for action in itertools.cycle(ACTIONS):
            if not App.ok():
                break

            self.client.move(action)

            print(f"Action {action.id} {action} created")

            # wait for action to finish
            rate = Rate(4)
            while rate.ok():
                planning_state = self.client.planning_state
                if planning_state.action_id != action.id:
                    # other action, ignore
                    print(f"\r  Waiting...", end="")
                    continue

                if planning_state.move_state in [MoveActionState.IDLE, MoveActionState.MOVING]:
                    print(
                        f"\r  {planning_state.move_state.value} ... {progress}, distance = {round(planning_state.remaining_distance, 2)}"
                        + " " * 10,  # erase characters
                        end="",
                    )
                    continue

                if planning_state.move_state == MoveActionState.SUCCEEDED:
                    print(" succeeded")
                    break

                raise exceptions.AxException(f"Action {action.id} {planning_state.move_state.value}")

    def shutdown(self):
        self.client.disconnect()
        return App.shutdown_code()


def main():
    try:
        patrol = PatrolApp()
        patrol.run_forever()
    except exceptions.AxException as e:
        print(str(e))
        App.shutdown(1)
    finally:
        patrol.shutdown()
        sys.exit(App.shutdown_code())


if __name__ == "__main__":
    main()
