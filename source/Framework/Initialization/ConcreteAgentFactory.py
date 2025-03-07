from source.Framework.Agents.Alarms_Control_Agent import AlarmsControlAgent
from source.Framework.Agents.Minimal_Reactive_Agent import MinimalReactiveAgent
from source.Framework.Agents.Minimally_Conscious_Agent import \
    MinimallyConsciousAgent
from source.Framework.Initialization.AgentFactory import AgentFactory


class ConcreteAgentFactory(AgentFactory):
    # concrete factory for creating and initializing agents
    def __init__(self):
        super().__init__()

    def get_agent(self, agent_type):
        if agent_type == "MinimalReactiveAgent" or agent_type == "1":
            return MinimalReactiveAgent()
        elif agent_type == "AlarmsControlAgent" or agent_type == "2":
            return AlarmsControlAgent()
        elif agent_type == "MinimallyConsciousAgent" or agent_type == "3":
            return MinimallyConsciousAgent()
        else:
            raise ModuleNotFoundError("Module not found")