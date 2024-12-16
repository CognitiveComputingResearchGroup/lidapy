#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

#from src.Memphis.ccrg.LIDA.Framework.Agents.Agent import Agent
from src.Framework.Initialization.ConcreteAgentFactory import ConcreteAgentFactory

if __name__ == "__main__":
    #agent = Agent() #instantiate FrozenLakeAgent / create instance of the class
    agent_type = {
        "render_mode": "human",
        "action_space_size": 4,
        "map_size": 5
    }

    # create factory and initialize agent
    factory = ConcreteAgentFactory()
    agent = factory.get_agent(agent_type)

    agent.run()