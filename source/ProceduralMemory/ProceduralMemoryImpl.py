#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo
import math
import string
from threading import Thread, RLock

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory


class ProceduralMemoryImpl(ProceduralMemory):
    def __init__(self):
        super().__init__()
        self.optimized_schemes = {}
        self.map_size = 7       #Map rows/columns max index
        self.goal = [self.map_size, self.map_size]
        self.similarity_min = 85.0
        
    def start(self, scheme):
        self.logger.debug(f"Initialized ProceduralMemory")
        self.scheme = scheme
        
    def notify(self, module):
        if isinstance(module, PAMImpl):
            self.state = module.get_state()
            associations = None

            associations = module.retrieve_association(self.state)
            for association in associations:
                if association.isRemovable():
                    module.associations.removeLink(association)

            """Get the closest_match to the scheme from surrounding
            link nodes"""
            self.activate_schemes(associations)
            self.notify_observers()

        elif isinstance(module, GlobalWorkSpaceImpl):
            winning_coalition = module.get_broadcast()
            broadcast = winning_coalition.getContent()
            self.logger.debug(f"Received conscious broadcast: {broadcast}")
            thread = Thread(target=self.learn, args=(broadcast,))
            thread.start()



    def activate_schemes(self, associations):
        schemes = self.get_closest_match(associations)
        if schemes:
            if isinstance(schemes, list):
                for scheme in schemes:
                    self.add_scheme(self.state, scheme)
                self.logger.debug(
                    f"Instantiated {len(schemes)} action scheme(s)")
            else:
                self.add_scheme(self.state, schemes)
                self.logger.debug(f"Instantiated single action scheme(s)")

    def get_direction(self, point1, point2):
        direction = []
        if point2[0] - point1[0] > 0:
            direction.append("right")
        elif point2[0] - point1[0] < 0:
            direction.append("left")
        if point2[1] - point1[1] > 0:
            direction.append("down")
        elif point2[1] - point1[1] < 0:
            direction.append("up")

        return direction

    def determine_direction(self, node1, node2):
        direction = None
        """If the nodes aren't similar, find the direction to the
        other node from the agent node"""
        if self.get_similarity(node1.getCategory("label"),
                              node2.getCategory("label")) == -1:
            node1_pam_link = node1.getGroundingPamLink()
            node1_x = (node1_pam_link.extended_id.sinkLinkCategory["position"]
                                                                        [0])
            node1_y = (node1_pam_link.extended_id.sinkLinkCategory["position"]
                                                                        [1])

            node2_pam_link = node2.getGroundingPamLink()
            node2_x = (node2_pam_link.extended_id.sinkLinkCategory["position"]
                                                                        [0])
            node2_y = (node2_pam_link.extended_id.sinkLinkCategory["position"]
                                                                        [1])

            direction =self.get_direction([node1_x, node1_y],
                               [node2_x, node2_y])
        return direction

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
        new_text = []
        for i in range(len(text)):
            new_text.append(text[i].lower())
        m = len(pattern)
        n = len(new_text)
        table = self.shift_table(pattern)
        i = m - 1
        while i <= n - 1:
            k = 0
            while k <= m - 1 and pattern[m - 1 - k] == new_text[i - k]:
                k = k + 1
            if k == m:
                return i - m + 1
            else:
                i = i + table[new_text[i]]
        return -1

    def get_similarity(self, scheme, word):
        similarity = self.horspool_matching(scheme, word)
        return similarity


    """Gets the link that closely matches the scheme"""
    def get_closest_match(self, linkables):
        goal_scheme = None
        content = None
        position = None
        for linkable in linkables:
            if isinstance(linkable, LinkImpl):
                content = linkable.label
            elif isinstance(linkable, NodeImpl):
                content = linkable.getLabel()["content"]

            if isinstance(content, dict):
                for key, value in content.items():
                    avoid_similarity = self.get_similarity(self.scheme[0],
                                                           value)
                    if avoid_similarity != -1:
                        linkables.remove(linkable)
                        avoid_similarity = -1
                        linkable.decay(0.05)

                    find_goal_similarity = self.get_similarity(self.scheme[1],
                                                               value)
                    if find_goal_similarity != -1:
                        goal_scheme = linkable
                        find_goal_similarity = -1
                        linkable.exciteActivation(0.05)
                        linkable.exciteIncentiveSalience(0.05)
                        break
            else:
                avoid_similarity = self.get_similarity(self.scheme[0], content)
                if avoid_similarity != -1:
                    linkables.remove(linkable)
                    avoid_similarity = -1
                    linkable.decay(0.05)

                find_goal_similarity = self.get_similarity(self.scheme[1],
                                                           content)
                if find_goal_similarity != -1:
                    goal_scheme = linkable
                    find_goal_similarity = -1
                    linkable.exciteActivation(0.05)
                    linkable.exciteIncentiveSalience(0.05)
                    break
            
        if goal_scheme:
            return goal_scheme
        return linkables

    """Updates the column, row value given a specific action"""
    def update_position(self, action, row, col):
        if action == 3:  # up
            row = max(row - 1, 0)
        elif action == 2:  # Right
            col = min(col + 1, self.map_size)
        elif action == 1:  # down
            row = min(row + 1, self.map_size)
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
        distance = self.similarity_min
        min_distance = distance
        current_scheme = None
        instantiated_schemes = []
        # Find the links with the shortest distance to the goal
        for scheme in schemes:
            position = scheme.getLabel()["position"]
            distance = self.closest_pair(distance,
                                         [position[0],
                                          self.goal[0]],
                                         [position[1],
                                          self.goal[1]])
            if distance < min_distance:
                min_distance = distance
                current_scheme = scheme
                instantiated_schemes.append(scheme)
                current_scheme.exciteActivation(0.5)
                current_scheme.exciteIncentiveSalience(0.3)
            


        self.logger.debug(f"Learned {len(instantiated_schemes)} new action "
                          f"scheme(s) that minimize(s) distance to goal")
        return instantiated_schemes

    def learn(self, broadcast):
        result = self.optimize_schemes(broadcast.getNodes())
        schemes = self.get_closest_match(broadcast.getNodes())
        wanted_schemes = []

        if len(result) > 0:
            for node in result:
                content = node.getLabel()
                if isinstance(content, dict):
                    for key, value in content.items():
                        if isinstance(schemes, list):
                            if key not in schemes:
                                self.add_scheme(node, key)
                                self.add_scheme_(node, key,
                                                 self.optimized_schemes)
                        else:
                            """Scheme is the goal or only wanted schemes"""
                            if key == schemes:
                                self.add_scheme(node, key)
                                self.add_scheme_(node, key,
                                                 self.optimized_schemes)
                                break


