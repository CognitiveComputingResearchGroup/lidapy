#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from SensoryMemory import SensoryMemory
from Environment import FrozenLakeEnvironment

class FrozenLakeAgent:
    def __init__(self):
        self.env = FrozenLakeEnvironment()
        self.sensory_memory = SensoryMemory()

    def run(self):
        done = False
        state = self.sensory_memory.run_sensors(self.env)
        print(f"Initial Observation: {state}")

        while not done:
            action = self.env.action_space.sample()
            print(f"Action: {action}")

            state, reward, done, truncated, info = self.env.step(action)
            self.env.render()
            print(f"State: {state}, Reward: {reward}, Done: {done}, Info: {info}")

        self.env.close()