import importlib
import multiprocessing
from importlib import util
from multiprocessing import Process
from threading import Thread
from yaml import YAMLError, safe_load

from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Agent import Agent
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl


class MinimalReactiveAgent(Agent):
    def __init__(self):
        super().__init__()

        # Agent modules
        self.environment = FrozenLake()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Module observers
        self.sensory_memory.add_observer(self.sensory_motor_mem)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment.add_observer(self.sensory_memory)

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = self.load_sensors_from_file("Sensors")
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Environment thread
        self.environment_thread = Thread(target=self.environment.reset)

        # Sensory memory thread
        self.sensory_memory_process = (
            Process(target=self.sensory_memory.run_sensors))

        # SensoryMotorMem process
        self.sensory_motor_mem_process = (
            Process(target=self.sensory_motor_mem.run))

    def run(self):
        multiprocessing.set_start_method("spawn")
        self.environment_thread.start()
        self.environment_thread.join()
        self.sensory_memory_process.start()
        self.sensory_motor_mem_process.join()
        self.sensory_motor_mem_process.start()
        self.sensory_motor_mem_process.join()

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
        return self.environment.get_stimuli()