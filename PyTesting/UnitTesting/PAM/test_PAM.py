from src.PAM.PAM import PerceptualAssociativeMemory

"""
This provided PyTest is for the Perceptual Associative Memory (PAM) Module:
It provideds test for the specific functions: add_associations, retrieve_associations,
    learn
As development continues these are subject to change or update as the module does. 
Test Cases: TC-037, TC-038, and TC-039.
"""

def test_add_associations():
    pam = PerceptualAssociativeMemory() #instance of PAM
    #Adding an association with cue1 and pattern1
    pattern = pam.add_association('cue1', 'pattern1')
    #assertions that cue1 is now in the association for pattern1
    assert 'cue1' in pam.associations['pattern1']
    #assertion that the returned pattern matches pattern1
    assert pattern == 'pattern1'

def test_retrieve_associations():
    pam = PerceptualAssociativeMemory() #instance of pam
    #adding an association
    pam.add_association('cue1', 'pattern1')
    #Retrieving the association for cue1
    result = pam.retrieve_associations('cue1')
    #assertion that the result list contains cue1
    assert result == ['cue1']
    #Attempting to retrieve association for cue2, expect cue
    result_default = pam.retrieve_associations('cue2')
    #Asserting the default list contains cue2
    assert result_default == ['cue2']

def test_learn_goal():
    pam = PerceptualAssociativeMemory()
    #Learn the association with state 1 leading to goal
    pam.learn('state1', 'goal')
    #assert that state1 is in the association
    assert 'state1' in pam.associations['goalstate1']

def test_learn_hole():
    pam = PerceptualAssociativeMemory()
    #Learn the association with state2
    pam.learn('state2', 'hole')
    #Assert that state 2 is in the association
    assert 'state2' in pam.associations['dangerstate2']

def test_learn_safe():
    pam = PerceptualAssociativeMemory()
    #learn the association with state 3
    pam.learn('state3', 'other')
    #Assert that state 3 is in the association
    assert 'state3' in pam.associations['safestate3']