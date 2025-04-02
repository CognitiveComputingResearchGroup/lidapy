from Configs import Sensors
from source.Environment.FrozenLakeEnvironment import FrozenLake
from source.SensoryMemory.SensoryMemory import SensoryMemory
from source.SensoryMemory.SensoryMemoryImpl import SensoryMemoryImpl

"""
This provided PyTest is for the Sensory Memory ModuleSubject:
It provides tests for the specific functions: 
As development continues these are subject to change or update as the module does. 
Test Cases: 
"""

#Testing the Sensory memory & sensory memory impl initialization
def test_sensoryMemory_initialization():
    sensory_memory = SensoryMemory()
    assert sensory_memory is not None

def test_sensoryMemoryImpl_Initialization():
    smi = SensoryMemoryImpl()
    assert smi.sensor is None
    assert smi.processors == {}
    assert smi.stimuli is None
    assert smi.position is None
    assert smi.state is None
    assert smi.links == []
    assert smi.sensor_dict == {}
    assert smi.processor_dict == {}

#Tesing the notify function
def test_notify():
    smi = SensoryMemoryImpl()
    env = FrozenLake() #Testing with the Frozen Lake Environment
    env.reset()
    env.add_observer(smi)
    env.notify_observers()
    smi.sensor_dict = {"text": "text_processing"}
    smi.processor_dict = {"text": "text_processing"}
    smi.processors["text"] = getattr(Sensors, smi.processor_dict["text"])
    assert smi.stimuli == env.get_stimuli()
    assert smi.position == env.get_position()
    assert smi.state == env.__getstate__()
    assert smi.processors["text"] is Sensors.text_processing

"""
implement run sensors test method
"""
def test_run_sensors():
    #preparing the sensors
    smi = SensoryMemoryImpl()
    smi.sensor_dict = {"text": "text_processing"}
    smi.processor_dict = {"text": "text_processing"}
    smi.processors["text"] = getattr(Sensors, smi.processor_dict["text"])
    env = FrozenLake()  # Testing with the Frozen Lake Environment
    env.reset()
    assert smi.processors["text"] is Sensors.text_processing
    smi.stimuli = env.get_stimuli()
    assert smi.stimuli is not None
    assert smi.links is not None