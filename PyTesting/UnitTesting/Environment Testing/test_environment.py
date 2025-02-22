import pytest
from src.Environment.Environment import FrozenLakeEnvironment

"""
This provided PyTest is for the Environment ModuleSubject:
It provides tests for the specific functions: reset, step, render
As development continues these are subject to change or update as the module does. 
Test Cases: TC-032, TC-033, and TC-034.
"""

#Defining a fixture function
#initializing resources
@pytest.fixture
def environment():
    return FrozenLakeEnvironment(render_mode="human")

def test_reset(environment):
    #Calling the reset
    state, info, col, row = environment.reset()
    #Asserting initial conditions
    assert state is not None #State should not be none after reset
    assert info is not None #Info should be a dictionary
    assert col == 0 #Column should be reset to 0
    assert row == 0 #Row should be reset to 0

def test_step(environment):
    environment.reset() #ensuring environment is reset
    action = environment.action_space.sample() #random action
    new_state, reward, done, truncated, info = environment.step(action)
    #Assertions
    assert new_state is not None
    assert info is not None
    assert isinstance(reward, (int,float))
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)

def test_render(environment):
    environment.reset()
    try:
        environment.render()
    except Exception as e:
        pytest.fail(f"Rendering failed: {e}")

