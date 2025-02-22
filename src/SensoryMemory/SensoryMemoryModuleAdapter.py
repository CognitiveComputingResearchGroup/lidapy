from src.ModuleObserver.ModuleObserver import ModuleObserver
from src.SensoryMemory import SensoryMemory as SensoryMem
from src.SensoryMemory.SensoryMemory import SensoryMemory


class SensoryMemoryModuleAdapter(ModuleObserver):

    def __init__(self):
        super().__init__()
        self.sensoryMemory = SensoryMemory()

    def notify(self, state):
        SensoryMem.SensoryMemory.notify(self.sensoryMemory, state)

