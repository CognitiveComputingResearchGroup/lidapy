from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl


class MinimalReactiveAgent(Agent):
    def __init__(self):
        super().__init__()
        self.environment = FrozenLake(self)
        self.sensory_motor_mem = SensoryMotorMemoryImpl(self.environment)
        self.sensory_memory = SensoryMemoryImpl(self.environment, None,
                                                self.sensory_motor_mem)

        #Add observers
        self.add_observer(self.sensory_memory)

    def run(self):
        self.environment.reset()

    def notify(self, module):
        if isinstance(module, Environment):
            self.notify_observers()

    def get_state(self):
        return self.environment.get_state()