from source.GlobalWorkspace.Coalition import Coalition


class CoalitionImpl(Coalition):
    def __init__(self, broadcast_content = None, attention_codelet = None):
        super().__init__()

        self.id_counter = 0
        self.ID = self.id_counter + 1
        self.broadcastContent = broadcast_content
        self.attention_codelet = attention_codelet

    def setCoalitionActivation(self):
        pass

    def getContent(self):
        return self.broadcastContent

    def setContent(self, broadcast_content):
        self.broadcastContent = broadcast_content

    def getCreatingAttentionCodelet(self):
        return self.attention_codelet

    def setCreatingAttentionCodelet(self, attention_codelet):
        self.attention_codelet = attention_codelet

    def getID(self):
        return self.ID



