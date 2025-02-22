from src.ProceduralMemory.ProceduralMemory import ProceduralMemory

"""
This provided PyTest is for the Procedural Memory ModuleSubject:
It provides tests for the specific functions: add_scheme, get_action
As development continues these are subject to change or update as the module does. 
Test Cases: TC-040, TC-041.
"""

def test_add_scheme():
    procedural_memory = ProceduralMemory()
    procedural_memory.add_scheme("goal", "move_forward")
    assert procedural_memory.schemes["goal"] == "move_forward"

def test_get_action_existing():
    procedural_memory = ProceduralMemory()
    procedural_memory.add_scheme("goal", "move_forward")
    assert procedural_memory.get_action("goal") == "move_forward"

def test_get_action_not_existing():
    procedural_memory = ProceduralMemory()
    assert procedural_memory.get_action("unknown") is None