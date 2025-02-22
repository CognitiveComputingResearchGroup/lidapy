#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.PAM.PAM import PerceptualAssociativeMemory
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            module.retrieve_associations(self)
