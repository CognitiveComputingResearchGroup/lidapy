#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from ActionSelection.ActionSelection import ActionSelection
from PAM.PAM import PerceptualAssociativeMemory
from SensoryMemory.SensoryMemory import SensoryMemory
from Environment.Environment import FrozenLakeEnvironment
from MotorPlanExecution.MotorPlanExecution import MPExecution
from ProceduralMemory.ProceduralMemory import ProceduralMemory

class FrozenLakeAgent:
    def __init__(self):
        self.env =  FrozenLakeEnvironment()
        self.pam = PerceptualAssociativeMemory() # create pam instance
        self.sensory_memory = SensoryMemory(self.env, self.pam)  # pass in environment and pam instance
        self.motor_plan_execution = MPExecution(self.env)
        self.procedural_memory = ProceduralMemory() # initialize procedural memory
        self.action_selection = ActionSelection(self.env.action_space, self.procedural_memory) # pass in procedural memory

        #self.procedural_memory.add_scheme("safe", 2)
        #self.procedural_memory.add_scheme("danger", 0)

        # state rules for 4x4 map
        self.procedural_memory.add_scheme("state-0", 2)  # move right
        self.procedural_memory.add_scheme("state-1", 2)  # move right
        self.procedural_memory.add_scheme("state-2", 1)  # move down
        self.procedural_memory.add_scheme("state-6", 1)  # move down
        self.procedural_memory.add_scheme("state-9", 2)  # move right
        self.procedural_memory.add_scheme("state-10", 2)  # move right
        self.procedural_memory.add_scheme("state-14", 3)  # move up
        self.procedural_memory.add_scheme("goal", None) # finish when goal reached

    def run(self):
        #Agents behavior logic
        done = False
        state, percept = self.sensory_memory.run_sensors()
        print(f"Initial Observation: {state}, Percept: {percept}")
        #Additional code needed for the agents action (MAYBE)?

        while not done:
            #action = self.env.action_space.sample() #Replace when developed action selection logic
            action = self.action_selection.select_action(percept) # use action selection to decide next action
            print(f"Action: {action}")

            state, reward, done, truncated, info = self.env.step(action)
            self.env.render()
            print(f"State: {state}, Reward: {reward}, Done: {done}, Info: {info}")

            if state == 15: # goal state in 4x4 map
                self.pam.learn(state, "goal")
            elif reward == 0 and done: # fell into a hole
                self.pam.learn(state, "hole")
            else: # safe state
                self.pam.learn(state, "safe")

            percept = self.pam.retrieve_associations(state)  # update percept

        self.env.close()