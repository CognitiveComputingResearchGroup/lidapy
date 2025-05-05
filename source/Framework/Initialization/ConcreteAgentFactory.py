import importlib.util
import os

from source.Framework.Agents.Alarms_Control_Agent import AlarmsControlAgent
from source.Framework.Agents.Minimal_Reactive_Agent import MinimalReactiveAgent
from source.Framework.Agents.Minimal_Conscious_Agent import \
    MinimalConsciousAgent
from source.Framework.Initialization.AgentFactory import AgentFactory

from Configs import Config


class ConcreteAgentFactory(AgentFactory):
    # concrete factory for creating and initializing agents
    def __init__(self):
        super().__init__()

    def get_agent(self, agent_type):
        if agent_type == "MinimalReactiveAgent" or agent_type == 1:
            return MinimalReactiveAgent()
        elif agent_type == "AlarmsControlAgent" or agent_type == 2:
            return AlarmsControlAgent()
        elif agent_type == "MinimalConsciousAgent" or agent_type == 3:
            return MinimalConsciousAgent()
        else:
            try:
                return self.load_from_module(agent_type)
            except:
                raise ModuleNotFoundError(f"Module \"{agent_type}\" not found")

    def load_from_module(self, module):
        proj_path = os.path.dirname(os.path.abspath("Configs"))
        path = Config.module_locations[module]
        full_path = proj_path + path

        # Name the module
        module_name = module

        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
