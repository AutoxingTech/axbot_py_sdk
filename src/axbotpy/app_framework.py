import signal
import time


class App:
    """
    App framework without ROS
    """

    node_name: str = None
    __ok = True
    __shutdown_code = 0

    @staticmethod
    def init_node(node_name: str) -> None:
        App.node_name = node_name

        def handler(sig_num, _frame):
            sig_name = signal.Signals(sig_num).name
            print(f"Signal handler called with signal {sig_name} ({sig_num}) in {App.node_name}")
            App.__ok = False

        # Set the signal handler
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

    @staticmethod
    def ok() -> bool:
        return App.__ok

    @staticmethod
    def shutdown(code=0):
        App.__shutdown_code = code
        App.__ok = False

    @staticmethod
    def shutdown_code() -> int:
        return App.__shutdown_code


class Rate:
    def __init__(self, rate, timeout=None) -> None:
        self.__interval = 1.0 / rate
        now = time.time()
        self.__last_stamp = now
        if timeout == None:
            self.__timeout_stamp = None
        else:
            self.__timeout_stamp = now + timeout

    def ok(self):
        if not App.ok():
            return False

        sleep_time = self.__interval - (time.time() - self.__last_stamp)
        if sleep_time > 0:
            time.sleep(sleep_time)

        now = time.time()
        self.__last_stamp = now
        if self.__timeout_stamp != None and now >= self.__timeout_stamp:
            return False

        return True


def test_main():
    # pylint: disable=import-outside-toplevel
    import threading

    App.init_node("test_node")

    def thread_proc():
        rate = Rate(4, 2)
        while rate.ok():
            print("thread...")

    print("create thread")
    thread = threading.Thread(target=thread_proc)
    thread.start()
    thread.join()

    print("main() exit")


if __name__ == "__main__":
    test_main()
