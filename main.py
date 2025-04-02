#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import argparse
import multiprocessing
import sys
from time import sleep

from source.Framework.Initialization.ConcreteAgentFactory import \
    ConcreteAgentFactory

DEFAULT_AGENT_ID = 3
DEFAULT_AGENT_TYPE = "AlarmsControlAgent"


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

        # Start the agent
        try:
            multiprocessing.set_start_method("spawn")
            agent.environment_thread.start()
            agent.environment_thread.join()
            agent.sensory_memory_process.start()
            agent.sensory_memory_process.join()
            agent.pam_process.start()
            agent.pam_process.join()
            agent.csm_process.start()
            agent.csm_process.join()
            agent.workspace_process.start()
            agent.workspace_process.join()
            agent.attention_codelets_process.start()
            agent.attention_codelets_process.join()
            agent.global_workspace_process.start()
            agent.global_workspace_process.join()
            agent.procedural_memory_process.start()
            agent.procedural_memory_process.join()
            agent.sensory_motor_mem_process.start()
            agent.sensory_motor_mem_process.join()
            sys.exit(0)
        except Exception as e:
            print(e)
        try:
            agent.main()
            sys.exit(0)
        except Exception as e:
            print(e)
    except Exception as e:
        raise e

