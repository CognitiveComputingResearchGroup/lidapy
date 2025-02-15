from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory
from source.SensoryMemory.Initialization.SensoryMemoryFactory import \
    SensoryMemoryFactory

class ConcreteSensoryMemoryFactory(SensoryMemoryFactory, GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_sensory_memory(self, sensory_memory):
        return sensory_memory

    def run_sensors(self, state=None, col=None, row=None, agent=None):
        pass

