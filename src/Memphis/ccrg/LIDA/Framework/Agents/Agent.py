#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from src.Memphis.ccrg.LIDA.ActionSelection.ActionSelection import ActionSelection
from src.Memphis.ccrg.LIDA.PAM.PAM import PerceptualAssociativeMemory
from src.Memphis.ccrg.LIDA.SensoryMemory.SensoryMemory import SensoryMemory
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment
from MotorPlanExecution.MotorPlanExecution import MPExecution
from src.Memphis.ccrg.LIDA.ProceduralMemory.ProceduralMemory import ProceduralMemory
from src.Memphis.ccrg.LIDA.SensoryMotorMemory.SensoryMotorMemoryImpl import SensoryMotorMemoryImpl


class Agent:
    def __init__(self):
        self.env =  FrozenLakeEnvironment()
        self.pam = PerceptualAssociativeMemory() # create pam instance
        self.sensory_memory = SensoryMemory(self.env, self.pam)  # pass in environment and pam instance
        self.motor_plan_execution = MPExecution(self.env)
        self.procedural_memory = ProceduralMemory() # initialize procedural memory
        self.action_selection = ActionSelection(self.env.action_space, self.procedural_memory) # pass in procedural memory
        self.sensory_motor_memory = SensoryMotorMemoryImpl(self.action_selection, self.motor_plan_execution)
        #self.procedural_memory.add_scheme("safe", 2)
        #self.procedural_memory.add_scheme("danger", 0)

        '''
        # state rules for 4x4 map
        self.procedural_memory.add_scheme("state-0", 2)  # move right
        self.procedural_memory.add_scheme("state-1", 2)  # move right
        self.procedural_memory.add_scheme("state-2", 1)  # move down
        self.procedural_memory.add_scheme("state-6", 1)  # move down
        self.procedural_memory.add_scheme("state-9", 2)  # move right
        self.procedural_memory.add_scheme("state-10", 2)  # move right
        self.procedural_memory.add_scheme("state-14", 3)  # move up
        self.procedural_memory.add_scheme("goal", None) # finish when goal reached
        '''

    def run(self):
        #Agents behavior logic
        done = False
        state_id = 0
        state, percept, action, environment, col, row = self.sensory_memory.run_sensors(self.procedural_memory, state_id)
        print(f"Initial Observation: State: {state}, Percept: {percept}")
        #Additional code needed for the agents action (MAYBE)?

        while not done:
            #action = self.env.action_space.sample() #Replace when developed action selection logic
            state, state_id, reward, done, truncated, info = self.action_selection.select_action(percept, state_id, self.sensory_motor_memory) # use action selection to decide next action
            #action = state["target_location"]
            print(f"Action: {action}\n")

            #state, reward, done, truncated, info = self.env.step(action)
            #self.env.render()
            print(f"State: {state_id}, Reward: {reward}, Done: {done}, Info: {info}")

            state_str = "state-"
            state_id_str = state_id.__str__()
            state_str += state_id_str

            if state == 15:         # goal state in 4x4 map
                self.pam.learn(state_str, "goal")
            elif reward == 0 and done: # fell into a hole
                self.pam.learn(state_str, "hole")
                print(f"Action: {action}\n")
            else: # safe state
                self.pam.learn(state_str, "safe")

            action = environment.action_space.sample() #Take a random action
            #observation = environment.env.spec.kwargs.get("desc")
            self.procedural_memory.add_scheme(state_str, action)
            percept = self.pam.retrieve_associations(state_str)  # update percept
        self.env.close()

