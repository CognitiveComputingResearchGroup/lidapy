import argparse
import logging
from src.Framework.Agents.Agent import Agent


class AgentStarter:
    logger = logging.getLogger(__name__)

    """
    Default configuration properties file path
    """
    DEFAULT_PROPERTIES_PATH = "configs/lidaConfig.properties"

    currentAgent = Agent

    """
    Starts an {@link Agent} using the default properties path or the one 
    that is specified in the command line arguments
    """
    def __main__(self):
        # Specify the configuration file path
        properties_path = AgentStarter.DEFAULT_PROPERTIES_PATH
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "agent", help="Agent name",
                            default=Agent)
        args = parser.parse_args()
        agent_type = args.agent  # Gets the name of the agent

        if len(agent_type) != 0:
            properties_path = agent_type
        properties = self.load_properties(properties_path)
        if properties is None:
            self.logger.critical('Could not load main properties file from '
                                 'path: ' f'{properties_path}, trying '
                                 f'default properties '
                                 'path instead.')
            self.start()
        else:
            self.start(properties)

    def start(self, properties=None, properties_path=None):
        if properties is not None:
            agent_properties = properties['agent']
            if agent_properties is None:
                self.logger.critical('Specified Properties object is null, '
                                     'attempting to load default properties '
                                     'path instead.')
                self.start()
            else:
                self.run()
        elif properties_path is not None:
            agent_properties = self.load_properties(properties_path)
            if agent_properties is not None:
                self.run()
            else:
                self.logger.critical(
                    'Specified Properties object is null, trying'
                    'to load default properties path instead.')
                self.start()
        else:
            properties_path = AgentStarter.DEFAULT_PROPERTIES_PATH
            agent_properties = self.load_properties(properties_path)
            if agent_properties is not None:
                self.run()
            else:
                self.logger.critical(
                    'Could not load main configuration file from '
                    'default path: '
                    f'{properties_path}. Application cannot start.')


    #def run(self):


    """
    Obtains the properties path by parsing the properties file.
    Credit to Roberto: 
        "https://stackoverflow.com/questions/3595363/
         properties-file-in-python-similar-to-java-properties".
    """
    def load_properties(self, properties_path, sep='=', comment_char='#'):
        """
        Read the file passed as parameter as a properties file.
        """
        props = {}
        with open(properties_path, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
        return props
