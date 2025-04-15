from source.Module.Initialization.ModuleInterface import Module


class MotorPlanExecution(Module):
    def __init__(self):
        super().__init__()

    def send_motor_plan(self):
        pass

    def send_motor_plans(self):
        pass

    def receive_motor_plan(self, state, motor_plan):
        pass

    def receive_motor_plans(self, state, motor_plan):
        pass

    def notify(self, module):
        pass
