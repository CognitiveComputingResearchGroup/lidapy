from source.Framework.Shared.Activatible import Activatible


class Coalition(Activatible):
    def __init__(self):
        super().__init__()
        self.Id = None

    def getBroadcastContent(self):
        pass

    def setBroadcastContent(self, content):
        pass

    def getCreatingAttentionCodelet(self):
        pass

    def setCreatingAttentionCodelet(self, codelet):
        pass

    def getId(self):
        return self.Id


