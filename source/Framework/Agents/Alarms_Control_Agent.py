from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl


class AlarmsControlAgent(Agent):
    def __init__(self):
        super().__init__()
        self.environment = FrozenLake(self)
        self.sensory_motor_mem = SensoryMotorMemoryImpl(self.environment)
        self.action_selection = ActionSelectionImpl(self.sensory_motor_mem)
        self.procedural_memory = ProceduralMemoryImpl(self.action_selection,
                                                      self.environment)
        self.pam = PAMImpl(self.procedural_memory)
        self.sensory_memory = SensoryMemoryImpl(None,self.pam,
                                                None)

        #Add observers
        self.add_observer(self.sensory_memory)

    def run(self):
        self.environment.reset()

    def notify(self, module):
        if isinstance(module, Environment):
            self.notify_observers()

    def get_state(self):
        return self.environment.get_state()