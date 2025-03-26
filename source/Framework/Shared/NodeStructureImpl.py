from win32comext.shell.shellcon import LOF_DEFAULT

from source.Framework.Shared.LinkImpl import LinkImpl
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructure import NodeStructure

DEFAULT_NODE = NodeImpl()
DEFAULT_NODE_TYPE = DEFAULT_NODE.getLabel()
DEFAULT_LINK = LinkImpl()
DEFAULT_LINK_TYPE = DEFAULT_LINK.getCategory()

class NodeStructureImpl(NodeStructure):
    def __init__(self):
        super().__init__()

    def addDefaultNode(self, label, activation, removal_threshold):
        self.addNode(label, activation, removal_threshold)

    def addDefaultNode_(self, node):
        self.nodes.append(node)

    def addDefaultNodes(self, nodes):
        for node in nodes:
            if node not in self.nodes:
                self.nodes.append(node)

    def addNode(self, label, activation, removal_threshold):
        node = NodeImpl()
        node.setLabel(label)
        node.setActivation(activation)
        if node not in self.nodes:
            self.nodes.append(node)

    def addNode_(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def addDefaultLink(self, source_node, sink_link, category, activation,
                       removal_threshold):
        self.addDefaultLink_(source_node.getId(), sink_link.getCategory["id"],
                     category, activation, removal_threshold)

    def addDefaultLink_(self, source_id, sink_id, category, activation,
                       removal_threshold):
        self.addLink(DEFAULT_LINK_TYPE, source_id, sink_id, category,
                     activation, removal_threshold)

    def addDefaultLink__(self, link):
        if link not in self.links:
            self.links.append(link)

    def addDefaultLinks(self, links):
        for link in links:
            if link not in self.links:
                self.links.append(link)

    def addLink(self, link_type, source_id, sink_id, category, activation,
                removal_threshold):
        link = LinkImpl()
        link.setCategory(link_type["id"], link_type["label"])
        link.setSource(source_id)
        link.setSink(sink_id)
        link.setActivation(activation)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeLink(self, link):
        self.links.remove(link)

    def clearLinks(self):
        self.links.clear()

    def clearNodeStructure(self):
        self.links.clear()
        self.nodes.clear()

    def containsNode(self, node):
        return node in self.nodes

    def containsNode_(self, node_id):
        for node in self.nodes:
            if node.getId() == node_id:
                return True
        return False

    def containsLink(self, link):
        return link in self.links

    def containsLink_(self, link_id):
        for link in self.links:
            if link.getCategory()["link_id"] == link_id:
                return True
        return False

    def mergeWith(self, node_structure):
        for node in node_structure.nodes:
            self.nodes.append(node)
        for link in node_structure.links:
            self.links.append(link)

    def copy(self):
        return self

    def decayNodeStructure(self, ticks):
        for node in self.nodes:
            node.decayNodeStructure(ticks)

    def getNode(self, node_id):
        for node in self.nodes:
            if node.getId() == node_id:
                return node

    def getNodes(self):
        return self.nodes

    def getLink(self, link_id):
        for link in self.links:
            if link.getCategory()["id"] == link_id:
                return link

    def getLinks(self):
        return self.links

    def getLinks_cat(self, category):
        for link in self.links:
            if link.getCategory() == category:
                return link

    def getAttachedLinks(self, link):
        pass
    def getAttachedLinks_cat(self, link, category):
        pass
    #Returns a list of all sink link objects connected to node
    def getConnectedSinks(self, node):
        sink_links = []
        for link in self.links:
            if link.getSource() == node:
                sink_links.append(link)
        return sink_links

    # Returns a list of all node objects connected to link as a source
    def getConnectedSources(self, link):
        sink_nodes = []
        for node in self.nodes:
            if node.getSource() == link:
                sink_nodes.append(node)
        return sink_nodes

    def getNodeCount(self):
        return self.nodes.count()

    def getLinkCount(self):
        return self.links.count()

    def getDefaultNodeType(self):
        return DEFAULT_NODE_TYPE

    def getDefaultLinkType(self):
        return DEFAULT_LINK_TYPE

    def getSubgraph(self, nodes, distance):
        pass
    def getSubgraph_(self, nodes, distance, threshold):
        pass