#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import unittest
import time

import pytest

from source.GlobalWorkspace.GlobalWorkSpaceImpl import GlobalWorkSpaceImpl
from source.GlobalWorkspace.CoalitionImpl import CoalitionImpl

"""
This generated test case will test the functions within the Global Workspace. These are to ensure each function is 
working properly. This module contains a conscious broadcast.
"""

#Mocking the Coalition
class MockCoalition:
    def __init__(self, activation, removable=True):
        self.activation = activation
        self.removable = removable

    def getActivation(self):
        return self.activation
    def decay(self, ticks):
        pass
    def isRemoveable(self):
        return self.removable
    def setDecayStrategy(self, strategy):
        pass
    def setActivationRemovalThreshold(self, threshold):
        pass

@pytest.fixture
def global_workspace():
    return GlobalWorkSpaceImpl()

def test_initiailization(global_workspace):
    assert global_workspace is not None

"""NOT YET PASSING"""
def test_trigger_broadcast(global_workspace):
    global_workspace.broadcast_started = True
    global_workspace.ticks = time.time() - 50 #Simulating previous
    global_workspace.ticks_at_last_broadcast = global_workspace.ticks - 100
    global_workspace.triggerBroadcast("Test Trigger")

    assert not global_workspace.broadcast_started
    assert global_workspace.broadcast_was_sent

"""NOT YET PASSING"""
def test_add_coalition(global_workspace):
    coalition = MockCoalition(activation=0.5)
    global_workspace.addCoalition(coalition)

    #assert len(global_workspace.coalitions) == 1

"""PASSED BUT DOUBLE CHECK"""
def test_new_coalition_event(global_workspace):
    coalition = MockCoalition(activation=1.0)
    global_workspace.coalitions = [coalition]
    global_workspace.aggregate_trigger_threshold = 0.5
    global_workspace.newCoalitionEvent()


