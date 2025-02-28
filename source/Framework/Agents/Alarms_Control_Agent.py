from source.Environment.FrozenLakeSimpleEnv import FrozenLakeMinimal
from source.Framework.Agents.Agent import Agent


class AlarmsControlAgent(Agent):
    def __init__(self):
        super().__init__()
        self.environment = FrozenLakeMinimal()

    def run(self):
        self.environment.reset()