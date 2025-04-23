from unittest.mock import Mock
from source.GlobalWorkspace import GlobalWorkspace
from source.Framework.Shared import LinkImpl, NodeImpl
from source.ProceduralMemory import ProceduralMemory

"""
Testing the integration of the Action Selection module with the GlobalWorkspace
as well as Procedural Memory.
"""
def test_notify_with_proceduralMemory(action_selection):
    mock_procedural = Mock(spec=ProceduralMemory)
    #mock_procedural.__getstate__.return_value = Mock(spec=NodeImpl)
    link1 = LinkImpl()
    link2 = LinkImpl()
    link1.setActivation(1.0)
    link2.setActivation(0.3)
    mock_procedural.get_schemes.return_value = [link1, link2]

    mock_procedural.get_action.return_value ={"action":"chosen_action"}

    state = NodeImpl()
    state.setId(0)
    action_selection.add_behavior(state, {"action":"chosen_action"})
    action_selection.notify(mock_procedural)
    # Ensuring the scheme is updated
    assert action_selection.get_behaviors(state)[0] == {"action":"chosen_action"}

def test_notify_with_globalWorkspace(action_selection):
    mock_workspace = Mock(spec=GlobalWorkspace)
    action_selection.notify(mock_workspace)