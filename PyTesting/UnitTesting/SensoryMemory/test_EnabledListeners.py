import pytest
from src.Memphis.ccrg.LIDA.SensoryMemory.SensoryMemory import SensoryMemory
from src.Memphis.ccrg.LIDA.PAM.PAM import PerceptualAssociativeMemory
from src.Memphis.ccrg.LIDA.Environment.Environment import FrozenLakeEnvironment
from src.Memphis.ccrg.LIDA.ProceduralMemory.ProceduralMemory import ProceduralMemory

def test_sensory_memory_listener():
    # Create the environment and perceptual associative memory instances
    environment = FrozenLakeEnvironment()
    pam = PerceptualAssociativeMemory()

    # Create the SensoryMemory instance
    sensory_memory = SensoryMemory(environment, pam)

    # Add a mock listener - Lambda function returning its input
    mock_listener = lambda x: x
    sensory_memory.add_sensory_listener(mock_listener) #Adding mock listener

    # Check if the listener has been added
    assert len(sensory_memory.listeners) == 1 #Ensuring one listener is added
    assert sensory_memory.listeners[0] == mock_listener #Ensure the correct one is added