import pytest

from Configs import Sensors
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl

@pytest.fixture
def action_selection():
    return ActionSelectionImpl()

@pytest.fixture
def env():
    return FrozenLake()

@pytest.fixture
def sensory_mem(env, pam):
    return SensoryMemoryImpl()

@pytest.fixture
def pam():
    return PAMImpl()

@pytest.fixture
def procedural_mem():
    return ProceduralMemoryImpl()

def test_select_action_initiallyEmpty(action_selection):
    smi = SensoryMemoryImpl()
    pam = PAMImpl()
    procedural_mem = ProceduralMemoryImpl()
    env = FrozenLake()          # Testing with the Frozen Lake Environment
    env.reset()

    #Setting up sensory memory sensors
    smi.sensor_dict = {"text": "text_processing"}
    smi.processor_dict = {"text": "text_processing"}
    smi.processors["text"] = getattr(Sensors, smi.processor_dict["text"])

    smi.stimuli = env.get_stimuli()
    smi.state = env.__getstate__()
    smi.position = env.get_position()

    assert smi.stimuli == env.get_stimuli()
    assert smi.position == env.get_position()
    assert smi.state == env.__getstate__()
    assert smi.processors["text"] is Sensors.text_processing

    smi.run_sensors()
    cue = smi.get_sensory_content()
    pam.position = cue["params"]["position"]

    assert cue is not None
    assert pam.position == cue["params"]["position"]

    pam.learn(cue)
    procedural_mem.scheme = ["avoid hole", "seek goal"]

    state = pam.__getstate__()
    schemes = pam.retrieve_association(state)

    assert state is not None
    assert procedural_mem.scheme == ["avoid hole", "seek goal"]
    assert schemes is not None
    assert len(schemes) == 4    #1 for each surrounding cell

    for scheme in schemes:
        procedural_mem.add_scheme(state, scheme)

    action_schemes = procedural_mem.get_schemes(state)

    #testing that the scheme isn't empty
    assert action_schemes is not None