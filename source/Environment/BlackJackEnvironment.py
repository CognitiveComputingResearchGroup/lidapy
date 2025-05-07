from threading import RLock
import gymnasium as gym

from source.Environment.Environment import Environment
from source.MotorPlanExecution.MotorPlanExecution import MotorPlanExecution


class BlackJackEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.env = gym.make('Blackjack-v1',
                            natural=False,
                            render_mode="human",
                            sab=False)
        self.args = None
        self.subscriber = None
        self.state = {}
        self.stimuli = {}
        self.id = 0
        self.sum = None
        self.dealer_show_card = None
        self.usable_ace = None
        self.done = False

    def get_state(self):
        return self.state

    # Resetting the environment to start a new episode
    def reset(self):
        state = self.env.reset()
        self.sum = state[0][0]
        self.dealer_show_card = state[0][1]
        self.usable_ace = state[0][2]
        self.state["state"] = 0
        lock = RLock()
        with lock:
            if self.sum >= 21:
                self.done = True
                self.stimuli = {"text": {"content":
                                             self.form_external_stimuli([0,1]),
                                         "id": self.id,
                                         "observation_space":
                                             self.state["state"],
                                         "action_space": [0, 1],
                                         "Reward" : 0,
                                         "position" : None}}
            else:
                self.stimuli = {"text": {"content":
                                             self.form_external_stimuli([0,1]),
                                         "id": self.id,
                                         "observation_space":
                                             self.state["state"],
                                         "action_space": [0, 1],
                                         "Reward" : 0,
                                         "position" : None}}
            self.state["done"] = self.done
        self.notify_observers()

    # perform an action in environment:
    def step(self, action):
        if self.sum < 21:
            state = self.env.step(action)
            self.sum = state[0][0]
            self.dealer_show_card = state[0][1]
            self.usable_ace = state[0][2]
        lock = RLock()
        with lock:
            self.state["state"] += 1
            if self.sum >= 21 or action == 0:
                self.state["done"] = True
                self.stimuli = {"text": {"content":
                                             self.form_external_stimuli([0,1]),
                                "id": self.id,
                                "observation_space": self.state["state"],
                                "action_space": [0, 1],
                                "Reward" : 0,
                                "position" : None}}

            else:
                self.stimuli = {"text": {"content":
                                             self.form_external_stimuli([0,1]),
                                         "id": self.id,
                                         "observation_space":
                                             self.state["state"],
                                         "action_space": [0, 1],
                                         "Reward" : 0,
                                         "position" : None}}
        self.notify_observers()

    # close the environment:
    def close(self):
        self.env.close()

    def form_external_stimuli(self, action_space):
        for action in action_space:
            if action == 0:
                return "stick"
            else:
                return "hold"

    def get_stimuli(self):
        return self.stimuli

    def get_position(self):
        pass

    def notify(self, module):
        if isinstance(module, MotorPlanExecution):
            actions = module.send_motor_plan()
            if actions and not self.state["done"]:
                if isinstance(actions, list):
                    for action in actions:
                        self.step(action)
                else:
                    self.step(actions)
            else:
                self.reset()
