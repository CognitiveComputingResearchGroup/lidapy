import concurrent.futures
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
            thread = Thread(target = observer.notify, args=(self,))
            self.observer_threads.append(thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.update, self.observer_threads)

    def update(self, worker):
        worker.start()
        sleep(5)
        worker.join()


