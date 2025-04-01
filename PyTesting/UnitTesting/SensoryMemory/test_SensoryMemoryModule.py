import pytest

from unittest.mock import Mock

from PyTesting.UnitTesting.ActionSelection.test_ActionSelection import sensory_motor_mem
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.Environment.FrozenLakeEnvironment import FrozenLake

"""
This provided PyTest is for the Sensory Memory ModuleSubject:
It provides tests for the specific functions: 
As development continues these are subject to change or update as the module does. 
Test Cases: 
"""

#Testing the Sensory memory & sensory memory impl initialization
def test_sensoryMemory_initialization():
    sensory_memory = SensoryMemory()
    assert sensory_memory is not None

def test_sensoryMemoryImpl_Initialization():
    smi = SensoryMemoryImpl()
    assert smi.sensor is None
    assert smi.processors == {}
    assert smi.stimuli is None
    assert smi.position is None
    assert smi.state is None
    assert smi.links == []
    assert smi.sensor_dict == {}
    assert smi.processor_dict == {}

#Tesing the notify function
def test_notify():
    smi = SensoryMemoryImpl()
    env = FrozenLake() #Testing with the Frozen Lake Environment
    smi.notify(env)
    assert smi.stimuli == env.get_stimuli()
    assert smi.position == env.get_position()
    assert smi.state == env.__getstate__()

"""
implement run sensors test method
"""
