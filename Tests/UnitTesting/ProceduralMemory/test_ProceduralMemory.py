#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import pytest

from unittest.mock import Mock
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.LinkImpl import LinkImpl

"""
This provided PyTest is for the Procedural Memory Module:
It provides tests for the specific functions: add_scheme, get_action
As development continues these are subject to change or update as the module does. 
Test Cases: 
"""

@pytest.fixture
def procedural_memory():
    return ProceduralMemoryImpl()

def test_initialization(procedural_memory):
    assert procedural_memory.logger is not None

"""IN WORKING PROCESSES & ADD NOTIFY WITH GW"""
def test_notify_with_PAM(procedural_memory):
    #Mocking the PAM
    module = PAMImpl()
    module.current_cell = NodeImpl()
    module.associations = NodeStructureImpl()
    assert isinstance(module.current_cell, NodeImpl) is True

    module.add_association(module.current_cell)
    default_link = LinkImpl()
    default_link.setSource(module.current_cell.getId())
    links = [default_link]
    module.associations.addLinks(links, "default")

    procedural_memory.scheme = ["avoid hole", "seek goal"]
    module.add_observer(procedural_memory)
    module.notify_observers()

    assert procedural_memory.__getstate__() == module.current_cell
    assert default_link in module.retrieve_association(module.current_cell)

def test_activate_Scheme(procedural_memory):
    link1 = LinkImpl()
    link1.setCategory(2, "hole")
    link2 = LinkImpl()
    link2.setCategory(1, "goal")
    link3 = LinkImpl()
    link3.setCategory(3, "safe")
    link4 = LinkImpl()
    link4.setCategory(0, "start")

    associations = [link1, link2, link3, link4]
    procedural_memory.scheme = ["avoid hole", "seek goal"]
    procedural_memory.activate_schemes(associations)
    assert procedural_memory.get_closest_match(associations) == link2

def test_seek_goal(procedural_memory):
    link1 = LinkImpl()
    link1.setCategory(2, "hole")
    link2 = LinkImpl()
    link2.setCategory(1, "safe")
    link3 = LinkImpl()
    link3.setCategory(3, "safe")
    link4 = LinkImpl()
    link4.setCategory(0, "start")

    procedural_memory.scheme = ["avoid hole", "seek goal"]
    procedural_memory.state = NodeImpl()

    # Position on the frozen lake environment map (row, col)
    procedural_memory.state.setLabel("03")

    associations = [link1, link2, link3, link4]
    result = procedural_memory.seek_goal(associations)

    assert result is not None