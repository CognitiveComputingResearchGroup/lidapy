#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import difflib
import math
from time import sleep
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

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            sleep(0.2)
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            links = broadcast.getLinks()
            self.learn(links)

    def activate_schemes(self, associations):
        schemes = None
        if associations is not None:
            """Get only the links that match the scheme"""
            schemes = self.get_closest_match(associations)

        if isinstance(schemes, list):
            for scheme in schemes:
                self.add_scheme(self.state, scheme)
                if scheme.isRemovable():
                    self.schemes[self.state].remove(scheme)
            self.logger.debug(f"Instantiated {len(schemes)} action scheme(s)")
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

    def get_similarity(self, scheme, link):
        label = link.getCategory("label")
        similarity = self.horspool_matching(scheme, label)
        return similarity


    """Gets the link that closely matches the scheme"""
    def get_closest_match(self, links):
        unwanted_scheme = None
        wanted_scheme = None

        for link in links:
            avoid_hole_similarity = self.get_similarity(self.scheme[0], link)
            if avoid_hole_similarity > -1:
                unwanted_scheme = link
                link.decay(0.05)

            find_goal_similarity = self.get_similarity(self.scheme[1], link)
            if find_goal_similarity > -1:
                wanted_scheme = link
                link.exciteActivation(0.05)
                link.exciteIncentiveSalience(0.05)

        if unwanted_scheme is not None:
            links.remove(unwanted_scheme)
        if wanted_scheme is not None:
            return wanted_scheme
        return links

    """Updates the column, row value given a specific action"""
    def update_position(self, action, row, col):
        if action == 3:  # up
            row = max(row - 1, 0)
        elif action == 2:  # Right
            col = min(col + 1, 7)
        elif action == 1:  # down
            row = min(row + 1, 7)
        elif action == 0:  # Left
            col = max(col - 1, 0)
        return row, col

    """Finds the distance between a pair of coordinates x, y"""
    def closest_pair(self, x_points, y_points):
        d = 64.0
        d = min(d, math.sqrt(math.pow(x_points[1] - x_points[0], 2)
                                      + math.pow(y_points[1] - y_points[0],
                                                 2)))
        return d

    """Finds the shortest distance between a scheme and the goal"""
    def optimize_schemes(self, schemes):
        min_distance = 64
        current_scheme = None
        instantiated_schemes = []

        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            x_points = []
            y_points = []
            if isinstance(scheme, LinkImpl):
                source_node = scheme.getSource()
                state = source_node
                """For all the links with a similar source node,find the action
                scheme that minimizes distance to the goal"""
                if state == self.state:
                    action = scheme.getCategory("id")
                    scheme_position = []
                    x, y = self.update_position(action,
                                                int(self.state.getLabel()[0]),
                                                int(self.state.getLabel()[1]))
                    x_points.append(x)      # Link row
                    y_points.append(y)      # Link column
                    x_points.append(7)      # Goal row
                    y_points.append(7)      # Goal column
                    distance = self.closest_pair(x_points, y_points)
                    if distance < min_distance:
                        min_distance = distance
                        current_scheme = scheme

        if current_scheme:
            instantiated_schemes.append(current_scheme)
            current_scheme.exciteActivation(0.05)
            current_scheme.exciteIncentiveSalience(0.05)
            self.add_scheme_(self.state, current_scheme,self.optimized_schemes)
        self.logger.debug(f"Learned {len(instantiated_schemes)} new action "
                          f"scheme(s) that minimize(s) distance to goal")
        return current_scheme

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


