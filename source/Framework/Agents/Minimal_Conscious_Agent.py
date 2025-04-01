import importlib
import time
from importlib import util
from threading import Thread
from yaml import YAMLError, safe_load

from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.AttentionCodelets.AttentionCodeletImpl import AttentionCodeletImpl
from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
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

        #Agent modules
        self.global_workspace = GlobalWorkSpaceImpl()
        self.csm = CurrentSituationalModelImpl()
        self.attention_codelets = AttentionCodeletImpl()
        self.environment = FrozenLake()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.workspace = WorkspaceImpl()
        self.sensory_memory = SensoryMemoryImpl()

        #Module observers
        self.sensory_motor_mem.add_observer(self.environment)
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.environment.add_observer(self.sensory_memory)
        self.attention_codelets.add_observer(self.csm)
        self.pam.add_observer(self.procedural_memory)
        self.pam.add_observer(self.workspace)
        self.procedural_memory.add_observer(self.action_selection)
        self.workspace.add_observer(self.pam)
        self.workspace.add_observer(self.global_workspace)
        self.sensory_memory.add_observer(self.pam)
        self.sensory_memory.add_observer(self.csm)
        self.sensory_memory.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.pam)
        self.global_workspace.add_observer(self.procedural_memory)
        self.global_workspace.add_observer(self.action_selection)
        self.global_workspace.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.attention_codelets)
        self.csm.add_observer(self.global_workspace)

        #Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_sensors_from_file("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        #Add procedural_mem schemes
        self.procedural_memory.scheme = ["Stay safe", "Seek goal"]

        #Add workspace csm
        self.workspace.csm = self.csm

        #Add attention codelets buffer
        self.attention_codelets.buffer = self.csm

        #Agent thread
        self.agent_thread = Thread(target=self.environment.reset)

        # Attention codelets thread
        self.attention_codelets_thread = Thread(
            target=self.attention_codelets.run_task)

        self.pam_thread = Thread(target=self.pam.run)

        #Sensory memory thread
        self.sensory_memory_thread = (
                        Thread(target=self.sensory_memory.run_sensors))

        #CSM thread
        self.csm_thread = Thread(target=self.csm.run_task)

        #GlobalWorkspace thread
        self.global_workspace_thread = (
                        Thread(target=self.global_workspace.run_task))

        #ProceduralMem thread
        self.procedural_memory_thread = (
            Thread(target=self.procedural_memory.run,
                   args=((["Avoid hole", "Find goal"]), )))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.run))


    def run(self):
        self.agent_thread.start()
        self.sensory_memory_thread.start()
        self.pam_thread.start()
        self.csm_thread.start()
        self.attention_codelets_thread.daemon = True
        self.attention_codelets_thread.start()
        self.global_workspace_thread.daemon = True
        self.global_workspace_thread.start()
        self.procedural_memory_thread.start()
        self.sensory_motor_mem_thread.start()

    def notify(self, module):
        if isinstance(module, Environment):
            state = module.get_state()

    def load_sensors_from_file(self, type):
        with open(
                r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\module_locations.yaml', 'r') as yaml_file:
            try:
                loaded_module_locations = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)

        #Specify the module file path
        try:
            module_path = loaded_module_locations[type]
        except:
            raise KeyError(f"Invalid key \"{type}\"")
        #Name the module
        module_name = type

        #Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_agent_sensors(self):
        with open(r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\DEFAULT_PROCESSORS.yaml', 'r') as yaml_file:
            try:
                DEFAULT_SENSORS = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)
        return DEFAULT_SENSORS

    def get_agent_processors(self):
        with open(r'C:\Users\brian\Documents\Fall 2024\SWENG 480\lidapy'
                r'\Configs\DEFAULT_PROCESSORS.yaml', 'r') as yaml_file:
            try:
                DEFAULT_PROCESSORS = safe_load(yaml_file)
            except YAMLError as exc:
                print(exc)
        return DEFAULT_PROCESSORS

    def __getstate__(self):
        return self.environment.get_stimuli()