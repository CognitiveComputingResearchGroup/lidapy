#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

import pytest

from unittest.mock import Mock
from Configs import Sensors
from src.Environment.FrozenLakeEnvironment import FrozenLakeEnvironment
from src.Framework.Shared.LinkImpl import LinkImpl
from src.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace
from src.PAM.PAM_Impl import PAMImpl
from src.ProceduralMemory.ProceduralMemory import ProceduralMemory
from src.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from src.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from src.ActionSelection.ActionSelectionImpl import ActionSelectionImpl

"""
This generated test case will ensure that all functions within the Action Selection are functioning properly.
"""

@pytest.fixture
def action_selection():
    return ActionSelectionImpl()

@pytest.fixture
def env():
    return FrozenLakeEnvironment()

@pytest.fixture
def sensory_mem(env, pam):
    return SensoryMemoryImpl()

@pytest.fixture
def pam():
    return PAMImpl()

@pytest.fixture
def procedural_mem():
    return ProceduralMemoryImpl()

def test_initialization(action_selection):
    assert isinstance(action_selection.scheme, dict)
    assert action_selection.scheme == {}

def test_select_action(action_selection):
    action_selection.scheme = {"test_key":"test_value"}
    assert action_selection.select_action() == {"test_key":"test_value"}

def test_select_action_initiallyEmpty(action_selection):
    smi = SensoryMemoryImpl()
    pam = PAMImpl()
    procedural_mem = ProceduralMemoryImpl()
    env = FrozenLakeEnvironment()          # Testing with the Frozen Lake Environment
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

"""NOT YET PASSABLE, AS CURRENTLY HAVE A MOCK PROCEDURAL BUT STILL WORKING"""
def test_notify_with_proceduralMemory(action_selection):
    mock_procedural = Mock(spec=ProceduralMemory)
    #mock_procedural.__getstate__.return_value = Mock(spec=NodeImpl)
    link1 = LinkImpl()
    link2 = LinkImpl()
    link1.setActivation(1.0)
    link2.setActivation(0.3)
    mock_procedural.get_schemes.return_value = [link1, link2]

    mock_procedural.get_action.return_value ={"action":"chosen_action"}

    action_selection.notify(mock_procedural)
    assert action_selection.scheme == {"action":"chosen_action"} #Ensuring the scheme is updated

def test_notify_with_globalWorkspace(action_selection):
    mock_workspace = Mock(spec=GlobalWorkspace)
    action_selection.notify(mock_workspace)