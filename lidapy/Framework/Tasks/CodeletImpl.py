from Framework.Shared.LearnableImpl import LearnableImpl
from Framework.Shared.NodeStructureImpl import NodeStructureImpl
from Framework.Tasks.Codelet import Codelet


class CodeletImpl(Codelet, LearnableImpl):
    def __init__(self):
        super().__init__()
        self.soughtContent  = NodeStructureImpl()

    def getSoughtContent(self):
        return self.soughtContent

    def setSoughtContent(self, content):
        self.soughtContent = content