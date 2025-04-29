from Framework.Tasks.Codelet import Codelet
from Module.Initialization.DefaultLogger import getLogger


class AttentionCodelet(Codelet):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__).logger

    def getModuleContent(self):
        pass

    def notify(self, module):
        pass