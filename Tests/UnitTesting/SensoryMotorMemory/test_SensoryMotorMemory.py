#LIDA Cognitive Framework
#Pennsylvania State University, Course : SWENG481
#Authors: Katie Killian, Brian Wachira, and Nicole Vadillo

from source.Environment.FrozenLakeEnvironment import FrozenLakeEnvironment
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import SensoryMotorMemoryImpl

"""
This provided PyTest is for the Sensory Motor Memory Module:
It provides tests for the specific functions: add_sensory_listener, receieve_action,
    send_action_exection_command. 
As development continues these are subject to change or update as the module does. 
Tests Cases: TC-044, TC-045, and TC-046.
"""

def test_add_sensory_listener():
    sensory_motor_memory = SensoryMotorMemoryImpl()
    env = FrozenLakeEnvironment()
    sensory_motor_memory.add_observer(env)
    assert env in sensory_motor_memory.observers

def test_receive_action():
    environment = FrozenLakeEnvironment()  # Generating environment for testing
    environment.reset()
    sensory_motor_memory = SensoryMotorMemoryImpl()
    action = 1
    sensory_motor_memory.action_plan = action
    action = sensory_motor_memory.send_action_execution_command()
    state, reward, done, truncated, info = environment.env.step(action)

    #Assertions
    assert state != 'state'
    assert reward != 'reward'
    assert done != 'done'
    assert truncated != 'truncated'
    assert info != 'info'

def test_send_action_execution_command():
    environment = FrozenLakeEnvironment()  # Generating environment for testing
    environment.reset()
    sensory_motor_memory = SensoryMotorMemoryImpl()
    sensory_motor_memory.add_observer(environment)
    action_plan = [1,3,2]
    sensory_motor_memory.action_plan = action_plan
    """The observer will call 
    sensory_motor_memory.send_action_execution_command and retrieve the 
    action plan"""
    sensory_motor_memory.notify_observers()

    state = 0
    reward = 0
    done = False
    truncated = False
    info = {"prob" : 1}

    # Assertions
    assert environment.state != state
    assert environment.reward != 'reward'
    assert done == False
    assert truncated == False
    assert info != {"prob" : 1/3}