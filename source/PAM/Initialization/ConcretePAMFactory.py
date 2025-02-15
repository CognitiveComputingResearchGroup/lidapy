from source.GlobalModuleInterface.GlobalModuleFactory import GlobalModuleFactory
from source.PAM.Initialization.PAMFactory import PAMFactory


class PAMConcreteFactory(PAMFactory, GlobalModuleFactory):
    def __init__(self):
        super().__init__()

    def create_pam(self, perceptual_associative_mem):
        return perceptual_associative_mem

    def get_position(self, state):
        pass

    def notify(self, event):
        pass

    def add_association(self, cue, pattern):
        pass

    def retrieve_associations(self, cue):
        pass

    def learn(self, state, outcome, action):
        pass
