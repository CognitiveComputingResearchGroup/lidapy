from abc import ABC, abstractmethod


class SensoryMemoryFactory(ABC):
    """
    Creates and returns a SensoryMemory Module
    @param sensory_memory
	        SensoryMemory properties
	    @return Constructed SensoryMemory object
    """
    @abstractmethod
    def create_sensory_memory(self, sensory_memory):
        pass

    @abstractmethod
    def run_sensors(self, state=None, col=None, row=None, agent=None):
        pass