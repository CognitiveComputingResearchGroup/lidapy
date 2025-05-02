from threading import Thread


class ModuleSubject:
    def __init__(self):
        self.observers = []
        self.threads = {}
        self.done_threads = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            thread = Thread(target=observer.notify, args=(self,))
            thread.start()
            thread.join()