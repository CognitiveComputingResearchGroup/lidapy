import pytest
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment

def test_step():
    #initializing the environment
    env = FrozenLakeEnvironment()

    #Reset the environment
    env.reset()

    #Taking a step within env
    initial_state, _, _, _ = env.reset()
    next_state, reward, done, truncated, info = env.step(env.action_space.sample())

    #making assertions - assist with verifying the code behaves as expected
    assert isinstance(initial_state, int) #Initial state should be integer
    assert isinstance(next_state, int)    #Next state should be an integer
    assert isinstance(reward, float)      #Reward could be a float
    assert isinstance(done, bool)         #Done is boolean
    assert isinstance(info, dict)         #Info is dictionary

if __name__ == '__main__':
    pytest.main()