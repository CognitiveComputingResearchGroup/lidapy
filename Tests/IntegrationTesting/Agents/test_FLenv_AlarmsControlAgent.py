import pytest

from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.Framework.Agents.Alarms_Control_Agent import AlarmsControlAgent
from source.PAM.PAM_Impl import PAMImpl
from source.ProceduralMemory.ProceduralMemoryImpl import ProceduralMemoryImpl
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import \
    SensoryMotorMemoryImpl

"""
This generated integrated test case will test the relationship between 
the Frozen Lake Environment and the Alarms Control Agent classes.
"""

def test_agent_integration():
    agent = AlarmsControlAgent()

    agent.environment = FrozenLake()
    agent.pam = PAMImpl()
    agent.sensory_memory = SensoryMemoryImpl()
    agent.procedural_memory = ProceduralMemoryImpl()
    agent.action_selection = ActionSelectionImpl()
    agent.sensory_motor_mem = SensoryMotorMemoryImpl()

    #Testing if the agent components are initialized
    assert agent.environment is not None
    assert agent.pam is not None
    assert agent.sensory_memory is not None
    #assert agent.motor_plan_execution is not None - Does not currently have this module
    assert agent.procedural_memory is not None
    assert agent.action_selection is not None
    assert agent.sensory_motor_mem is not None

    agent.run()
    assert agent.environment.get_stimuli() is not None
    assert agent.__getstate__()["done"] is True
    assert hasattr(agent.environment, 'action_space')
    assert agent.procedural_memory #Checking to see if it initializes without error