import pytest
from src.Framework.Agents.Agent import Agent
from src.Environment.Environment import FrozenLakeEnvironment
from src.SensoryMemory.SensoryMemory import SensoryMemory
from src.ProceduralMemory.ProceduralMemory import ProceduralMemory
from src.PAM.PAM import PerceptualAssociativeMemory
from src.ActionSelection.ActionSelection import ActionSelection
import unittest.mock as mock

def test_run():
    #Generating instances
    env_m = FrozenLakeEnvironment()
    proc_memory_m = ProceduralMemory
    pam_m = PerceptualAssociativeMemory
    sensory_memory_m = SensoryMemory
    sensory_memory_m.run_sensors.return_value = (0,0,None,None,None,None)
    action_selection_m = ActionSelection
    action_selection_m.select_action.return_value = (0,0,0,False,False,False)

    #create the agent
    agent = Agent()
    agent.env = env_m
    agent.pam = pam_m
    agent.sensory_memory = sensory_memory_m
    agent.proc_memroy = proc_memory_m
    agent.action_selection = action_selection_m

    #running the agent
    agent.run()

    #Assertions
    sensory_memory_m.run_sensors.assert_called_once()
    action_selection_m.select_action.assert_called()
    pam_m.learn.assert_any_call('state-0', outcome="safe")


