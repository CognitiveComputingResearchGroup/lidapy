#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG480
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from lidapy import Environment
from lidapy.src import FrozenLakeEnvironment

#Testing the Generalized Environment
def test_environment_initialization():
    env = Environment()
    assert env is not None

def test_environment_reset():
    env = Environment()
    env.reset()
    assert env.get_state() is None

def test_environment_step():
    env = Environment()
    state = env.step('any_action')
    assert state is None

def test_environment_close():
    env = Environment()
    env.close()

#Testing the Frozen Lake Environment
def test_frozenlake_initialization():
    fl_env = FrozenLakeEnvironment()
    state = fl_env.reset()
    assert "state" in fl_env.state
    assert not fl_env.state["done"]

def test_frozenlake_positionUpdate():
    fl_env = FrozenLakeEnvironment()
    initial_position = fl_env.get_position().copy()
    fl_env.update_position(1)
    new_position = fl_env.get_position()
    assert initial_position != new_position

def test_frozenlake_step():
    fl_env = FrozenLakeEnvironment()
    fl_env.reset()
    fl_env.step(1)
    assert "state" in fl_env.state
    assert "info" in fl_env.state

def test_frozenlake_get_stimuli():
    fl_env = FrozenLakeEnvironment()
    stimuli = fl_env.get_stimuli()
    assert isinstance(stimuli, dict)

def test_frozenlake_render():
    fl_env = FrozenLakeEnvironment(render_mode="human")