import concurrent.futures
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
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(observer.notify, self)
                sleep(0.5)

            """thread = Thread(target=observer.notify, args=(self,))
            with threading.Lock():
                thread.name = observer.__class__.__name__
                self.observer_threads.append(thread)
            thread.start()
            sleep(25)
        for thread in self.observer_threads:
            event = threading.Event()
            event.set()
            thread.join()"""

