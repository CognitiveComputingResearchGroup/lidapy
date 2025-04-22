from source.Module.Initialization.ModuleInterface import Module


class SensoryMotorMemory(Module):
    def __init__(self):
        super().__init__()
        self.listeners = []

    def notify(self, module):
        pass

    def add_sensory_listener(self, listener):
        """Adding the listener to the memory"""
        if listener not in self.listeners:
            self.listeners.append(listener)

    def send_action_execution_command(self):
        """
        Returning the content from this Sensory Motor Memory
        :param action_plan: Specifying the action(s) to take
        :return: content corresponding to the action_plan
        """
        pass