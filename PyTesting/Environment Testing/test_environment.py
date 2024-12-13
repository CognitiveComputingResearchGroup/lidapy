import pytest
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment

def test_reset():
    #Generating an instance of FrozenLakeEnvironment
    env = FrozenLakeEnvironment()

    #Calling the reset
    state, info, col, row = env.reset()

    #Asserting initial conditions
    assert isinstance(state, (int, tuple))
    assert isinstance(info, dict)
    assert col == 0
    assert row == 0
