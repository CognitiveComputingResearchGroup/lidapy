from email.errors import NonASCIILocalPartDefect

import pytest
import logging

from pygame import NOEVENT

from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
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
    def __init__(self, id=0):
        self.id = id
        self.activation = 0.0
        self.label = ""

    def setID(self, id):
        self.id = id
    def getID(self):
        return self.id
    def setActivation(self, a):
        self.activation = a
    def getActivation(self):
        return self.activation
    def setLabel(self, label):
        self.label = label
    def getLinks(self):
        return [] #Empty list just for testing purposes
    def decay(self, rate):
        self.activation -= rate
    def isRemovable(self):
        return self.activation < 0.1 #If low it can be removed

class exampleNodeStructure:
    def __init__(self):
        self.nodes = []
        self.links = {}

    def addNode_(self, node):
        self.nodes.append(node)
    def getNodes(self):
        return self.nodes
    def remove(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
    def addDefaultLink(self, source, target, meta, a, b):
        if source not in self.links:
            self.links[source] = []
        self.links[source].append(target)
    def getConnectedSinks(self, node):
        return self.links.getSource(node, [])

#Example logger to avoid excessive testing output
def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
    return logger

#Pathcing the example dependencies to the PAM and PAMImpl
PerceptualAssociativeMemory.NodeStructureImpl = exampleNodeStructure()
PAMImpl.NodeStructureImpl = exampleNodeStructure()
PAMImpl.NodeImpl = exampleNode()
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

    #Before storing, the retrieval should return the node
    result = pam.retrieve_association(testNode)
    assert result is None #Should return None when the node is not within the association

    #add the node and simulate the connection
    pam.add_association(testNode)
    connected_node = exampleNode(id=2)

    #simulating as association
    pam.associations.links = {testNode: [connected_node]}

    result = pam.retrieve_association(testNode)
    assert result == [connected_node] #Linked node should be retrieved

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

    #before learning, current cell should be None
    assert pamImpl.current_cell is None

    #Calling learn and verify that the correct node is stored
    pamImpl.learn(cue)

    current_cell = pamImpl.current_cell
    assert current_cell is not None
    assert current_cell.getId() == 6 #Checking to see if the current node is active.
