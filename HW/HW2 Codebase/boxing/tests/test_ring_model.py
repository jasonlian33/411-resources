import pytest
from pytest_mock import MockerFixture



# from boxing.models.boxers_model import Boxer

from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer

@pytest.fixture()
def ring_model():
    """ Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

@pytest.fixture
def mock_update_boxer_stats(mocker):
    """Mock the update_play_count function for testing purposes."""
    return mocker.patch("boxing.models.boxers_model.update_boxer_stats")

"""Fixtures providing sample boxers for the tests."""
@pytest.fixture()
def sample_boxer1():
    # boxer id, name, weight (lbs), height (cm), reach (in), age, weightclass
    return Boxer(1234, "Alex", 160, 180, 77, 23, None ) 

@pytest.fixture()
def sample_boxer2():
    return Boxer(5678, "Bob", 168, 175, 74, 21, None)

@pytest.fixture()
def sample_boxer3():
    return Boxer(2346, "Cody", 175, 178, 75, 30, None)

@pytest.fixture()
def sample_ring(sample_boxer1, sample_boxer2):
    return [sample_boxer1, sample_boxer2]

@pytest.fixture()
def sample_ring2(sample_boxer1, sample_boxer2, sample_boxer3):
    return [sample_boxer1, sample_boxer2, sample_boxer3]


##################################################
# Fight Test Cases
##################################################

def test_fight(ring_model, sample_ring, mocker):
    """
    Test that lets two fighters fight
    """

    ring_model.ring.extend(sample_ring)
    
    mocker.patch("boxing.models.ring_model.get_random", return_value=0.10)
    mocker.patch("boxing.models.ring_model.update_boxer_stats")
    
    winner = ring_model.fight()
    assert winner == "Alex", "Winner of the fight is Alex"
    assert len(ring_model.ring) == 0, "Ring should be empty after the fight"

def test_fight_zero_boxer(ring_model):
    """
    Test with zero fighter in the ring.
    """

    with pytest.raises(ValueError, match="There must be two boxers to start a fight."): 
        ring_model.fight() 


def test_fight_one_boxer(ring_model, sample_boxer1):
    """
    Test with only one fighter in the ring.
    """

    ring_model.ring.append(sample_boxer1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."): 
        ring_model.fight()

def test_fight_three_boxer(ring_model, sample_ring2):
    """
    Test with three fighter in the ring.
    """
    ring_model.ring.extend(sample_ring2)

    with pytest.raises(ValueError, match="There must be two boxers to start a fight."): 
        ring_model.fight()



##################################################
# Ring Management Test Cases
##################################################


def test_clear_ring(ring_model, sample_boxer1, sample_boxer2):
    """ Test clearing the ring of all(two) boxers.
    """
    ring_model.ring.append(sample_boxer1)
    ring_model.ring.append(sample_boxer2)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

def test_clear_ring_one(ring_model, sample_boxer1):
    """ Test clearing the ring with one boxer.
    """
    ring_model.ring.append(sample_boxer1)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

def test_clear_ring_empty(ring_model):
    """Test clearing a ring that is empty
    """
    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be clear if empty"
    
def test_enter_ring(ring_model, sample_boxer1, sample_boxer2):
    """Test adding two boxer to the ring
    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    assert len(ring_model.ring) == 2
    assert ring_model.ring[0].name == "Alex"
    assert ring_model.ring[1].name == "Bob"

def test_enter_ring_three(ring_model, sample_boxer1, sample_boxer2, sample_boxer3):
    """Test adding three boxers to the ring
    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)

    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."): 
        ring_model.enter_ring(sample_boxer3)


def test_enter_ring_invalid_boxer(ring_model):
    """Test adding a invalid boxer to the ring
    """
    invalid_boxer = "NotABoxer"  # Invalid type (string)

    with pytest.raises(TypeError, match="Invalid type: Expected 'Boxer', got 'str'"):
        ring_model.enter_ring(invalid_boxer)


##################################################
# Get Boxers / Fighting Skills Test Cases
##################################################

# test fighting with 
def test_get_boxers(ring_model, sample_ring):
    """Test succesfully getting the boxers in the ring.
    """
    ring_model.ring.extend(sample_ring)
    
    all_boxers = ring_model.get_boxers()
    assert len(all_boxers) == 2
    assert all_boxers[0].id == 1234
    assert all_boxers[1].id == 5678

def test_get_boxers_empty(ring_model):
    """Test getting zero boxers in the ring.
    """
    ring_model.clear_ring()
    all_boxers = ring_model.get_boxers()
    assert len(all_boxers) == 0

def test_get_fighting_skills(ring_model, sample_boxer1):
    """Test successfully retrieving the boxer's skill.
    """
    ring_model.ring.append(sample_boxer1)

    boxer_skill = ring_model.get_fighting_skill(sample_boxer1)
    assert boxer_skill == 646.7, "Expected fighting skill for sample_boxer1"

def test_get_fighting_skills_two_boxers(ring_model, sample_boxer2, sample_boxer3):
    """Test successfully retrieving the boxer's skill.
    """
    ring_model.ring.append(sample_boxer2)
    ring_model.ring.append(sample_boxer3)
    
    boxer_skill2 = ring_model.get_fighting_skill(sample_boxer2)
    boxer_skill3 = ring_model.get_fighting_skill(sample_boxer3)

    assert boxer_skill2 == 510.4, "Expected fighting skill for sample_boxer2"
    assert boxer_skill3 == 707.5, "Expected fighting skill for sample_boxer3"



