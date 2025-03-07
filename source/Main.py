#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

if __name__ == "__main__":
    # Create agent factory and initialize agent
    agent_factory = ConcreteAgentFactory()
    agent = agent_factory.get_agent("3")

    #Start the agent
    agent.run()