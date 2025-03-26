from source.GlobalWorkspace.Coalition import Coalition
from source.Framework.Shared.ActivatibleImpl import ActivatibleImpl


class CoalitionImpl(Coalition, ActivatibleImpl):
    def __init__(self):
        super().__init__()
        self.broadcastContent = None
        self.attentionCodelet = None

    def getBroadcastContent(self):
        return self.broadcastContent

    def setBroadcastContent(self, content):
        self.broadcastContent = content

    def getCreatingAttentionCodelet(self):
        return self.attentionCodelet

    def setCreatingAttentionCodelet(self, codelet):
        self.attentionCodelet = codelet