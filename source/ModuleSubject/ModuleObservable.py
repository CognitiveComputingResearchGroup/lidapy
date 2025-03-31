import threading
from threading import Thread
from tenacity import sleep


class ModuleSubject:
    def __init__(self):
        self.observers = []
        self.observer_threads = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            thread = Thread(target=observer.notify, args=(self, ))
            self.observer_threads.append(thread)
            thread.start()
            sleep(25)
            #thread.join()
        for thread in self.observer_threads:
            if thread.is_alive():
                event = threading.Event()
                event.set()
                thread.join(15)
            #observer.notify(self)