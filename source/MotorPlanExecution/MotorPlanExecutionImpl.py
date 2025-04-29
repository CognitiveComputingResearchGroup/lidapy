import random
from time import sleep

from source.Framework.Shared.NodeImpl import NodeImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.MotorPlanExecution.MotorPlanExecution import MotorPlanExecution
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMotorMemory.SensoryMotorMemory import SensoryMotorMemory
from source.Sockets.Publisher import Publisher


class MotorPlanExecutionImpl(MotorPlanExecution):
    def __init__(self):
        super().__init__()
        self.motor_plans = {}
        self.state = None
        self.publisher = None
        self.connection = None
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
            if len(motor_plan) >= 1:
                for action in motor_plan:
                    self.receive_motor_plan(state, action)
            else:
                self.receive_motor_plan(state, motor_plan)
            self.notify_observers()

    def send_action_request(self):
        action = random.choice(list(self.publisher.action_map.keys()))
        request = self.publisher.create_request(data={'event':
                                {'type': 'action',
                                'agent': self.publisher.id,
                                'value': self.publisher.action_map[action]}
                                })
        self.connection = self.publisher.connection
        reply = self.publisher.send(self.connection, request)
        return action