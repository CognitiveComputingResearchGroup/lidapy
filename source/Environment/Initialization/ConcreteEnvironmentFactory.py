from source.Environment.Initialization.EnvironmentFactory import \
    EnvironmentFactory
from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory


class ConcreteEnvironmentFactory(EnvironmentFactory, GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_environment(self, environment_type):
        return environment_type

    def reset(self, module):
        pass    # Resetting the environment to start a new episode

    def step(self, action, module):
        pass    # Perform an action in environment

    def render(self):
        pass    # render environment's current state:

    def close(self):
        pass    # close the environment:

    def update_position(self, action):
        pass    #updating the agents position based on the action taken

    def get_surrounding_tiles(self, row, col):
        pass    #gathering information about the tiles surrounding the agent