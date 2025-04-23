from email.errors import NonASCIILocalPartDefect

import pytest
from source.Workspace.CurrentSitutationalModel.CurrentSituationalModelImpl import CurrentSituationalModelImpl
from source.Framework.Shared.NodeStructureImpl import NodeStructureImpl

@pytest.fixture
def model():
    """Generating fixture"""
    return CurrentSituationalModelImpl()

def test_initialization(model):
    """Testing the initialization function"""
    assert model.node_structure is not None
    assert model.received_coalition is None
    assert model.state is None

def test_addBufferContent(model):
    """Testing the addBufferContent function"""
    workspace_content = NodeStructureImpl()
    model.addBufferContent(workspace_content)

    assert model.getBufferContent() == workspace_content

def test_get_state(model):
    """testing getting the state function"""
    assert model.get_state() is None
    expected_state = {"state":"example_state"}
    model.set_state(expected_state)
    assert model.get_state() == expected_state
