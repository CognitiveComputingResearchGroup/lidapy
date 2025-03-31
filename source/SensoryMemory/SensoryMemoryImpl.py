# LIDA Cognitive Framework
# Pennsylvania State University, Course : SWENG480
# Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from time import sleep

from source.Environment.Environment import Environment
from source.Framework.Agents.Agent import Agent
from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
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
        self.sensor = None
        self.processors = {}
        self.stimuli = None
        self.position = None
        self.state = None
        self.links = []
        self.sensor_dict = {}
        self.processor_dict = {}
        self.logger = getLogger(__class__.__name__).logger

        self.logger.debug(f"Initialized SensoryMemory with "
                          f"{len(self.processors)} sensor processors")

    def notify(self, module):
        if isinstance(module, Environment):
            self.stimuli = module.get_stimuli()
            self.position = module.get_position()
            self.state = module.__getstate__()

            #Initialize sensors
            for key, processor in self.processor_dict.items():
                self.processors[key] = getattr(self.sensor, processor)
            self.run_sensors()

    def run_sensors(self):
        """All sensors associated will run with the memory"""
        # Logic to gather information from the environment
        if self.stimuli is not None:
            for sensor, value in self.stimuli.items():
                if sensor not in self.sensor_dict:
                    self.logger.debug(f"Sensor '{sensor}' is currently not "
                                      f"supported.")
                else:
                    sensory_cue = self.processors[sensor](value)
                    if sensory_cue is not None:
                        if isinstance(sensory_cue, LinkImpl):
                            self.links.append(sensory_cue)
                        elif isinstance(sensory_cue, NodeStructureImpl):
                            for link in sensory_cue.getLinks():
                                self.links.append(link)
            self.logger.debug(f"Processed {len(self.links)} sensory cue(s)")
            sleep(0.5)       #Wait for previous sensory cue processing
            self.notify_observers()
        else:
            self.logger.debug("Waiting for stimuli from the environment")

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
        return {"cue": self.links, "modality": modality,
                "params": {"position": self.position, "state": self.state}}