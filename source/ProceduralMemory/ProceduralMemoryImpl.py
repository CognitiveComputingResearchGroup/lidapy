#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import math
from threading import RLock
import string

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()
        self.optimized_schemes = {}
        self.logger.debug(f"Initialized ProceduralMemory")

    def notify(self, module):
        if isinstance(module, PAMImpl):
            self.state = module.get_state()
            associations = None

            if isinstance(self.state, NodeImpl):
                associations = module.retrieve_association(self.state)
                for association in associations:
                    if association.isRemovable():
                        module.associations.remove(association)

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            nodes = broadcast.getNodes()
            self.learn(nodes)

    def activate_schemes(self, associations):
        schemes = None
        if associations is not None:
            """Get only the links that match the scheme"""
            schemes = self.get_closest_match(associations)
        if isinstance(schemes, list):
            for scheme in associations:
                position = scheme.getCategory("label")["position"]
                if isinstance(position, dict):
                    for key, value in position.items():
                        if key not in schemes:
                            self.add_scheme(self.state, {key : value})

            self.logger.debug(f"Instantiated {len(associations) - len(schemes)} "
                                f"action scheme(s)")
        else:
            self.add_scheme(self.state, schemes)
            self.logger.debug("Instantiated single action scheme")

    def shift_table(self, text):
        table = {}
        alphabet = []
        shift_table = []
        for char in string.printable:
            alphabet.append(char)
            table[char] = len(text)
            if char in text:
                shift_table.append(len(text) - 1 - text.index(char))
                table[char] = len(text) - 1 - text.index(char)
        return table

    def horspool_matching(self, text, pattern):
        m = len(pattern)
        n = len(text)
        table = self.shift_table(pattern)
        i = m - 1
        while i <= n - 1:
            k = 0
            while k <= m - 1 and pattern[m - 1 - k] == text[i - k]:
                k = k + 1
            if k == m:
                return i - m + 1
            else:
                i = i + table[text[i]]
        return -1

    def get_similarity(self, scheme, word):
        similarity = self.horspool_matching(scheme, word)
        return similarity


    """Gets the link that closely matches the scheme"""
    def get_closest_match(self, linkables):
        goal_scheme = None
        unwanted_schemes = []
        lock = RLock()
        with lock:
            for linkable in linkables:
                if isinstance(linkable, LinkImpl):
                    position = linkable.getCategory("label")["content"]
                elif isinstance(linkable, NodeImpl):
                    position =linkable.label["content"]

                if isinstance(position, dict):
                    for key, value in position.items():
                        avoid_hole_similarity = self.get_similarity(
                            self.scheme[0], value)
                        if avoid_hole_similarity != -1:
                            unwanted_schemes.append(key)
                            avoid_hole_similarity = -1

                        find_goal_similarity = self.get_similarity(
                            self.scheme[1], value)
                        if find_goal_similarity != -1:
                            goal_scheme = {key : value}
                            linkable.exciteActivation(0.05)
                            linkable.exciteIncentiveSalience(0.05)
                            find_goal_similarity = -1
                            break

        if goal_scheme is not None:
            return goal_scheme
        return unwanted_schemes

    """Updates the column, row value given a specific action"""
    def update_position(self, action, row, col):
        if action == 3:  # up
            row = max(row - 1, 0)
        elif action == 2:  # Right
            col = min(col + 1, 3)
        elif action == 1:  # down
            row = min(row + 1, 3)
        elif action == 0:  # Left
            col = max(col - 1, 0)
        return row, col

    """Finds the distance between a pair of coordinates x, y"""
    def closest_pair(self, distance, x_points, y_points):
        d = distance
        i = 0
        j = i + 1
        current_scheme = None
        for i in range(i, len(x_points) - 1):
            for j in range(j, len(x_points)):
                d = min(d, math.sqrt(math.pow(x_points[j] - x_points[i], 2)
                                      + math.pow(y_points[j] - y_points[i],
                                                 2)))
        return d

    """Finds the shortest distance between a scheme and the goal"""
    def optimize_schemes(self, schemes):
        distance = 4.0
        min_distance = distance
        current_scheme = None
        instantiated_schemes = []
        """Change constant to FrozenLake Map final state"""
        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            if 64 - scheme.id < min_distance:
                min_distance = 64 - scheme.id
                current_scheme = scheme
                current_scheme.exciteActivation(0.05)
                instantiated_schemes.append(current_scheme)

        self.logger.debug(f"Learned {len(instantiated_schemes)} new action "
                          f"scheme(s) that minimize(s) distance to goal")

    def learn(self, broadcast):
        result = self.get_closest_match(broadcast)
        wanted_schemes = []
        """If closest match returns more than one link, optimize results"""
        if isinstance(result, list):
            for scheme in broadcast:
                position = scheme.extended_id.sinkLinkCategory["position"]
                for key, value in position.items():
                    if key not in result:
                        wanted_schemes.append(scheme)
            self.optimize_schemes(wanted_schemes)
        else:
            """Scheme leads to goal if single link is returned"""
            current_scheme = result


