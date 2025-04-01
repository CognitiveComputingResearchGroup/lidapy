from itertools import product

import pytest
from unittest.mock import Mock

from source.ActionSelection.ActionSelection import ActionSelection
from source.SensoryMotorMemory.SensoryMotorMemoryImpl import SensoryMotorMemoryImpl
from source.ActionSelection.ActionSelectionImpl import ActionSelectionImpl
from source.ProceduralMemory.ProceduralMemory import ProceduralMemory
from source.GlobalWorkspace.GlobalWorkSpace import GlobalWorkspace

@pytest.fixture
def action_selection():
    return ActionSelectionImpl()

def test_select_action_initiallyEmpty(action_selection):
    #testing that the scheme is initially empty
    assert action_selection.select_action() == {}

