from abc import ABC, abstractmethod


class PAMFactory(ABC):
    """
        Creates and returns a PAM module
        @param perceptual_associative_mem
	        PAM properties
	    @return Constructed PAM object
        """

    @abstractmethod
    def create_pam(self, perceptual_associative_mem):
        pass

    @abstractmethod
    def notify(self, event):
        pass

    @abstractmethod
    def get_position(self, state):
        pass

    @abstractmethod
    def add_association(self, cue, pattern):
        pass

    @abstractmethod
    def retrieve_associations(self, cue):
        pass

    @abstractmethod
    def learn(self, state, outcome, action):
        pass