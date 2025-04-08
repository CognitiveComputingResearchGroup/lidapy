from abc import ABC, abstractmethod


class AgentFactory(ABC):

    """
    Creates and returns an Agent from a specified type
	 @param agent_type
	        Agent properties
	 @return Constructed Agent object
    """

    @abstractmethod
    def get_agent(self, agent_type):
        pass