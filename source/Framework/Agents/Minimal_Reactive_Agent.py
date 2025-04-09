import concurrent.futures
from threading import Thread
from time import sleep
from yaml import YAMLError

from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLakeEnvironment
from source.Framework.Agents.Agent import Agent
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from Configurations import Sensors, Config


class MinimalReactiveAgent(Agent):
    def __init__(self):
        super().__init__()

        # Agent modules
        self.environment = FrozenLakeEnvironment()
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = Sensors
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Module observers
        self.sensory_memory.add_observer(self.sensory_motor_mem)

        # Environment thread
        self.environment_thread = None

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.run_sensors))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.run))

        self.threads = [
            self.sensory_memory_thread,
            self.sensory_motor_mem_thread,
        ]

    def run(self):
        self.environment.add_observer(self.sensory_memory)
        self.sensory_motor_mem.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.append(self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
            executor.shutdown(wait=True)

    def start(self, worker):
        worker.start()
        sleep(5)
        worker.join()

    def notify(self, module):
        if isinstance(module, Environment):
            state = module.get_state()

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