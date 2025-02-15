from abc import ABC, abstractmethod

class SensoryMotorMemoryFactory(ABC):

    @abstractmethod
    def create_sensory_motor(self, sensory_motor_memory):
        pass

    @abstractmethod
    def add_sensory_listener(self, listener):
        pass
    @abstractmethod
    def notify(self, state, percept, action):
        pass
    @abstractmethod
    def send_action_execution_command(self, action_plan, percept):
        pass