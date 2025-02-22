from source.Framework.Agents.Minimal_Reactive_Agent import MinimalReactiveAgent
from source.Framework.Initialization.AgentFactory import AgentFactory


class ConcreteAgentFactory(AgentFactory):
    # concrete factory for creating and initializing agents
    def __init__(self):
        super().__init__()

    def get_agent(self, agent_type):
        if agent_type == "MinimalReactiveAgent":
            return MinimalReactiveAgent()
        else:
            raise ModuleNotFoundError("Module not found")