#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import argparse
import sys


from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

DEFAULT_AGENT_ID = 3
DEFAULT_AGENT_TYPE = "AlarmsControlAgent"
DEFAULT_AGENT_ENVIRONMENT = "GodotEnvironment"


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

if __name__ == "__main__":
    # Create agent factory
    agent_factory = ConcreteAgentFactory()
    try:
        args = parse_args()
        if args.type != DEFAULT_AGENT_TYPE:
            agent = agent_factory.get_agent(args.type)
        else:
            agent = agent_factory.get_agent(args.id) # Initialize agent

        agent.environment_type = args.environment

        # Start the agent
        try:
            agent.run()
            sys.exit(0)
        except Exception as e:
            print(e)
    except Exception as e:
        raise e

