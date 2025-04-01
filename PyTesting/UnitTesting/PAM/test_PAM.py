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

    def setID(self, id): #Setting the Id for the Node
        self.id = id
    def getID(self): #Get the current id for the node
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

class exampleNodeStructure:
   #initializing node structure with empty nodes and links
    def __init__(self):
        self.nodes = []
        self.links = {}

    def addNode_(self, node): #add a node to the structure
        self.nodes.append(node)
    def getNodes(self): #get all nodes in the structure
        return self.nodes
    def remove(self, node): #remove a node from the structure
        if node in self.nodes:
            self.nodes.remove(node)
    def addDefaultLink(self, source, target, meta, a, b):
        if source not in self.links:
            self.links[source] = []
        self.links[source].append(target)
    def getConnectedSinks(self, node):
        return self.links.get(node, [])

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
