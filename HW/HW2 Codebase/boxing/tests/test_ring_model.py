import pytest

# from boxing.models.boxers_model import Boxer

from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer

@pytest.fixture()
def ring_model():
    """ Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

"""Fixtures providing sample boxers for the tests."""
@pytest.fixture()
def sample_boxer1():
    # boxer id, name, weight (lbs), height (cm), reach (in), age, weightclass
    return Boxer(1234, "Alex", 160, 180, 77, 23, None ) 

@pytest.fixture()
def sample_boxer2():
    return Boxer(5678, "Bob", 168, 175, 74, 21, None)

@pytest.fixture()
def sample_ring(sample_boxer1, sample_boxer2):
    return [sample_boxer1, sample_boxer2]


##################################################
# Fight Test Cases
##################################################

def test_fight(ring_model, sample_ring):
    """
    Test that lets two fighters fight
    """

    ring_model.ring.extend(sample_ring)
    
    ring_model.fight()

    assert len(ring_model.ring) == 0, "Ring should be empty after the fight"


##################################################
# Ring Management Test Cases
##################################################

def test_clear_ring(ring_model, sample_boxer1, sample_boxer2):
    """ Test clearing the ring of all boxers.
    """
    ring_model.ring.append(sample_boxer1)
    ring_model.ring.append(sample_boxer2)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

def test_enter_ring(ring_model, sample_boxer1):
    """Test adding a boxer to the ring
    """
    ring_model.enter_ring(sample_boxer1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == "Alex"


##################################################
# Get Boxers / Fighting Skills Test Cases
##################################################

def test_get_boxers(ring_model, sample_ring):
    """Test succesfully getting the boxers in the ring.
    """
    ring_model.ring.extend(sample_ring)
    
    all_boxers = ring_model.get_boxers()
    assert len(all_boxers) == 2
    assert all_boxers[0].id == 1234
    assert all_boxers[1].id == 5678

def test_get_fighting_skills(ring_model, sample_boxer1):
    """Test successfully retrieving the boxer's skill.
    """
    ring_model.ring.append(sample_boxer1)

    boxer_skill = ring_model.get_fighting_skill(sample_boxer1)
    assert boxer_skill == 646.7, "Expected fighting skill for sample_boxer1"
