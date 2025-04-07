import pytest

from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.PAM.PAM import PerceptualAssociativeMemory
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl

"""
This provided PyTest is for an integration test of the Sensory Memory Module:
It provides the specific integration test for:
    environment, procedural memory, PAM, and accepting modalities 
As development continues these are subject to change or update as the module does. 
Test Cases: TC-047, TC-048, TC-049 and TC-050.
"""

@pytest.fixture
def setup_environment():
    #Fixtures that need to be initialized
    environment = FrozenLake()
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

    state, percept, action, env, col, row = sensory_memory.run_sensors()

    #Assertions
    assert state is not None
    assert percept is not None
    assert action is not None
    assert env is environment
    assert isinstance(col, int)
    assert isinstance(row, int)

def test_get_sensory_content(setup_environment):
    """
    Testing the integration of Sensory Memory get_sensory_content with PAM
    :param setup_environment:
    :return: Learn
    """
    sensory_memory, _, pam, _ = setup_environment

    state = 'initial'
    outcome = 'goal'

    pam.learn(state, outcome)
    associations = pam.retrieve_associations(state)

    #Verifying the learning
    assert associations is not None
    assert 'goal' + state in pam.associations

#Testing the procedural retrieval
def test_procedural_memory_action_retrieval(setup_environment):
    sensory_memory, procedural_memory, pam, _ = setup_environment

    #add percept action pair to procedural memory
    percept = "safe"
    action = "move_right"
    procedural_memory.add_scheme(percept, action)

    #retrieve action
    retrieved_action = procedural_memory.get_action(percept)

    assert retrieved_action == action