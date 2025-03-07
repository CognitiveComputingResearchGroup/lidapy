from source.Workspace.Workspace import Workspace


class WorkspaceImpl(Workspace):
    def __init__(self):
        super().__init__()
        self.logger.name = self.__class__.__name__

    def addCueListener(self, cue_listener):
        self.observers.add(cue_listener)

    def addWorkspaceListener(self, workspace_listener):
        self.observers.add(workspace_listener)

    def cueEpisodicMemories(self, node_structure):
        self.notify_observers()
        self.logger.info("Cue performed.")

    def get_module_content(self , params):
        pass

    def receive_broadcast(self, coalition):
        pass

    def receive_percept(self, percept):
        self.percepts.append(percept)

    def receiveLocalAssociation(self, node_structure):
        pass

    def decayModule(self, time):
        pass

    def notify(self, module):
        pass