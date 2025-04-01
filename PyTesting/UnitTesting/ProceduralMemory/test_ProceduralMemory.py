import pytest

from unittest.mock import Mock
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.PAM.PAM import PerceptualAssociativeMemory
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from source.Framework.Shared.NodeImpl import NodeImpl
from source.Framework.Shared.LinkImpl import LinkImpl

"""
This provided PyTest is for the Procedural Memory ModuleSubject:
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
    module = Mock(spec=PerceptualAssociativeMemory)
    state = Mock(spec=NodeImpl)
    module.__getstate__.return_value = state
    module.retrieve_association.return_value = ['assoication1','association2']

    procedural_memory.notify(module)

    assert procedural_memory.state == state

def test_activate_Scheme(procedural_memory):
    associations = [Mock(spec=LinkImpl), Mock(spec=NodeImpl)]
    procedural_memory.activate_Scheme(associations)

"""
Add testing for functions:
    Learn
    get closest match
    seek goal
"""