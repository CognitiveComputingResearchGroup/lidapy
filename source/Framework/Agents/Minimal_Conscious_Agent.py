from threading import Thread
from time import sleep

from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.AttentionCodelets.AttentionCodeletImpl import AttentionCodeletImpl
from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
from source.Framework.Shared.NodeStructure import NodeStructure
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from source.Workspace.CurrentSituationModel.CurrentSituationModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl


class MinimalConsciousAgent(Agent):
    def __init__(self):
        super().__init__()
        self.environment = FrozenLake(self)
        self.sensory_motor_mem = SensoryMotorMemoryImpl(self.environment)
        self.action_selection = ActionSelectionImpl(self.sensory_motor_mem)
        self.procedural_memory = ProceduralMemoryImpl(self.action_selection,
                                                      self.environment)
        self.pam = PAMImpl(self.procedural_memory)
        self.global_workspace = GlobalWorkSpaceImpl()
        self.csm = CurrentSituationalModelImpl()
        self.workspace = WorkspaceImpl(self.csm, self.pam)
        self.attention_codelets = AttentionCodeletImpl(self.csm,
                                                       self.global_workspace)
        self.sensory_memory = SensoryMemoryImpl(None,self.pam,
                                                None,
                                                self.workspace)

        #Add observers
        self.add_observer(self.sensory_memory)
        self.agent_thread = Thread(target=self.environment.reset)
        self.attention_codelets_thread = (
                            Thread(target=self.attention_codelets.run_task))

    def run(self):
        self.agent_thread.start()
        sought_content = NodeStructure()
        sought_content.addNode("safe", 1.0, 0.0)
        sought_content.addNode("start", 1.0, 0.0)
        sought_content.addNode("goal", 2.0, -1.0)
        sought_content.addNode("danger", -1.0, 0.5)
        self.attention_codelets.setSoughtContent(NodeStructure())
        self.attention_codelets_thread.start()

    def notify(self, module):
        if isinstance(module, Environment):
            self.notify_observers()

    def get_module_content(self):
        return self.attention_codelets_thread

    def get_state(self):
        return self.environment.get_state()