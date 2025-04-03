import importlib
import multiprocessing
from importlib import util
from multiprocessing import Process
from threading import Thread
from yaml import YAMLError, safe_load

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

        # Agent modules
        self.environment = FrozenLake()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Module observers
        self.sensory_motor_mem.add_observer(self.environment)
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.environment.add_observer(self.sensory_memory)
        self.pam.add_observer(self.procedural_memory)
        self.procedural_memory.add_observer(self.action_selection)
        self.sensory_memory.add_observer(self.pam)

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_sensors_from_file("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        # Environment thread
        self.environment_thread = Thread(target=self.environment.reset)

        # Sensory memory process
        self.sensory_memory_process = (
            Process(target=self.sensory_memory.run_sensors,
                    args=(self.sensory_memory,)))

        # PAM process
        self.pam_process = Process(target=self.pam.run, args=(self.pam,))

        # ProceduralMem process
        self.procedural_memory_process = (
            Process(target=self.procedural_memory.run,
                    args=(
                        self.procedural_memory, ["Avoid hole", "Find goal"])))

        # ActionSelection process
        self.action_selection_process = (
            Process(target=self.action_selection.run))

        # SensoryMotorMem process
        self.sensory_motor_mem_process = (
            Process(target=self.sensory_motor_mem.run))

    def run(self):
        multiprocessing.set_start_method("spawn")
        self.environment_thread.start()
        self.environment_thread.join()
        self.sensory_memory_process.start()
        self.sensory_memory_process.join()
        self.pam_process.start()
        self.pam_process.join()
        self.procedural_memory_process.start()
        self.procedural_memory_process.join()
        """self.action_selection_process.start()
        self.action_selection_process.join()"""
        self.sensory_motor_mem_process.start()
        self.sensory_motor_mem_process.join()

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

        # Specify the module file path
        try:
            module_path = loaded_module_locations[type]
        except:
            raise KeyError(f"Invalid key \"{type}\"")
        # Name the module
        module_name = type

        # Load the module dynamically
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