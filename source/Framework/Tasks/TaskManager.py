from threading import Lock
from time import sleep

from source.Module.Initialization.DefaultLogger import getLogger


class TaskManager:
    def __init__(self):
        self.tick = 0
        self.name = ""
        self.shutdown_manager = None
        self.shutdown = False
        self.logger = None

    def run(self):
        self.logger = getLogger(__class__.__name__ + f" ({self.name})").logger
        self.logger.debug("Initializing Task Manager")
        while not self.shutdown:
            lock = Lock()
            lock.acquire()
            self.tick += 3
            lock.release()
            sleep(3)

    def getCurrentTick(self):
        return self.tick

    def get_shutdown(self):
        return self.shutdown

    def set_shutdown(self, state):
        self.shutdown = state