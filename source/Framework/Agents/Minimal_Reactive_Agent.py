import concurrent.futures
from threading import Thread
from time import sleep
from yaml import YAMLError

from source.Environment.Environment import Environment
from source.Environment.FrozenLakeEnvironment import FrozenLakeEnvironment
from source.Framework.Agents.Agent import Agent
from source.MotorPlanExecution.MotorPlanExecutionImpl import \
    MotorPlanExecutionImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from Configurations import Sensors, Config


class MinimalReactiveAgent(Agent):
    def __init__(self):
        super().__init__()

        # Agent modules
        self.environment = FrozenLakeEnvironment()
        self.motor_plan_exec = MotorPlanExecutionImpl()
        self.sensory_memory = SensoryMemoryImpl()

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = Sensors
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Module observers
        self.sensory_memory.add_observer(self.motor_plan_exec)

        # Environment thread
        self.environment_thread = None

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.start))

        # MotorPlan Thread
        self.motor_plan_exec_thread = (
            Thread(target=self.motor_plan_exec.start))

        self.threads = [
            self.sensory_memory_thread,
            self.motor_plan_exec_thread,
        ]

    def run(self):
        self.environment.add_observer(self.sensory_memory)
        self.motor_plan_exec.add_observer(self.environment)
        self.environment_thread = Thread(target=self.environment.reset)
        self.threads.insert(0, self.environment_thread)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.start, self.threads)
        executor.shutdown(wait=True, cancel_futures=False)

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