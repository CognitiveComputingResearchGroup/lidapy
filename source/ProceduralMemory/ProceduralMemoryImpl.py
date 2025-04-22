#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import math
from threading import RLock
import string


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
            self.activate_schemes(associations)
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
        goal_scheme = None
        unwanted_schemes = []
        lock = RLock()
        with lock:
            for link in links:
                avoid_hole_similarity = self.get_similarity(self.scheme[0],
                                                            link)
                if avoid_hole_similarity != -1:
                    unwanted_schemes.append(link)
                    avoid_hole_similarity = -1

                find_goal_similarity = self.get_similarity(self.scheme[1],
                                                           link)
                if find_goal_similarity != -1:
                    goal_scheme = link
                    link.exciteActivation(0.05)
                    link.exciteIncentiveSalience(0.05)
                    find_goal_similarity = -1
                    break

        if len(unwanted_schemes) > 0:
            for scheme in unwanted_schemes:
                scheme.decay(0.3)
                links.remove(scheme)
        if goal_scheme is not None:
            return goal_scheme
        return links

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
    def closest_pair(self, x_points, y_points):
        d = 64.0
        d = min(d, math.sqrt(math.pow(x_points[1] - x_points[0], 2)
                                      + math.pow(y_points[1] - y_points[0],
                                                 2)))
        return d

    """Finds the shortest distance between a scheme and the goal"""
    def optimize_schemes(self, schemes):
        min_distance = 20
        current_scheme = None
        instantiated_schemes = []
        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            x_points = []
            y_points = []
            source = scheme.getSource()
            scheme_position = []
            if isinstance(source, NodeImpl):
                stored_schemes = self.get_schemes(source)
                """Optimize stored schemes based on state from coalition"""
                if stored_schemes is not None and len(stored_schemes) > 0:
                    for link in stored_schemes:
                        action = link.getCategory("id")
                        x, y = self.update_position(action,
                                                    int(source.getLabel()[0]),
                                                    int(source.getLabel()[1]))
                        x_points.append(x)  # Link row
                        y_points.append(y)  # Link column
                        x_points.append(3)  # Goal row
                        y_points.append(3)  # Goal column
                        distance = self.closest_pair(x_points,
                                                     y_points)
                        if distance < min_distance:
                            min_distance = distance
                            current_scheme = scheme
                    if current_scheme:
                        instantiated_schemes.append(current_scheme)
                        current_scheme.exciteActivation(0.05)
                        current_scheme.exciteIncentiveSalience(0.05)
                else:
                    """Store new links otherwise from coalition"""
                    action = scheme.getCategory("id")
                    x, y = self.update_position(action,
                                                int(source.getLabel()[0]),
                                                int(source.getLabel()[1]))
                    x_points.append(x)  # Link row
                    y_points.append(y)  # Link column
                    x_points.append(3)  # Goal row
                    y_points.append(3)  # Goal column
                    distance = self.closest_pair(x_points,
                                                 y_points)
                    if distance < min_distance:
                        min_distance = distance
                        current_scheme = scheme
        if current_scheme:
            instantiated_schemes.append(current_scheme)
            current_scheme.exciteActivation(0.05)
            current_scheme.exciteIncentiveSalience(0.05)
            self.add_scheme_(current_scheme.getSource(), current_scheme,
                                         self.optimized_schemes)
            self.add_scheme(current_scheme.getSource(), current_scheme)

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


