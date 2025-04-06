from source.Framework.Tasks.Codelet import Codelet
from source.Module.Initialization.ModuleInterface import Module


class StructureBuildingCodelet(Module, Codelet):
    def __init__(self):
        super().__init__()

    def get_codelet_run_results(self):
        pass

    def retrieve_workspace_content(self):
        pass

    def notify(self, module):
        pass