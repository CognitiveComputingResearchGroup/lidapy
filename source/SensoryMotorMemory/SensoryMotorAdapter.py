from source.Module.ModuleObserver import ModuleObserver


class SensoryMotorAdapter(ModuleObserver):
    def __init__(self):
        super().__init__()

    def notify(self, state, module):
        pass

    def notify_(self, state, module, percept, action):
        module.notify(state, percept, action)