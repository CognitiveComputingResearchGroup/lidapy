from source.Environment.Environment import Environment
from source.Module.Initialization.DefaultLogger import getLogger
from source.MotorPlanExecution.MotorPlanExecutionImpl import \
    MotorPlanExecutionImpl
from source.Sockets.Subscriber import Subscriber

# maps single character user inputs from command line to Godot agent actions
ACTION_MAP = {'W': 'up',
              'S': 'down',
              'A': 'left',
              'D': 'right',
              'Q': 'rotate_counterclockwise',
              'E': 'rotate_clockwise'}

class GodotEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.done = False
        self.subscriber = None
        self.publisher = None
        self.connection = None
        self.stimuli = None
        self.col = 0
        self.row = 0
        self.position = {"row": self.row, "col": self.col}
        self.state = None
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug("Initialized Godot Environment")


    def get_state(self):
        return self.state

    def notify(self, module):
        if isinstance(module, MotorPlanExecutionImpl):
            action = module.send_action_request()
            if isinstance(action, list):
                for value in action:
                    self.step(value)
            else:
                self.step(action)

    def reset(self):
        try:
            if self.connection is None:
                self.subscriber = Subscriber()
                self.connection = self.subscriber.connection

            state = self.subscriber.receive(self.connection)[1]
            self.state = {"content" : state["data"]["content"],
                          "id" : state["data"]["id"],
                        "position": state["data"]["position"],
                          "rotation (degrees)":
                              state["data"]["rotation_in_degrees"],
                          "seqno": state["header"]["seqno"],
                          "done": False}

            self.logger.debug(self.state)
            self.notify_observers()

        except Exception as e:
            print(e)

    def step(self, action):
        state = self.subscriber.receive(self.connection)[1]
        self.state = {"content" : state["data"]["content"],
                      "id": state["data"]["id"],
                      "position": state["data"]["position"],
                      "rotation (degrees)":
                          state["data"]["rotation_in_degrees"],
                      "seqno": state["header"]["seqno"],
                      "done": False}
        self.steps += 1
        if action:
            self.update_position(action)
        self.logger.debug(self.state)
        self.notify_observers()

    def update_position(self, action):
        if action == 'W':  # up
            self.row = max(self.row - 1, 0)
        elif action == "D":  # Right
            self.col = self.col + 1
        elif action == 'S':  # down
            self.row = self.row + 1
        elif action == 'A':  # Left
            self.col = max(self.col - 1, 0)

    def get_position(self):
        return self.position

    def get_stimuli(self):
        return {"text" : {"content" : self.state["content"],
         "id" : self.state["id"], "position" : self.state["position"]}}