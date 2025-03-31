#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import difflib
import random
import numpy as np

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.ModuleInitialization.DefaultLogger import getLogger
from source.PAM.PAM import PerceptualAssociativeMemory
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug(f"Initialized ProceduralMemory")

    def notify(self, module):
        if isinstance(module, PerceptualAssociativeMemory):
            state = module.__getstate__()
            self.state = state
            associations = None

            if isinstance(state, NodeImpl):
                associations = module.retrieve_association(state)

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            self.notify_observers()

        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()
            self.learn(winning_coalition, self.scheme)

    def activate_schemes(self, associations):
        actions = None
        percepts = []
        schemes = None
        result = None

        if associations is not None:
            """Get only the links that match the scheme"""
            schemes, actions = (
                self.get_closest_match(associations, self.scheme))

        if isinstance(schemes, list):
            for scheme, action in zip(schemes, actions):
                self.add_scheme(self.state, scheme, action)
                scheme.setActivation(1.0)
            random_index = random.randint(0, len(schemes) - 1)
            while schemes[random_index].getActivation == 1.0:
                random_index = random.randint(0, len(schemes) - 1)
            self.percept = schemes[random_index]
        else:
            self.add_scheme(self.state, schemes, actions)
            schemes.setActivation(1.0)
            schemes.setSink(self.state.getId())
            self.percept = schemes

    def learn(self, broadcast, scheme):
        percepts = []
        schemes = []
        actions = []

        result = self.get_closest_match(broadcast, self.scheme)
        current_scheme = None

        """If closest match returns more than one link, optimize results"""
        if isinstance(result[0], list):
            #Find the scheme that minimizes distance to goal
            current_scheme = self.seek_goal(result[0])
        else:
            """Scheme leads to goal if single link is returned"""
            current_scheme = result[0]
            action = result[1]

        action = current_scheme.getCategory("id")
        self.add_scheme(self.state, current_scheme, action)
        self.notify_observers()

    def get_closest_match(self, links, scheme):
        schemes = []
        percepts = []
        wanted_scheme = None
        alright_schemes = []
        actions = []
        action = None
        closest_match = []

        if links is not None:
            for link in links:
                percepts.append(link.getCategory("label"))

        values_to_match = len(self.scheme)
        if not "goal" in percepts:
            values_to_match = 1

        if isinstance(self.scheme, list):
            for scheme in self.scheme:
                closest_match.append(difflib.get_close_matches(scheme,
                                                               percepts,
                                                            n=values_to_match))
        else:
            for scheme in self.scheme:
                closest_match = difflib.get_close_matches(self.scheme,
                                                          percepts,
                                                          n=values_to_match)
        for link in links:
            for matches in closest_match:
                if link.getCategory("label") in matches:
                    schemes.append(link)

        for scheme in schemes:
            if scheme.getCategory("label") == "goal":
                wanted_scheme = scheme  # Seek goal
                break
            else:
                alright_schemes.append(scheme)  # Stay safe

        if wanted_scheme is not None:
            action = wanted_scheme.getCategory("id")
            return wanted_scheme, action
        else:
            for scheme in schemes:
                actions.append(scheme.getCategory("id"))
            return alright_schemes, actions

    def seek_goal(self, schemes):
        min_distance = 64
        current_scheme = None
        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            if isinstance(scheme, LinkImpl):
                if isinstance(self.state, NodeImpl):
                    action = scheme.getCategory("id")
                    current_position = []
                    action = scheme.getCategory("id")
                    if action == 0:
                        current_position.append(int(self.state.getLabel()[0]))
                        current_position.append(
                            max(int(self.state.getLabel()[1]) - 1, 0))
                    elif action == 1:
                        current_position.append(
                            min(int(self.state.getLabel()[0]) + 1, 7))
                        current_position.append(
                            int(self.state.getLabel()[1]))
                    elif action == 2:
                        current_position.append(
                            int(self.state.getLabel()[0]))
                        current_position.append(
                            min(int(self.state.getLabel()[1]) + 1, 7))
                    elif action == 3:
                        current_position.append(
                            max(int(self.state.getLabel()[0]) - 1, 0))
                        current_position.append(
                            int(self.state.getLabel()[1]))
                    goal = [7, 7]
                    point1 = np.array(current_position)
                    point2 = np.array(goal)
                    distance = np.linalg.norm(point1 - point2)
                    min_distance = min(min_distance, distance)
                    if distance <= min_distance:
                        current_scheme = scheme
        return current_scheme

