#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import difflib
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
            self.state = module.__getstate__()
            associations = None

            if isinstance(self.state, NodeImpl):
                associations = module.retrieve_association(self.state)

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            self.notify_observers()

        elif isinstance(module, GlobalWorkspace):
            winning_coalition = module.__getstate__()
            self.learn(winning_coalition)

    def activate_schemes(self, associations):
        schemes = None
        if associations is not None:
            """Get only the links that match the scheme"""
            schemes = self.get_closest_match(associations)

        if isinstance(schemes, list):
            for scheme in schemes:
                self.add_scheme(self.state, scheme)
                scheme.setSink(self.state.getId())
        else:
            self.add_scheme(self.state, schemes)
            schemes.setSink(self.state.getId())

    def learn(self, broadcast):
        result = self.get_closest_match(broadcast)
        current_scheme = None

        """If closest match returns more than one link, optimize results"""
        if isinstance(result[0], list):
            #Find the scheme that minimizes distance to goal
            current_scheme = self.seek_goal(result[0])
        else:
            """Scheme leads to goal if single link is returned"""
            current_scheme = result[0]

        self.add_scheme(self.state, current_scheme)
        self.notify_observers()

    def get_closest_match(self, links):
        schemes = []
        percepts = []
        wanted_scheme = None
        alright_schemes = []
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
            closest_match = difflib.get_close_matches(self.scheme,
                                                          percepts,
                                                          n=values_to_match)
        for link in links:
            if isinstance(closest_match, list):
                for matches in closest_match:
                    if link.getCategory("label") in matches:
                        schemes.append(link)
            else:
                if link.getCategory("label") == closest_match:
                    schemes.append(link)

        for scheme in schemes:
            if scheme.getCategory("label") == "goal":
                wanted_scheme = scheme  # Seek goal
                break
            else:
                links.remove(scheme)            # Avoid hole
                #alright_schemes.append(scheme)  # Stay safe

        if wanted_scheme is not None:
            return wanted_scheme
        else:
            return links

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

