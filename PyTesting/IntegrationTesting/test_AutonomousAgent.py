from src.Memphis.ccrg.LIDA.Framework.Agents.Agent import Agent

def test_agent_integration():
    agent = Agent()

    #Testing if the agent components are initialized
    assert agent.env is not None
    assert agent.pam is not None
    assert agent.sensory_memory is not None
    assert agent.motor_plan_execution is not None
    assert agent.procedural_memory is not None
    assert agent.action_selection is not None
    assert agent.sensory_motor_memory is not None


    #Example of a check
    assert hasattr(agent.env, 'action_space')
    assert agent.procedural_memory #Checking to see if it initializes without error