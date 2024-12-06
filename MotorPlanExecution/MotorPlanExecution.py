#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

"""
Responsible for taking in a behavior and executing
"""

class MPExecution:
    def __init__(self, environment):
        self.env = environment #Storing the environment reference

    def execute(self, action):
        #Executing the action within the environment
        state,reward,done,truncated,info = self.env.step(action)
        #self.env.render() #Visualizing the environment
        return state,reward,done, truncated,info #Returning the results of the action
        