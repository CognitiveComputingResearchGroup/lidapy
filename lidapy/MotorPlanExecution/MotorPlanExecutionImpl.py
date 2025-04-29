import random
from time import sleep

from Framework.Shared.NodeImpl import NodeImpl
from Module.Initialization.DefaultLogger import getLogger
from MotorPlanExecution.MotorPlanExecution import MotorPlanExecution
from SensoryMemory.SensoryMemory import SensoryMemory
from SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory



class MotorPlanExecutionImpl(MotorPlanExecution):
    def __init__(self):
        super().__init__()
        self.motor_plans = {}
        self.state = None
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized Motor Plan Execution")

    def start(self):
        pass

    def send_motor_plan(self):
        if self.motor_plans and self.state in self.motor_plans:
            motor_plans = self.motor_plans[self.state]
            return random.choice(motor_plans)

    def send_motor_plans(self):
        return self.motor_plans[self.state]

    def receive_motor_plan(self, state, motor_plan):
        if not self.motor_plans or state not in self.motor_plans:
            self.motor_plans[state] = []
            self.motor_plans[state].append(motor_plan)
        else:
            if motor_plan not in self.motor_plans[state]:
                self.motor_plans[state].append(motor_plan)

    def receive_motor_plans(self, state, motor_plans):
        for motor_plan in motor_plans:
            self.receive_motor_plan(state, motor_plan)


    def notify(self, module):
        if isinstance(module, SensoryMemory):
            cue = module.get_sensory_content(module)["cue"]
            source = NodeImpl()
            state = (module.get_sensory_content(module)["params"]["state"]
            ["state"])
            source.setId(state)
            for link in cue:
                if link.getCategory("label") != "hole":
                    source = link.getSource()
                    if source is not None and isinstance(source, NodeImpl):
                        self.state = source
                        self.receive_motor_plan(source, link.getCategory("id"))
                    else:
                        self.state = source
                        self.receive_motor_plan(source, link.getCategory("id"))
            sleep(0.1)
            self.notify_observers()

        elif isinstance(module, SensoryMotorMemory):
            state = module.get_state()
            self.state = state
            motor_plan = module.send_action_execution_command()
            if len(motor_plan) > 1:
                for action in motor_plan:
                    for key, value in action.items():
                        self.receive_motor_plan(state, value)
            elif len(motor_plan) == 1:
                for key, value in motor_plan[0].items():
                    self.receive_motor_plan(state, value)
            self.notify_observers()