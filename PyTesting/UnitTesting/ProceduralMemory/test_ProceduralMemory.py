from src.ProceduralMemory.ProceduralMemory import ProceduralMemory

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