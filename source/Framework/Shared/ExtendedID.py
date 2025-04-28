

class ExtendedID:
    def __init__(self):
        self.linkCategory = None
        self.sourceNodeId = None
        self.sinkLinkCategory = None
        self.sinkNode1Id = None
        self.sinkNode2Id = None

    def setLinkCategory(self, link_category):
        self.linkCategory = link_category

    def setSourceNodeId(self, source_node_id):
        self.sourceNodeId = source_node_id

    def setSinkLinkCategory(self, sink_link_category):
        self.sinkLinkCategory = sink_link_category

    def setSinkNode1Id(self, sink_node1_id):
        self.sinkNode1Id = sink_node1_id

    def setSinkNode2Id(self, sink_node2_id):
        self.sinkNode2Id = sink_node2_id

    def getSourceNodeId(self):
        return self.sourceNodeId

    """True if the link is between two nodes"""
    def isSimpleLink(self):
        return self.linkCategory is not None and self.sinkLinkCategory is None

    def isNode(self):
        return self.linkCategory is None

    """True if the link is between a node and a link"""
    def isComplexLink(self):
        return self.linkCategory is not None and self.sinkLinkCategory is None
