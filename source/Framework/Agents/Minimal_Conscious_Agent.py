import concurrent.futures
from threading import Thread
from time import sleep

from yaml import YAMLError

from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.AttentionCodelets.AttentionCodeletImpl import AttentionCodeletImpl
from source.Environment.Environment import Environment
from source.Framework.Agents.Agent import Agent
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from source.Workspace.CurrentSituationalModel.CurrentSituationalModelImpl import \
    CurrentSituationalModelImpl
from source.Workspace.WorkspaceImpl import WorkspaceImpl
from Configurations import Sensors, Config


class MinimalConsciousAgent(Agent):
    def __init__(self):
        super().__init__()

        #Agent modules
        self.environment = None
        self.global_workspace = GlobalWorkSpaceImpl()
        self.csm = CurrentSituationalModelImpl()
        self.attention_codelets = AttentionCodeletImpl()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.workspace = WorkspaceImpl()
        self.sensory_memory = SensoryMemoryImpl()

        #Module observers
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.attention_codelets.add_observer(self.csm)
        self.pam.add_observer(self.procedural_memory)
        self.pam.add_observer(self.workspace)
        self.procedural_memory.add_observer(self.action_selection)
        self.workspace.add_observer(self.pam)
        self.sensory_memory.add_observer(self.csm)
        self.sensory_memory.add_observer(self.pam)
        self.sensory_memory.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.pam)
        self.global_workspace.add_observer(self.procedural_memory)
        self.global_workspace.add_observer(self.action_selection)
        self.global_workspace.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.attention_codelets)
        self.csm.add_observer(self.global_workspace)

        #Global Workspace Ticks
        self.global_workspace.ticks = 0

        #Add workspace csm
        self.workspace.csm = self.csm

        #Add attention codelets buffer
        self.attention_codelets.buffer = self.csm

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        #Environment thread
        self.environment_thread = None

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = Sensors
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Sensory memory thread
        self.sensory_memory_thread = (
        Thread(target=self.sensory_memory.start))

        # PAM thread
        self.pam_thread = Thread(target=self.pam.run)

        # Workspace thread
        self.workspace_thread = Thread(target=self.workspace.run)

        # CSM thread
        self.csm_thread = Thread(target=self.csm.run_task)

        # Attention codelets thread
        self.attention_codelets_thread = Thread(
            target=self.attention_codelets.start)

        # GlobalWorkspace thread
        self.global_workspace_thread = (
            Thread(target=self.global_workspace.run_task))

        # ProceduralMem thread
        self.procedural_memory_thread = (
            Thread(target=self.procedural_memory.run,
                    args=(["Avoid hole", "Find goal"],)))

        # ActionSelection thread
        self.action_selection_thread = (
            Thread(target=self.action_selection.run))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.run))

        self.threads = [
            self.sensory_memory_thread,
            self.csm_thread,
            self.attention_codelets_thread,
            self.pam_thread,
            self.workspace_thread,
            self.global_workspace_thread,
            self.procedural_memory_thread,
            self.action_selection_thread,
            self.sensory_motor_mem_thread,
        ]


    def run(self):
        self.environment.add_observer(self.sensory_memory)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.insert(0, self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
            executor.shutdown(wait=True, cancel_futures=False)

        if self.get_state()["done"]:
            self.global_workspace.task_manager.set_shutdown(True)
            self.attention_codelets.shutdown = True

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            stimuli = module.get_stimuli()

    def get_agent_sensors(self):
        try:
            DEFAULT_SENSORS = Config.DEFAULT_SENSORS
            return DEFAULT_SENSORS
        except YAMLError as exc:
            print(exc)

    def get_agent_processors(self):
        try:
            DEFAULT_PROCESSORS = Config.DEFAULT_PROCESSORS
            return DEFAULT_PROCESSORS
        except YAMLError as exc:
            print(exc)

    def get_state(self):
        return self.environment.get_state()