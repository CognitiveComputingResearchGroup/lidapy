import concurrent.futures


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
            with (concurrent.futures.ThreadPoolExecutor(max_workers=5) as
                  executor):
                executor.submit(observer.notify, self)

