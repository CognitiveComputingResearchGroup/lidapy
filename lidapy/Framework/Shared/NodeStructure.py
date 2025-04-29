from Module.Initialization.DefaultLogger import getLogger


class NodeStructure:
    def __init__(self):
        self.logger = getLogger(self.__class__.__name__).logger
        self.nodes = []
        self.links = []

    def addDefaultNode(self, label, activation, removal_threshold):
        pass
    def addDefaultNode_(self, node):
        pass
    def addDefaultNodes(self, nodes):
        pass
    def addNode(self, label, activation, removal_threshold):
        pass
    def addNode_(self, node):
        pass
    def addDefaultLink(self, source_node, sink_link, category, activation,
                       removal_threshold):
        pass
    def addDefaultLink_(self, source_id, sink_id, category, activation,
                       removal_threshold):
        pass
    def addDefaultLink__(self, link):
        pass
    def addDefaultLinks(self, links):
        pass
    def addLink(self, link_type, source_id, sink_id, category, activation,
                removal_threshold):
        pass
    def addLinks(self, links, link_type):
        pass

    def setLinkType(self, link, link_type):
        pass

    def getLinkType(self, link):
        pass
    def removeNode(self, node):
        pass
    def removeLink(self, link):
        pass
    def clearLinks(self):
        pass
    def clearNodeStructure(self):
        pass
    def containsNode(self, node):
        pass
    def containsNode_(self, node_id):
        pass
    def containsLink(self, link):
        pass
    def containsLink_(self, link_id):
        pass
    def mergeWith(self, node_structure):
        pass
    def copy(self):
        pass
    def decayNodeStructure(self, ticks):
        pass
    def getNode(self, node_id):
        pass
    def getNodes(self):
        pass
    def getLink(self, link_id):
        pass
    def getLinks(self):
        pass
    def getLinks_cat(self, category):
        pass
    def getAttachedLinks(self, link):
        pass
    def getAttachedLinks_cat(self, link, category):
        pass
    #Returns a list of all sink link objects connected to node
    def getConnectedSinks(self, node):
        pass
    # Returns a list of all node objects connected to link as a source
    def getConnectedSources(self, link):
        pass
    def getNodeCount(self):
        pass
    def getLinkCount(self):
        pass
    def getDefaultNodeType(self):
        pass
    def getDefaultLinkType(self):
        pass
    def getSubgraph(self, nodes, distance):
        pass
    def getSubgraph_(self, nodes, distance, threshold):
        pass