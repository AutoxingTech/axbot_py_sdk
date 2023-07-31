#!/usr/bin/env python3
import argparse
import itertools
import sys

from app_framework import App, Rate
from axbotpy import exceptions
from axbotpy.client import Client
from axbotpy.planning.actions import MoveActionState

from .actions.obstacle import ACTIONS


class ProgressIndicator:
    step = 0
    icons = "/-\\|/-\\|"

    def __repr__(self) -> str:
        self.step += 1
        if self.step >= len(self.icons):
            self.step = 0
        return self.icons[self.step]


class Patrol:
    """
    Move the robot with predefined actions
    """

    def __init__(self, base_url: str) -> None:
        App.init_node("patrol_node")
        self.__client = Client(base_url=base_url)

    def run_forever(self):
        progress = ProgressIndicator()

        self.__client.connect()

        for action in itertools.cycle(ACTIONS):
            if not App.ok():
                break

            # make move action
            self.__client.move(action)
            print(f"Action {action.id} {action} created")

            # wait for action to finish
            rate = Rate(4)
            while rate.ok():
                planning_state = self.__client.planning_state
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
        self.__client.disconnect()


class Options:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", default="http://localhost:8000")

        args = parser.parse_args()

        self.url = args.url


def main():
    opts = Options()

    try:
        patrol = Patrol(opts.url)
        patrol.run_forever()
    except exceptions.AxException as e:
        print(str(e))
        App.shutdown(1)
    finally:
        patrol.shutdown()
        sys.exit(App.shutdown_code())


if __name__ == "__main__":
    main()
