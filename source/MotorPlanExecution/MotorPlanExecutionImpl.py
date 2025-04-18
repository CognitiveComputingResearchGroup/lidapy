import random

from source.Module.Initialization.DefaultLogger import getLogger
from source.MotorPlanExecution.MotorPlanExecution import MotorPlanExecution
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory
from src.Framework.Shared.NodeImpl import NodeImpl


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
            for link in cue:
                if link.getCategory("label") != "H":
                    source = link.getSource()
                    if source is not None and isinstance(source, NodeImpl):
                        self.receive_motor_plan(source,
                                    {link.getCategory("label"):
                                                link.getCategory("id")})

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