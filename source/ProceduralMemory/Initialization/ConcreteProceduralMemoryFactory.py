from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory
from source.ProceduralMemory.Initialization.ProceduralMemoryFactory import \
    ProceduralMemoryFactory


class ConcreteProceduralMemoryFactory(ProceduralMemoryFactory,
                                      GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_procedural_memory(self, procedural_memory):
        return procedural_memory

    def add_scheme(self, percept, action):
        pass

    def get_action(self, percept):
        pass

    def notify(self, percept):
        pass
