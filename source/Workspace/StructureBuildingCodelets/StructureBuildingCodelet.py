from source.ModuleInitialization.ModuleInterface import Module


class StructureBuildingCodelet(Module):
    def __init__(self):
        super().__init__()
        self.observers = []

    def get_codelet_run_results(self):
        pass

    def retrieve_workspace_content(self):
        pass

    def notify(self, module):
        pass