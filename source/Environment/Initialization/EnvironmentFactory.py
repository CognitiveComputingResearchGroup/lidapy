from abc import ABC, abstractmethod


class EnvironmentFactory(ABC):
    """
        Creates and returns an Environment Module
        @param environment_type
	        Environment properties
	    @return Constructed Agent object
        """

    @abstractmethod
    def create_environment(self, environment_type):
        pass

    @abstractmethod
    def reset(self, module):
        pass    # Resetting the environment to start a new episode

    @abstractmethod
    def step(self, action, module):
        pass    # Perform an action in environment

    @abstractmethod
    def render(self):
        pass    # render environment's current state:

    @abstractmethod
    def close(self):
        pass    # close the environment:

    @abstractmethod
    def update_position(self, action):
        pass    #updating the agents position based on the action taken

    @abstractmethod
    def get_surrounding_tiles(self, row, col):
        pass    #gathering information about the tiles surrounding the agent