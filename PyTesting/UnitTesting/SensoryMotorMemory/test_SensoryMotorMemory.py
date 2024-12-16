import pytest

from src.Memphis.ccrg.LIDA.SensoryMotorMemory.SensoryMotorMemoryImpl import SensoryMotorMemoryImpl
from unittest.mock import Mock

"""
This provided PyTest is for the Sensory Motor Memory Module:
It provideds test for the specific functions: add_sensory_listener, receieve_action,
    send_action_exection_command. 
As development continues these are subject to change or update as the module does. 
Test Cases: TC-044, TC-045, and TC-046.
"""

def test_add_sensory_listener():
    sensory_memory = SensoryMotorMemoryImpl(action = None, environment = Mock())
    listener = Mock() #Mock listener
    sensory_memory.add_sensory_listener(listener)
    assert listener in sensory_memory.listeners

def test_receive_action():
    env = Mock() #Generating a mock environment for testing
    env.step.return_value = ('state', 'reward', 'done', 'truncated', 'info')
    sensory_memory = SensoryMotorMemoryImpl(action = None, environment = env)
    action = "some_action"
    state, reward, done, truncated, info = sensory_memory.receive_action(action)

    #Assertions
    assert state == 'state'
    assert reward == 'reward'
    assert done == 'done'
    assert truncated == 'truncated'
    assert info == 'info'

def test_send_action_execution_command():
    env = Mock() #Generating mock environment for testing
    expected_output = ('state', 'reward', 'done', 'truncated', 'info')
    env.step.return_value = expected_output
    sensory_memory = SensoryMotorMemoryImpl(action = None, environment = env)
    result = sensory_memory.send_action_execution_command("some_action_plan")

    #Assertion
    assert result == expected_output
