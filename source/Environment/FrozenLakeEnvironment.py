#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
The environment is essential for receiving, processing, and
integrating all sensory information, enabling the agent to interact
effectively.
Sends Sensory information to the Sensory Memory.
"""

from multiprocessing import Process
from threading import RLock, Thread, current_thread, main_thread

import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map


from source.Environment.Environment import Environment
from source.MotorPlanExecution.MotorPlanExecution import MotorPlanExecution

ActionMap = {
        "up": 3,
        "right": 2,
        "down" : 1,
        "left" : 0
}

class FrozenLakeEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.env = gym.make('FrozenLake-v1',
                            desc=generate_random_map(size=4),
                            is_slippery=False,
                            render_mode="human")
        self.args = None
        self.subscriber = None
        self.action_space = ActionMap
        self.observation_space = None
        self.reward= 0
        self.done = False
        self.text_stimuli = {}
        self.vision_stimuli = {}
        self.state = {}
        self.row = 0
        self.col = 0
        self.id = 0
        self.shutdown = False

    def get_state(self):
        return self.state

    # Resetting the environment to start a new episode
    def reset(self):
        lock = RLock()
        with lock:
            self.observation_space = self.env.reset()[0]
            self.state["state"] = self.observation_space
            self.state["done"] = False
            surrounding_tiles = self.get_surrounding_tiles(self.row,
                                                       self.col)
            self.text_stimuli = {"text": { "content" :
                                self.form_external_stimuli(surrounding_tiles),
                                "id" : self.id,
                                "observation_space" :  self.observation_space,
                                "action_space": self.action_space,
                                "Reward": self.reward,
                                "position": [self.row, self.col]
                                 }}
        thread = Thread(target=self.notify_observers())
        thread.start()
        thread.join()

    def recursive_step(self, action):
        for _action in action:
            self.step(_action)

    # perform an action in environment:
    def step(self, action):
        lock = RLock()
        with lock:
            (self.observation_space, reward, self.state["done"], truncated,
            info) = self.env.step(action)
            self.state["state"] = self.observation_space
            self.update_position(action)
            surrounding_tiles = self.get_surrounding_tiles(self.row,
                                                       self.col)
            self.text_stimuli = {"text": {"content":
                                self.form_external_stimuli(surrounding_tiles),
                                      "id": self.id,
                                 "observation_space": self.observation_space,
                                 "action_space": self.action_space,
                                 "Reward": self.reward,
                                 "position" : [self.row, self.col]}}
        thread = Thread(target=self.notify_observers())
        thread.start()
        thread.join()

    def update_position(self, action):
        if action == 3:  # up
            self.row = max(self.row - 1, 0)
        elif action == 2:  # Right
            self.col = min(self.col + 1, self.env.unwrapped.desc.shape[1] - 1)
        elif action == 1:  # down
            self.row = min(self.row + 1, self.env.unwrapped.desc.shape[0] - 1)
        elif action == 0:  # Left
            self.col = max(self.col - 1, 0)

    def get_surrounding_tiles(self, row, col):
        # gathering information about the tiles surrounding the agent
        desc = self.env.unwrapped.desc
        surrounding_tiles = {}
        directions = {
            "up": (max(row - 1, 0), col),
            "right": (row, min(col + 1, desc.shape[1] - 1)),
            "down": (min(row + 1, desc.shape[0] - 1), col),
            "left": (row, max(col - 1, 0)),
        }
        for direction, (r, c) in directions.items():
            surrounding_tiles[direction] = desc[r, c].decode(
                'utf-8')  # Decode byte to string
        return surrounding_tiles

    def form_external_stimuli(self, surrounding_tile):
        directions = {
            'up': 3,
            'right': 2,
            'down' : 1,
            'left' : 0
        }
        stimuli = {}
        for direction, tile in surrounding_tile.items():
            if tile == 'H':
                stimuli[direction] = 'hole'
            elif tile == 'S':
                stimuli[direction] = 'start'
            elif tile == 'G':
                stimuli[direction] = 'goal'
            else:
                stimuli[direction] = 'safe'
        return stimuli

    # close the environment:
    def close(self):
        self.env.close()

    def get_stimuli(self):
        return self.text_stimuli

    def get_position(self):
        return {"row": self.row, "col" : self.col}

    def notify(self, module):
        if isinstance(module, MotorPlanExecution):
            action = module.send_motor_plan()
            if not self.state["done"] and not self.shutdown:
                if isinstance(action, list):
                    self.recursive_step(action)
                else:
                    self.step(action)
            else:
                self.reward += 1
                self.close()