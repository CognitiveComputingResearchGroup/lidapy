#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

class ProceduralMemory:
    def __init__(self):
        self.schemes = {} # initialize empty memory for schemes

    def add_scheme(self, percept, action):
        self.schemes[percept] = action # add new scheme to memory
        # percept: percept cue ("goal", "safe", or "danger")
        # action: corresponding action or scheme

    def get_action(self, percept):
        return self.schemes.get(percept, None) # get action for the percept
        # return corresponding action or None if not found