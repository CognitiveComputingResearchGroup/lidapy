import pytest
from src.Memphis.ccrg.LIDA.SensoryMemory import SensoryMemory
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment
from src.Memphis.ccrg.LIDA.PAM.PAM import PerceptualAssociativeMemory
from src.Memphis.ccrg.LIDA.ProceduralMemory.ProceduralMemory import ProceduralMemory

@pytest.fixture
def setup_environment():
    #Instance of the environment, PAM, and Procedural Memory
    env = FrozenLakeEnvironment()
    pam = PerceptualAssociativeMemory()
    procedural_memory = ProceduralMemory()
    return env, pam, procedural_memory

def test_sensory_memory_receives_input(setup_environment):
    env, pam, procedural_memory = setup_environment

    #initializing SensoryMemory with the environment and PAM
    sensory_memory = SensoryMemory(env, pam)

    #Running the sensors to simulate data retrieval from environment
    percept = sensory_memory.run_sensors(procedural_memory, state_id=0)

    #Assertions ensuring functionality and call was successful
    assert percept is not None
    assert isinstance(percept, dict)
    assert "state" in percept
    assert "action" in percept

if __name__ == '__main__':
    pytest.main()
