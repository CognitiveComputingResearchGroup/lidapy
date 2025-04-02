#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import pytest
import logging

from source.PAM.PAM import PerceptualAssociativeMemory
from source.PAM.PAM_Impl import PAMImpl

"""
This provided PyTest is for the Perceptual Associative Memory (PAM) and PAMImpl.
As development continues these are subject to change or update as the module does. 
Test Cases: 
"""

"""
Generating example classes for the dependencies: NodeImpl and NodeStructureImpl
NodeImpl: Representing an individual memory node
NodeStructureImpl: Storing and managing the nodes
"""
class exampleNode:
    #initializing the node with default id, activation and label
    def __init__(self, id=0):
        self.id = id
        self.activation = 0.0
        self.label = ""

    def setId(self, id): #Setting the Id for the Node
        self.id = id
    def getId(self): #Get the current id for the node
        return self.id
    def setActivation(self, a): #Set the activation level for the node
        self.activation = a
    def getActivation(self): #Retrieve the current activation of the node
        return self.activation
    def setLabel(self, label): #Set the label for the node
        self.label = label
    def getLinks(self): #Return an empty list representing no links
        return [] #Empty list just for testing purposes
    def decay(self, rate): #Decrease the activation by a given rate
        self.activation -= rate
    def isRemovable(self): #Determinr if the node is removable based on activation
        return self.activation < 0.1 #If low it can be removed

from source.Framework.Shared.ActivatibleImpl import ActivatibleImpl
from source.Framework.Shared.Link import Link

class exampleLink:
    # initializing the link with default id, activation and label
    def __init__(self):
        self.grounding_pam_link = None
        self.id = 0
        self.source = None
        self.sink = None
        self.label = "TestLink"
        self.category = {"id" : self.id,
                         "label" : self.label}
        self.type = None

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def getSink(self):
        return self.sink

    def setType(self, link_type):
        self.type = link_type

    def getType(self):
        return self.type

    def setSink(self, sink):
        self.sink = sink

    def getCategory(self, key):
        return self.category[key]

    def setCategory(self, id, label):
        self.category["id"] = id
        self.category["label"] = label

    def setGroundingPamLink(self, grounding_pam_link):
        self.grounding_pam_link = grounding_pam_link

    def getGroundingPamLink(self):
        return self.grounding_pam_link

class exampleNodeStructure:
   #initializing node structure with empty nodes and links
    def __init__(self):
        self.nodes = []
        self.links = []

    def addNode_(self, node): #add a node to the structure
        self.nodes.append(node)
    def getNodes(self): #get all nodes in the structure
        return self.nodes
    def remove(self, node): #remove a node from the structure
        if node in self.nodes:
            self.nodes.remove(node)
    def addDefaultLink(self, source, target, meta, a, b):
        if not source in self.getConnectedSources(target):
            target.setSource(source.getId())
            target.setCategory(meta["id"], meta["label"])
            self.links.append(target)
    def getConnectedSinks(self, node):
        links = []
        for link in self.links:
            if link.getSource() == node.getId():
                links.append(link)
        return links
    def getConnectedSources(self, link):
        nodes = []
        for node in self.nodes:
            if node.getId() == link.getSource():
                nodes.append(node)
        return nodes

#Example logger to avoid excessive testing output
def getLogger(name):
    logger = logging.getLogger(name) #Getting a logger instance with a name
    logger.setLevel(logging.DEBUG) #set the logging level to DEBUG (capturing all levels of messages)
    if not logger.handlers: #Checking if the logger already contains handlers to avoid additional
        handler = logging.StreamHandler() #Generating a stream handler to log to console
        handler.setFormatter(logging.Formatter('%(message)s')) #Set the format (only the message part)
        logger.addHandler(handler) #Adding the handler to the logger
    return logger

"""Patching the example dependencies to the PAM and PAMImpl"""
#Assigning the example node structure to the NodeStructureImpl
PerceptualAssociativeMemory.NodeStructureImpl = exampleNodeStructure()
#Assigning the example node structure to the NodeStructureImpl to PAM
PAMImpl.NodeStructureImpl = exampleNodeStructure()
#Assigning the example NodeImpl to the PAMImpl
PAMImpl.NodeImpl = exampleNode()
#Assigning a logger to the PAM and PAMImpl
PerceptualAssociativeMemory.getLogger = staticmethod(getLogger)
PAMImpl.getLogger = staticmethod(getLogger)

"""
Generating the Test Cases
"""
#Add Associations
def test_add_association():
    """Testing a new node is stored when this method is called"""
    pam = PerceptualAssociativeMemory()
    testNode = exampleNode()

    #Before adding, ensuring that the node is not present
    assert testNode not in pam.associations.getNodes()

    pam.add_association(testNode)

    #After adding, the test node should be present
    assert testNode in pam.associations.getNodes()

#Retreiving Association (NOT PASSABLE YET)
def test_retrieve_association():
    """ Testing the function retrieve association"""
    pam = PerceptualAssociativeMemory()
    testNode = exampleNode(id=1)
    testLink = exampleLink()
    pam.associations = exampleNodeStructure()

    #Before storing, the retrieval should return the node
    result = pam.retrieve_association(testNode)

    """Should return None when the node is not within the association"""
    assert result is None

    pam.add_association(testNode)
    result = pam.retrieve_association(testNode)
    """Should return an empty list when the node is within the association
           but the node is not a source for any links"""
    assert len(result) == 0

    pam.associations.addDefaultLink(testNode, testLink, {"id": 0,
                                                         "label": "test"},
                                                                0,0)

    result = pam.retrieve_association(testNode)
    assert len(result) > 0
    assert testLink in result

    """#add the node and simulate the connection
    pam.add_association(testNode)
    connected_node = exampleNode(id=2)

    #simulating as association
    pam.associations.links = {testNode: [connected_node]}

    result = pam.retrieve_association(testNode)
    assert result == [connected_node] #Linked node should be retrieved"""

#Testing the get_stored_nodes function
def test_get_stored_nodes():
    #Testing the PAMImpl initializes with 16 nodes in its memory
    pamImpl = PAMImpl()
    storedNodes = pamImpl.get_stored_nodes()

    assert len(storedNodes) == 16 #PAMImpl should create 16 nodes upon initialization

#Testing Learn()
def test_learn():
    """ Learn should set the current cell appropriately """
    pamImpl = PAMImpl()

    #Creating a cue with position
    cue = {
        "params" : {
            "position" : {"row":1,"col":2},
            "state" : {"state":"active"}
        },
        "cue":[] #No surrounding links within this test
    }
    pamImpl.position = cue["params"]["position"]

    #before learning, current cell should be None
    assert pamImpl.current_cell is None

    #Calling learn and verify that the correct node is stored
    pamImpl.learn(cue)

    current_cell = pamImpl.current_cell
    assert current_cell is not None
    assert current_cell.getId() == 6 #Checking to see if the current node is active.