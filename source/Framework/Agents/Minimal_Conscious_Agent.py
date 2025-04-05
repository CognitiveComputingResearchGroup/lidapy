import concurrent.futures
import importlib
import multiprocessing
from importlib import util
from multiprocessing import Process
from threading import Thread
from time import sleep

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
        self.sensory_memory.add_observer(self.csm)
        self.sensory_memory.add_observer(self.pam)
        self.sensory_memory.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.procedural_memory)
        self.global_workspace.add_observer(self.pam)
        self.global_workspace.add_observer(self.action_selection)
        self.global_workspace.add_observer(self.sensory_motor_mem)
        self.global_workspace.add_observer(self.attention_codelets)
        self.csm.add_observer(self.global_workspace)

        #Global Workspace Ticks
        self.global_workspace.ticks = 0

        #Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_sensors_from_file("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        #Add workspace csm
        self.workspace.csm = self.csm

        #Add attention codelets buffer
        self.attention_codelets.buffer = self.csm

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        #Environment thread
        self.environment_thread = Thread(target=self.environment.reset)

        # Sensory memory process
        self.sensory_memory_process = (
            Thread(target=self.sensory_memory.run_sensors))

        # PAM process
        self.pam_process = Thread(target=self.pam.run)

        # Workspace thread
        self.workspace_process = Thread(target=self.workspace.run)

        # CSM thread
        self.csm_thread = Thread(target=self.csm.run_task)

        # Attention codelets thread
        self.attention_codelets_thread = Thread(
            target=self.attention_codelets.start)

        # GlobalWorkspace process
        self.global_workspace_process = (
            Thread(target=self.global_workspace.run_task))

        # ProceduralMem process
        self.procedural_memory_process = (
            Thread(target=self.procedural_memory.run,
                    args=(["Avoid hole", "Find goal"],)))

        # ActionSelection process
        self.action_selection_process = (
            Thread(target=self.action_selection.run))

        # SensoryMotorMem process
        self.sensory_motor_mem_process = (
            Thread(target=self.sensory_motor_mem.run))

        """self.processes = [
            self.sensory_memory_process,
            self.pam_process,
            self.workspace_process,
            self.global_workspace_process,
            self.procedural_memory_process,
            self.action_selection_process,
            self.sensory_motor_mem_process
        ]"""
        self.threads = [
            self.environment_thread,
            self.sensory_memory_process,
            self.csm_thread,
            self.attention_codelets_thread,
            self.pam_process,
            self.workspace_process,
            self.global_workspace_process,
            self.procedural_memory_process,
            self.action_selection_process,
            self.sensory_motor_mem_process
        ]


    def run(self):
        multiprocessing.set_start_method("spawn")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)

        """self.environment_thread.start()
        self.environment_thread.join()
        self.sensory_memory_process.start()
        self.sensory_memory_process.join()
        self.pam_process.start()
        self.pam_process.join()
        self.csm_thread.start()
        self.csm_thread.join()
        self.workspace_process.start()
        self.workspace_process.join()
        self.attention_codelets_thread.start()
        self.attention_codelets_thread.join()
        self.global_workspace_process.start()
        self.global_workspace_process.join()
        self.procedural_memory_process.start()
        self.procedural_memory_process.join()
        self.action_selection_process.start()
        self.action_selection_process.join()
        self.sensory_motor_mem_process.start()
        self.sensory_motor_mem_process.join()"""

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            stimuli = module.get_stimuli()

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
        return self.environment.__getstate__()