import concurrent.futures
import importlib
import multiprocessing
import sys
from importlib import util
from threading import Thread
from time import sleep
from yaml import YAMLError, safe_load

from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.Environment.Environment import Environment
from source.Framework.Agents.Agent import Agent
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl


class AlarmsControlAgent(Agent):
    def __init__(self):
        super().__init__()
        self.environment_type = None

        # Agent modules
        self.environment = None
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Module observers
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.pam.add_observer(self.procedural_memory)
        self.procedural_memory.add_observer(self.action_selection)
        self.sensory_memory.add_observer(self.pam)

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_from_file("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        # Environment thread
        self.environment_thread = None

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.start))

        # PAM thread
        self.pam_thread = Thread(target=self.pam.run)

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
            self.pam_thread,
            self.procedural_memory_thread,
            self.action_selection_thread,
            self.sensory_motor_mem_thread,
        ]

    def run(self):
        # Initialize environment dynamically
        self.environment = self.load_from_file(self.environment_type)

        if self.environment_type == "FrozenLakeEnvironment":
            self.environment_type = "FrozenLake"

        self.environment = self.environment.__getattribute__(
            self.environment_type)()
        self.environment.add_observer(self.sensory_memory)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.append(self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
            executor.shutdown(wait=True)

        if self.get_state()["done"]:
            sys.exit(0)

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            stimuli = module.get_stimuli()

    def load_from_file(self, type):
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