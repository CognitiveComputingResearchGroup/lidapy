import pytest
from src.SensoryMemory.SensoryMemory import SensoryMemory
from unittest.mock import Mock #utilize to mock the dependencies

"""
This provided PyTest is for the Sensory Memory ModuleSubject:
It provides tests for the specific functions: run_sensors, add_listener
As development continues these are subject to change or update as the module does. 
Test Cases: TC-035, TC-036.
"""

@pytest.fixture
def environment():
    #Generating a Mock Environment
    env = Mock()
    env.reset.return_value = ('mock_state', 'mock_infor', 'mock-col', 'mock-row')
    env.action_space.sample.return_value = 'mock_action'
    return env

@pytest.fixture
def mock_pam():
    #Generating a Mock PAM
    pam = Mock()
    pam.retrieve_associations.return_value = 'mock_percept'
    return pam

@pytest.fixture
def sensory_memory(environment, mock_pam):
    #initialzing into the sensory memory
    return SensoryMemory(environment, mock_pam)

def test_add_sensory_listener(sensory_memory):
    #Testing the listener
    listener = Mock()
    sensory_memory.add_sensory_listener(listener)
    assert listener in sensory_memory.listeners

def test_run_sensors(sensory_memory, environment, mock_pam):
    #preparing the procedural memory
    procedural_memory = Mock()
    procedural_memory.add_scheme = Mock()

    state, percept, action, environment, col, row = sensory_memory.run_sensors(procedural_memory, 0)

    assert state == 'mock_state'
    assert percept == 'mock_percept'
    assert action == 'mock_action'
    assert environment == environment
    assert col == 'mock-col'
    assert row == 'mock-row'

    procedural_memory.add_scheme.assert_called_with('state-0', 'mock_action')
    mock_pam.retrieve_associations.assert_called_with('state-0')