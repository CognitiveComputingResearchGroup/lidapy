import concurrent.futures
from threading import Thread
from time import sleep
from yaml import YAMLError

from ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from Environment.Environment import Environment
from Framework.Agents.Agent import Agent
from MotorPlanExecution.MotorPlanExecutionImpl import \
    MotorPlanExecutionImpl
from PAM.PAM_Impl import PAMImpl
from ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl
from Configurations import Sensors, Config


class AlarmsControlAgent(Agent):
    def __init__(self):
        super().__init__()

        # Agent modules
        self.environment = None
        self.sensory_motor_mem = SensoryMotorMemoryImpl()
        self.action_selection = ActionSelectionImpl()
        self.procedural_memory = ProceduralMemoryImpl()
        self.pam = PAMImpl()
        self.sensory_memory = SensoryMemoryImpl()
        self.motor_plan_exec = MotorPlanExecutionImpl()

        # Module observers
        self.action_selection.add_observer(self.sensory_motor_mem)
        self.pam.add_observer(self.procedural_memory)
        self.procedural_memory.add_observer(self.action_selection)
        self.sensory_memory.add_observer(self.pam)
        self.sensory_memory.add_observer(self.motor_plan_exec)
        self.sensory_motor_mem.add_observer(self.motor_plan_exec)

        # Sensory Memory Sensors
        self.sensory_memory.sensor_dict = self.get_agent_sensors()
        self.sensory_memory.sensor = Sensors
        self.sensory_memory.processor_dict = self.get_agent_processors()

        # Add procedural memory schemes
        self.procedural_memory.scheme = ["Avoid hole", "Find goal"]

        # Environment thread
        self.environment_thread = None

        # Sensory memory thread
        self.sensory_memory_thread = (
            Thread(target=self.sensory_memory.start))

        # PAM thread
        self.pam_thread = Thread(target=self.pam.start)

        # ProceduralMem thread
        self.procedural_memory_thread = (
            Thread(target=self.procedural_memory.start,
                   args=(["Avoid hole", "Find goal"],)))

        # ActionSelection thread
        self.action_selection_thread = (
            Thread(target=self.action_selection.start))

        # SensoryMotorMem thread
        self.sensory_motor_mem_thread = (
            Thread(target=self.sensory_motor_mem.start))

        # MotorPlan Thread
        self.motor_plan_exec_thread = (
            Thread(target=self.motor_plan_exec.start))

        self.threads = [
            self.sensory_memory_thread,
            self.pam_thread,
            self.procedural_memory_thread,
            self.action_selection_thread,
            self.sensory_motor_mem_thread,
            self.motor_plan_exec_thread
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
        sleep(3)
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