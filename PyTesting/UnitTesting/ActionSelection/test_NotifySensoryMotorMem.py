import pytest
from unittest.mock import MagicMock

from src.ActionSelection.ActionSelection import ActionSelection
from src.SensoryMotorMemory.SensoryMotorMemoryImpl import (
                                                        SensoryMotorMemoryImpl)
from src.ProceduralMemory.ProceduralMemory import ProceduralMemory

#initializing resources
@pytest.fixture
def test_action_select():
    return ActionSelection

#initializing resources
@pytest.fixture
def test_sensory_motor_mem():
    return SensoryMotorMemoryImpl

#initializing resources
@pytest.fixture
def test_procedural_mem():
    return ProceduralMemory

def test_notify_sensory_motor_mem(test_action_select, test_sensory_motor_mem):
    test_action_select.notify_sensory_motor_memory =(
        MagicMock(return_value=["test_state", 0.0, True, False,
                                {"info": "test_information"}]))
    test_action_select.notify_sensory_motor_memory(1,
                                                      test_sensory_motor_mem
                                                      )
    state, reward, done, truncated, info = (test_action_select.
                                            notify_sensory_motor_memory(
                                                1, test_sensory_motor_mem
                                            ))
    assert state == "test_state"
    assert reward == 0.0
    assert done == True
    assert truncated == False
    assert info == {'info': 'test_information'}
    (test_action_select.notify_sensory_motor_memory.
     assert_called_with(1, test_sensory_motor_mem))


def test_action_selected(test_action_select, test_sensory_motor_mem):
    test_action_select.select_action = (
        MagicMock(return_value=["test_state", 0, 0.0, True, False,
                                {"info": "test_information"}]))
    test_action_select.select_action(["state-0"], 0,
                                        test_sensory_motor_mem)
    state, state_id, reward, done, truncated, info = (test_action_select.
                                                select_action(
                                                ['state-0'], 0,
                                                test_sensory_motor_mem))
    assert state == "test_state"
    assert state_id == 0
    assert reward == 0
    assert truncated == 0
    assert info == {'info': 'test_information'}
    test_action_select.select_action.assert_called_with(["state-0"], 0
                                        , test_sensory_motor_mem)
