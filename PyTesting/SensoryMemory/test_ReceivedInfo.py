import pytest
from src.Memphis.ccrg.LIDA.SensoryMemory import SensoryMemory
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment
from src.Memphis.ccrg.LIDA.PAM.PAM import PerceptualAssociativeMemory
from src.Memphis.ccrg.LIDA.ProceduralMemory.ProceduralMemory import ProceduralMemory
from unittest.mock import Mock, create_autospec


def test_run_sensors():
    # Create a mock of the environment
    environment = create_autospec(FrozenLakeEnvironment)
    environment.reset.return_value = ('mock_state', 'mock_info', 0, 0)
    environment.action_space.sample.return_value = 'mock_action'

    # Create a mock of the procedural memory
    procedural_memory = create_autospec(ProceduralMemory)

    # Set up the sensory memory with the mock environment
    sensory_memory = SensoryMemory(environment=environment)

    # Invoke run_sensors
    state, percept, action, env, col, row = sensory_memory.run_sensors(procedural_memory, state_id=0)

    # Assertions to verify expected behavior
    assert state == 'mock_state'
    assert action == 'mock_action'
    assert env == environment
    assert col == 0
    assert row == 0
    procedural_memory.add_scheme.assert_called_with('state-0', 'mock_action')

    # Ensure percept retrieval from PAM is tested if possible
    # This depends on how PAM is implemented in your actual Sensory Memory class


if __name__ == "__main__":
    pytest.main()


