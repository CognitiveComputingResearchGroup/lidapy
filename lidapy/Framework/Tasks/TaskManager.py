from threading import Lock, RLock
from time import sleep

from Module.Initialization.DefaultLogger import getLogger


class TaskManager:
    def __init__(self):
        self.tick = 0
        self.name = ""
        self.shutdown = False
        self.logger = getLogger(__class__.__name__).logger

    def run(self):
        self.logger.name = __class__.__name__ +  f" ({self.name})"
        self.logger.debug("Initializing Task Manager")
        while not self.shutdown:
            lock = RLock()
            with lock:
                self.tick += 3
            sleep(3)

    def getCurrentTick(self):
        return self.tick

    def get_shutdown(self):
        return self.shutdown

    def set_shutdown(self, state):
        self.shutdown = state