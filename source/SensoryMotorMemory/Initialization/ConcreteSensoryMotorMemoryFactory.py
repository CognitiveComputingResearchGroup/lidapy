from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory
from source.SensoryMotorMemory.Initialization.SensoryMotorMemoryFactory \
import SensoryMotorMemoryFactory


class ConcreteSensoryMotorMemoryFactory(SensoryMotorMemoryFactory,
                                   GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_sensory_motor(self, sensory_motor_memory):
        return sensory_motor_memory

    def add_sensory_listener(self, listener):
        pass

    def notify(self, state, percept, action):
        pass

    def send_action_execution_command(self, action_plan, percept):
        pass