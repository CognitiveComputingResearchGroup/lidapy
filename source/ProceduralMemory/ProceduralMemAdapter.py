from source.Module.ModuleObserver import ModuleObserver


class ProceduralMemAdapter(ModuleObserver):

    def __init__(self):
        super().__init__()

    def notify(self, percept, module):
        module.notify(percept)