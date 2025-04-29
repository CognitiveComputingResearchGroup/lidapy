from Framework.Shared.Learnable import Learnable
from Module.Initialization.ModuleInterface import Module


class Codelet(Module, Learnable):
    def __init__(self):
        super().__init__()
        self.observers = []

    def notify(self, module):
        pass

    """
         return the sought content
         """
    def getSoughtContent(self):
        pass

    """"
        content the codelet looks for
        """
    def setSoughtContent(self, content):
        pass

    """
        WorkspaceBuffer to be checked for content,
        returns true, if successful
        """
    def bufferContainsSoughtContent(self, buffer):
        pass

    """
        Returns sought content and related content from specified
        WorkspaceBuffer
        """
    def retrieveWorkspaceContent(self, buffer):
        pass