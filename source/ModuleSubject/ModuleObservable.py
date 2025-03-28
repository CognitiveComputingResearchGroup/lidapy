

class ModuleSubject:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)
    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        index = 0
        for observer in self.observers:
            observer.notify(self)