#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import difflib
from time import sleep
import numpy as np

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.Module.Initialization.DefaultLogger import getLogger
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()
        self.near_goal_schemes = {}
        self.logger = getLogger(__class__.__name__).logger
        self.logger.debug(f"Initialized ProceduralMemory")

    def notify(self, module):
        if isinstance(module, PAMImpl):
            self.state = module.get_state()
            associations = None

            if isinstance(self.state, NodeImpl):
                associations = module.retrieve_association(self.state)

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            sleep(0.2)
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            links = []
            for link in broadcast.getLinks():
                """If a node has been visited (optimize the route from that
                node to the goal ( find the shortest path))"""
                source = link.getSource()
                if isinstance(source, NodeImpl):
                    if link.getSource().getActivation() < 1:
                        links.append(link)
            if len(links) == 0:
                source = broadcast.containsNode()
                links = broadcast.getConnectedSinks(source)

            self.learn(links)

    def activate_schemes(self, associations):
        schemes = None
        if associations is not None:
            """Get only the links that match the scheme"""
            schemes = self.get_closest_match(associations)

        if isinstance(schemes, list):
            for scheme in schemes:
                self.add_scheme(self.state, scheme)
                if (scheme.getActivation() is not None and
                        scheme.getActivation() >= 0.05):
                    scheme.decay(0.05)
                if scheme.isRemovable():
                    self.schemes[self.state].remove(scheme)
            self.logger.debug(f"Instantiated {len(schemes)} action scheme(s)")
        else:
            self.add_scheme(self.state, schemes)
            #schemes.setSink(self.state.getId())
            self.logger.debug("Instantiated single action scheme")

    """Gets the link that closely matches the scheme"""
    def get_closest_match(self, links):
        schemes = []
        percepts = []
        wanted_scheme = None
        alright_schemes = []
        closest_match = []
        found_matches = False

        """Get a list of all percepts"""
        if links is not None:
            for link in links:
                percepts.append(link.getCategory("label"))

        values_to_match = len(self.scheme)
        if not "goal" in percepts:
            values_to_match = 1

        """Match the percept to a scheme based on string similarity"""
        if isinstance(self.scheme, list):
            for scheme in self.scheme:
                closest_match.append(difflib.get_close_matches(scheme,
                                                               percepts,
                                                            n=values_to_match))
        else:
            closest_match = difflib.get_close_matches(self.scheme,
                                                          percepts,
                                                          n=values_to_match)

        ""'Get the corresponding schemes'
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
            links = wanted_scheme

        return links

    def learn(self, broadcast):
        result = self.get_closest_match(broadcast)
        current_scheme = None

        """If closest match returns more than one link, optimize results"""
        if isinstance(result, list):
            #Find the scheme that minimizes distance to goal
            current_scheme = self.optimize_schemes(result)
        else:
            """Scheme leads to goal if single link is returned"""
            current_scheme = result

        self.add_scheme(self.state, current_scheme)

    """Finds the shortest distance between the current link and a scheme"""
    def optimize_schemes(self, schemes):
        min_distance = 64
        current_scheme = None
        instantiated_schemes = []
        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            if isinstance(scheme, LinkImpl):
                source_node = scheme.getSource()
                state = source_node
                """For all the links with a similar source node,find the action
                that minimizes distance to the goal"""
                for link in schemes:
                    if link.getSource() == state:
                        action = scheme.getCategory("id")
                        scheme_position = []
                        if action == 0:
                            # Get the row and append it to the position array
                            scheme_position.append(
                                int(state.getLabel()[0]))
                            # Append the col with the new col after moving left
                            scheme_position.append(
                                max(int(state.getLabel()[1]) - 1, 0))
                        elif action == 1:
                            scheme_position.append(
                                min(int(state.getLabel()[0]) + 1, 7))
                            scheme_position.append(
                                int(state.getLabel()[1]))
                        elif action == 2:
                            scheme_position.append(
                                int(state.getLabel()[0]))
                            scheme_position.append(
                                min(int(state.getLabel()[1]) + 1, 7))
                        elif action == 3:
                            scheme_position.append(
                                max(int(state.getLabel()[0]) - 1, 0))
                            scheme_position.append(
                                int(state.getLabel()[1]))
                        goal = [7, 7]
                        point1 = np.array(scheme_position)
                        point2 = np.array(goal)
                        distance = np.linalg.norm(point2 - point1)
                        min_distance = min(min_distance, distance)
                        if distance <= min_distance:
                            current_scheme = scheme
                instantiated_schemes.append(current_scheme)
                self.add_scheme(self.state, current_scheme)
        self.logger.debug(f"Learned {len(instantiated_schemes)} new action "
                          f"scheme(s) that minimize distance to goal")
        return current_scheme

