#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import argparse
import importlib
import os
from importlib import util

from Configurations import Config
from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

DEFAULT_AGENT_ID = 3
DEFAULT_AGENT_TYPE = "AlarmsControlAgent"
DEFAULT_AGENT_ENVIRONMENT = "FrozenLakeEnvironment"


def parse_args():
    parser = argparse.ArgumentParser(description='LIDA Agent Factory '
                                                 'Command Line Interface')
    parser.add_argument('--id', type=int, required=False,
                        default=DEFAULT_AGENT_ID, help='The agent ID (default: '
                                        f'{DEFAULT_AGENT_ID})')
    parser.add_argument('--type', type=str,
                        required=False, default=DEFAULT_AGENT_TYPE,
                        help='The name of the agent type'
                             f'(default: {DEFAULT_AGENT_TYPE})')
    parser.add_argument('--environment', type=str, required=False,
                        default=DEFAULT_AGENT_ENVIRONMENT, help='The name of '
                        f'the agent environment (default: '
                        f'{DEFAULT_AGENT_ENVIRONMENT})')
    return parser.parse_args()

def load_from_module(module_name):
    proj_path = os.path.dirname(os.path.abspath("lidapy"))
    path = Config.module_locations[module_name]
    full_path = proj_path + path

    # Name the module
    module_name = module_name

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    # Create agent factory
    agent_factory = ConcreteAgentFactory()
    try:
        args = parse_args()
        if args.type != DEFAULT_AGENT_TYPE:
            agent = agent_factory.get_agent(args.type)
        else:
            agent = agent_factory.get_agent(args.id) # Initialize agent

        module = load_from_module(args.environment)
        agent.environment = module.__getattribute__(args.environment)()

        # Start the agent
        agent.run()
    except Exception as e:
        raise e

