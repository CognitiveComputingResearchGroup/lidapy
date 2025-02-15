from abc import ABC, abstractmethod


class ProceduralMemoryFactory(ABC):
    """
    Creates and returns a ProceduralMemory Module
    @:parameter procedural_memory
            ProceduralMemory properties
    @:return ProceduralMemory
            Constructed ProceduralMemory Object
    """

    @abstractmethod
    def create_procedural_memory(self, procedural_memory):
        pass

    @abstractmethod
    def add_scheme(self, percept, action):
        pass

    @abstractmethod
    def get_action(self, percept):
        pass

    @abstractmethod
    def notify(self, percept):
        pass