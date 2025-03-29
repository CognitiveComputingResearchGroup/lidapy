# LIDA Cognitive Framework
# Pennsylvania State University, Course : SWENG480
# Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from source.Environment.Environment import Environment
from source.Framework.Agents.Agent import Agent
from source.Framework.Shared.NodeImpl import NodeImpl
from source.ModuleInitialization.DefaultLogger import getLogger
from source.SensoryMemory.SensoryMemory import SensoryMemory


"""
This module can temporarily store sensory data from the environment and then
process and transfer to further working memory.
"""


class SensoryMemoryImpl(SensoryMemory):
    def __init__(self):
        super().__init__()

        #Add module specific attributes
        self.processors = {}
        self.logger = getLogger(__class__.__name__).logger
        self.stimuli = None
        self.position = None
        self.nodal_cues = []

        for key, processor in self.processor_dict.items():
            self.processors[key] =  getattr(self.sensor_module, processor)

        self.logger.debug(f"Initialized SensoryMemory with "
                          f"{len(self.processors)} sensor processors")

    def notify(self, module):
        if isinstance(module, Environment):
            self.stimuli = module.get_stimuli()
            self.position = module.get_position()
            self.run_sensors()

    def run_sensors(self):
        """All sensors associated will run with the memory"""
        # Logic to gather information from the environment
        for sensor, value in self.stimuli.items():
            if sensor not in self.sensors:
                self.logger.debug(f"Sensor '{sensor}' is currently not "
                                  f"supported.")
            else:
                sensory_cue = self.processors[sensor](value)
                if sensory_cue is not None:
                    if isinstance (sensory_cue, NodeImpl):
                        self.nodal_cues.append(sensory_cue)
        self.logger.debug(f"Processed {len(self.nodal_cues)} sensory cue(s)")
        self.notify_observers()

    def get_sensory_content(self, modality=None, params=None):
        """
        Returning the content from this Sensory Memory
        :param modality: Specifying the modality
        :param params: optional parameters to filter or specify the content
        :return: content corresponding to the modality
        """
        for key, content in self.stimuli.items():
            modality = key
        # Logic to retrieve and return data based on the modality.
        return {"cue": self.nodal_cues, "modality": modality,
                "params": self.position}