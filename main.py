#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import argparse
from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

DEFAULT_AGENT_ID = 1
DEFAULT_AGENT_TYPE = 'MinimalReactiveAgent'


def parse_args():
    parser = argparse.ArgumentParser(description='LIDA Agent Factory '
                                                 'Command Line Interface')
    parser.add_argument('--id', type=int, required=False,
                        default=1, help='The agent ID (default: '
                                        f'{DEFAULT_AGENT_ID})')
    parser.add_argument('--type', type=str,
                        required=False, default=DEFAULT_AGENT_TYPE,
                        help='The name of the agent type'
                             f'(default: {DEFAULT_AGENT_TYPE})')
    return parser.parse_args()

if __name__ == "__main__":
    # Create agent factory
    agent_factory = ConcreteAgentFactory()
    try:
        args = parse_args()
        agent = agent_factory.get_agent(args.id) # Initialize agent

        # Start the agent
        agent.run()
    except Exception as e:
        raise e

