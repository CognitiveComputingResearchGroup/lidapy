import threading
from threading import Thread
from time import sleep


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
            observer.notify(self)
            thread = Thread(target=observer.notify, args=(self,))
            self.observer_threads.append(thread)
            thread.name = observer.__class__.__name__
            thread.start()
            sleep(5)
            #thread.join()
        for thread in self.observer_threads:
            event = threading.Event()
            event.set()
            thread.join(15)
