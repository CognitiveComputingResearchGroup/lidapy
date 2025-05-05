# LIDA Cognitive Framework
# Pennsylvania State University, Course : SWENG480
# Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
from threading import Lock
from time import sleep

from source.Environment.Environment import Environment
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.Module.Initialization.DefaultLogger import getLogger
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
        self.nodes = []
        self.sensor_dict = {}
        self.processor_dict = {}
        self.logger = getLogger(__class__.__name__).logger


    def start(self):
        self.logger.debug(f"Initialized SensoryMemory with "
                          f"{len(self.processors)} sensor processors")
        # Initialize sensors
        for key, processor in self.processor_dict.items():
            self.processors[key] = getattr(self.sensor, processor)

    def notify(self, module):
        if isinstance(module, Environment):
            self.stimuli = module.get_stimuli()
        if not self.processors:
            self.start()
        self.run_sensors()

    def run_sensors(self):
        """All sensors associated will run with the memory"""
        # Logic to gather information from the environment
        self.nodes = []
        if self.stimuli is not None:
            for sensor, value in self.stimuli.items():
                if sensor not in self.processor_dict:
                    self.logger.debug(f"Sensor '{sensor}' is currently not "
                                        f"supported.")
                else:
                    sensory_cue = self.processors[sensor](value)
                    if sensory_cue is not None:
                        if isinstance(sensory_cue, NodeStructureImpl):
                            nodes = sensory_cue.getNodes()
                            for node in nodes:
                                self.nodes.append(node)
                        elif isinstance(sensory_cue, NodeImpl):
                            self.nodes.append(sensory_cue)
            self.logger.debug(f"Processed {len(self.nodes)} sensory cue(s)")
            sleep(0.5)
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
        return {"cue": self.nodes, "modality": modality, "params": None}