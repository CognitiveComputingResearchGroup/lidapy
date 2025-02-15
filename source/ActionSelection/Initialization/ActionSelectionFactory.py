from abc import ABC,abstractmethod


class ActionSelectionFactory(ABC):
    """
    Creates and returns a ActionSelection Module
    @param action_selection
	        ActionSelection properties
	    @return Constructed ActionSelection object
    """

    @abstractmethod
    def create_action_selection(self, action_selection):
        pass

    @abstractmethod
    def select_action(self, percept, action, module):
        pass

    @abstractmethod
    def notify(self, scheme):
        pass