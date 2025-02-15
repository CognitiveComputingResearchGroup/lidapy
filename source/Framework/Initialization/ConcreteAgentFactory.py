from source.Framework.Initialization.AgentFactory import AgentFactory
from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory


class ConcreteAgentFactory(AgentFactory, GlobalModuleFactory):
    # concrete factory for creating and initializing agents
    def __init__(self):
        super().__init__()

    def get_agent(self, agent_type):
        return agent_type

    # Run the agent through the environment
    def run(self):
        pass

    def notify_(self, action):
        pass

    def notify(self, state, reward, done, truncated, info, action,
               surrounding_tiles):
        pass