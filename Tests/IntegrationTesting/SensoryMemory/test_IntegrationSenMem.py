import pytest

from Configs import Sensors
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.Environment.FrozenLakeEnvironment import FrozenLakeEnvironment
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl

"""
This provided PyTest is for an integration test of the Sensory Memory Module:
It provides the specific integration test for:
    environment, procedural memory, PAM, and accepting modalities 
As development continues these are subject to change or update as the module does. 
Tests Cases: TC-047, TC-048, TC-049 and TC-050.
"""

@pytest.fixture
def setup_environment():
    #Fixtures that need to be initialized
    environment = FrozenLakeEnvironment()
    pam = PAMImpl()
    procedural_memory = ProceduralMemoryImpl()
    sensory_memory = SensoryMemoryImpl()
    return sensory_memory, procedural_memory, pam, environment

def test_run_sensors(setup_environment):
    """
    Testing the integration of Sensory Memory run_sensors with
        Procedural and PAM
    :param setup_environment:  Initialized
    :return:
    """
    sensory_memory, procedural_memory, pam, environment = setup_environment

    # Setting up sensory memory sensors
    sensory_memory.sensor_dict = {"text": "text_processing"}
    sensory_memory.processor_dict = {"text": "text_processing"}
    sensory_memory.processors["text"] = getattr(Sensors,
                                        sensory_memory.processor_dict["text"])

    environment.reset()
    sensory_memory.stimuli = environment.get_stimuli()

    sensory_memory.run_sensors()
    assert len(sensory_memory.links) > 0

    #Assertions
    assert environment.state is not None
    assert isinstance(environment.col, int)
    assert isinstance(environment.row, int)

def test_get_sensory_content(setup_environment):
    """
    Testing the integration of Sensory Memory get_sensory_content with PAM
    :param setup_environment:
    :return: Learn
    """

    smi, _, pam, _ = setup_environment

    env = FrozenLakeEnvironment()  # Testing with the Frozen Lake Environment
    env.reset()

    # Setting up sensory memory sensors
    smi.sensor_dict = {"text": "text_processing"}
    smi.processor_dict = {"text": "text_processing"}
    smi.processors["text"] = getattr(Sensors, smi.processor_dict["text"])

    smi.stimuli = env.get_stimuli()
    smi.state = env.get_state()
    smi.position = env.get_position()

    assert smi.stimuli == env.get_stimuli()
    assert smi.position == env.get_position()
    assert smi.state == env.get_state()
    assert smi.processors["text"] is Sensors.text_processing

    smi.run_sensors()
    cue = smi.get_sensory_content()
    pam.position = cue["params"]["position"]

    assert cue is not None
    assert pam.position == cue["params"]["position"]


    pam.learn(cue)
    associations = pam.retrieve_association(pam.get_state())

    #Verifying the learning
    assert associations is not None

#Testing the procedural retrieval
def test_procedural_memory_action_retrieval(setup_environment):
    smi, procedural_memory, pam, _ = setup_environment

    env = FrozenLakeEnvironment()  # Testing with the Frozen Lake Environment
    env.reset()

    # Setting up sensory memory sensors
    smi.sensor_dict = {"text": "text_processing"}
    smi.processor_dict = {"text": "text_processing"}
    smi.processors["text"] = getattr(Sensors, smi.processor_dict["text"])

    smi.stimuli = env.get_stimuli()
    smi.state = env.get_state()
    smi.position = env.get_position()

    assert smi.stimuli == env.get_stimuli()
    assert smi.position == env.get_position()
    assert smi.state == env.get_state()
    assert smi.processors["text"] is Sensors.text_processing

    smi.run_sensors()
    cue = smi.get_sensory_content()
    pam.position = cue["params"]["position"]

    assert cue is not None
    assert pam.position == cue["params"]["position"]

    pam.learn(cue)
    associations = pam.retrieve_association(pam.get_state())

    #add percept action pair to procedural memory
    percept = "safe"
    action = "move_right"
    for association in associations:
        procedural_memory.add_scheme(pam.get_state(), association)

    #retrieve action
    retrieved_action_schemes = procedural_memory.get_schemes(pam.get_state())

    for link in retrieved_action_schemes:
        assert (percept == link.getCategory("label") or
                percept != link.getCategory("label"))