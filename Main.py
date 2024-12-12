#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from src.Memphis.ccrg.LIDA.Framework.Agents.Agent import Agent

if __name__ == "__main__":
    agent = Agent() #instantiate FrozenLakeAgent / create instance of the class
    agent.run()