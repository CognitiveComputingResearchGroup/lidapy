from abc import ABC, abstractmethod


class GlobalWorkspace(ABC):
    """
    Interface for storing, retrieving, and updating
    modules and attributes between various LIDA modules
    """

    def __init__(self):
        self.modules = {}
        self.attributes = {}

    def add_module(self, module_name, module_instance):
        # add a module to the instance
        self.modules[module_name] = module_instance

    def get_module(self, module_name):
        return self.modules.get(module_name)  # retrieve a module by name

    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def update_attribute(self, attribute_name, value):
        self.attributes[attribute_name] = value

    def get_attribute(self, attribute_name):
        return self.attributes.get(attribute_name)