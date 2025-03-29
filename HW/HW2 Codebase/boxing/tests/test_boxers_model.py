from contextlib import contextmanager
import re
import sqlite3
import pytest

from boxing.models.boxers_model import (
    Boxer,
    create_boxer,
    delete_boxer,
    get_boxer_by_id,
    get_boxer_by_name,
    get_weight_class,
    update_boxer_stats,
    get_leaderboard
)

######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("boxing.models.boxer_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Test Boxer Creation - Valid Input
#
######################################################

def test_create_boxer(mock_cursor):
    create_boxer(name="Boxer Name", weight=150, height=175, reach=180, age=25)

    expected_query = normalize_whitespace("""
        INSERT INTO boxers (name, weight, height, reach, age)
        VALUES (?, ?, ?, ?, ?)
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ("Boxer Name", 150, 175, 180, 25)

    assert actual_arguments == expected_arguments
######################################################
#
#    Test Boxer Creation - Invalid Inputs
#
######################################################

def test_create_boxer_invalid_weight():
    """Test that an error is raised when weight is below 125."""
    with pytest.raises(ValueError, match="Invalid weight: 100. Must be at least 125."):
        create_boxer(name="Invalid Boxer", weight=100, height=175, reach=180, age=25)

def test_create_boxer_invalid_height():
    """Test that an error is raised when height is 0 or negative."""
    with pytest.raises(ValueError, match="Invalid height: 0. Must be greater than 0."):
        create_boxer(name="Invalid Boxer", weight=150, height=0, reach=180, age=25)

    with pytest.raises(ValueError, match="Invalid height: -10. Must be greater than 0."):
        create_boxer(name="Invalid Boxer", weight=150, height=-10, reach=180, age=25)

def test_create_boxer_invalid_reach():
    """Test that an error is raised when reach is 0 or negative."""
    with pytest.raises(ValueError, match="Invalid reach: 0. Must be greater than 0."):
        create_boxer(name="Invalid Boxer", weight=150, height=175, reach=0, age=25)

    with pytest.raises(ValueError, match="Invalid reach: -5. Must be greater than 0."):
        create_boxer(name="Invalid Boxer", weight=150, height=175, reach=-5, age=25)

def test_create_boxer_invalid_age():
    """Test that an error is raised when age is outside the 18-40 range."""
    with pytest.raises(ValueError, match="Invalid age: 17. Must be between 18 and 40."):
        create_boxer(name="Invalid Boxer", weight=150, height=175, reach=180, age=17)

    with pytest.raises(ValueError, match="Invalid age: 41. Must be between 18 and 40."):
        create_boxer(name="Invalid Boxer", weight=150, height=175, reach=180, age=41)

def test_create_boxer_duplicate_name(mock_cursor):
    """Test that an error is raised when a boxer with the same name already exists."""
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: songs.artist, songs.title, songs.year")

    with pytest.raises(ValueError, match="Song with artist 'Artist Name', title 'Song Title', and year 2022 already exists."):
        create_song(artist="Artist Name", title="Song Title", year=2022, genre="Pop", duration=180)


def test_create_boxer_sql_error(mocker):
    """Test that a database error is properly caught and raised."""
    mock_execute = mocker.patch("boxing.utils.sql_utils.get_db_connection")
    mock_execute.side_effect = sqlite3.Error("Database error")

    with pytest.raises(sqlite3.Error, match="Database error"):
        create_boxer(name="SQL Error Boxer", weight=150, height=175, reach=180, age=25)

######################################################
#
#    Deleting Boxer
#
######################################################

def test_delete_boxer(mock_cursor):
    """Test deleting a boxer from the catalog by ID."""
    mock_cursor.fetchone.return_value = (True)
    delete_boxer(1)

    expected_select_sql = normalize_whitespace("SELECT id FROM boxers WHERE id = ?")
    expected_delete_sql = normalize_whitespace("DELETE FROM boxers WHERE id = ?")

    actual_select_sql = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])
    actual_delete_sql = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_select_sql == expected_select_sql, "The SELECT query did not match the expected structure."
    assert actual_delete_sql == expected_delete_sql, "The DELETE query did not match the expected structure."

    expected_select_args = (1,)
    expected_delete_args = (1,)

    actual_select_args = mock_cursor.execute.call_args_list[0][0][1]
    actual_delete_args = mock_cursor.execute.call_args_list[1][0][1]

    assert actual_select_args == expected_select_args, f"The SELECT query arguments did not match. Expected {expected_select_args}, got {actual_select_args}."
    assert actual_delete_args == expected_delete_args, f"The DELETE query arguments did not match. Expected {expected_delete_args}, got {actual_delete_args}."

def test_delete_boxer_bad_id(mock_cursor):
    """Test error when trying to delete a non-existent boxer.

    """
    # Simulate that no song exists with the given ID
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        delete_boxer(999)

######################################################
#
#    Get Boxer by Name
#
######################################################

def test_get_boxer_by_name(mock_cursor):
    """Test getting a boxer by name."""
    mock_cursor.fetchone.return_value = (1, "Boxer A", 75, 180, 10, 1)

    result = get_boxer_by_name("Boxer A")

    expected_result = Boxer(1, "Boxer A", 75, 180, 10, 1)

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("SELECT id, name, weight, height, wins, losses FROM boxers WHERE name = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ("Boxer A",)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"


def test_get_boxer_by_name_not_found(mock_cursor):
    """Test error when getting a non-existent boxer by name."""
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Boxer with name 'Boxer A' not found"):
        get_boxer_by_name("Boxer A")
######################################################
#
#    Get Boxer by ID
#
######################################################
def test_get_boxer_by_id(mock_cursor):
    """Test retrieving a boxer by ID."""
    mock_cursor.fetchone.return_value = (1, "Boxer A", 150, 175, 180, 25)

    result = get_boxer_by_id(1)

    expected_result = Boxer(1, "Boxer A", 150, 175, 180, 25)

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("""
        SELECT id, name, weight, height, reach, age
        FROM boxers WHERE id = ?
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = (1,)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"


def test_get_boxer_by_id_not_found(mock_cursor):
    """Test error when getting a non-existent boxer by ID."""
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Boxer with ID 99 not found."):
        get_boxer_by_id(99)
git
######################################################
#
#    Get Weight Class
#
######################################################

def test_get_weight_class():
    """Test retrieving the weight class for valid weights."""
    assert get_weight_class(204) == "HEAVYWEIGHT"  # Should be HEAVYWEIGHT
    assert get_weight_class(170) == "MIDDLEWEIGHT"  # Should be MIDDLEWEIGHT
    assert get_weight_class(150) == "LIGHTWEIGHT"  # Should be LIGHTWEIGHT
    assert get_weight_class(130) == "FEATHERWEIGHT"  # Should be FEATHERWEIGHT


def test_edge_cases_weight_class():
    """Test edge cases for weight class boundaries."""
    assert get_weight_class(125) == "FEATHERWEIGHT"  # Lower boundary for FEATHERWEIGHT
    assert get_weight_class(133) == "LIGHTWEIGHT"  # Lower boundary for LIGHTWEIGHT
    assert get_weight_class(166) == "MIDDLEWEIGHT"  # Lower boundary for MIDDLEWEIGHT
    assert get_weight_class(203) == "HEAVYWEIGHT"  # Lower boundary for HEAVYWEIGHT


def test_invalid_weight_class():
    """Test that an error is raised when weight is below 125."""
    with pytest.raises(ValueError, match="Invalid weight: 100. Weight must be at least 125."):
        get_weight_class(100)  # Invalid weight


######################################################
#
#    Update Boxer Stats
#
######################################################
def test_update_boxer_stats_win(mock_cursor):
    """Test updating a boxer's stats when the result is 'win'."""
    
    # Mock fetching the boxer (simulating boxer with ID 1 exists)
    mock_cursor.fetchone.return_value = (1,)

    # Call the function to update stats
    update_boxer_stats(1, result="win")

    # Verify the correct SQL query was executed
    expected_query = normalize_whitespace("""
        UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Verify the arguments passed to the query
    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = (1,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"

def test_update_boxer_stats_loss(mock_cursor):
    """Test updating a boxer's stats when the result is 'loss'."""
    
    # Mock fetching the boxer (simulating boxer with ID 1 exists)
    mock_cursor.fetchone.return_value = (1,)

    # Call the function to update stats
    update_boxer_stats(1, result="loss")

    # Verify the correct SQL query was executed
    expected_query = normalize_whitespace("""
        UPDATE boxers SET fights = fights + 1 WHERE id = ?
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Verify the arguments passed to the query
    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = (1,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"

def test_update_boxer_stats_invalid_result(mock_cursor):
    """Test that an error is raised when the result is not 'win' or 'loss'."""
    
    with pytest.raises(ValueError, match="Invalid result: invalid. Expected 'win' or 'loss'."):
        update_boxer_stats(1, result="invalid")  # Invalid result

def test_update_boxer_stats_boxer_not_found(mock_cursor):
    """Test that an error is raised when the boxer with the given ID is not found."""
    
    # Simulate the boxer not being found in the database
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Boxer with ID 1 not found."):
        update_boxer_stats(1, result="win")  # Boxer with ID 1 doesn't exist

######################################################
#
#    Get Leaderboard
#
######################################################

def test_get_leaderboard_by_wins(mock_cursor):
    """Test retrieving the leaderboard of boxers sorted by wins."""
    mock_cursor.fetchall.return_value = [
        (1, "Boxer A", 150, 180, 10, 1, 11, 10, 10 / 11),
        (2, "Boxer B", 160, 170, 10, 2, 12, 8, 8 / 12),
        (3, "Boxer C", 155, 175, 10, 3, 13, 7, 7 / 13)
    ]

    leaderboard = get_leaderboard(sort_by="wins")

    expected_result = [
        {
            "id": 1, "name": "Boxer A", "weight": 150, "height": 180,
            "reach": 10, "age": 1, "weight_class": "LIGHTWEIGHT", 
            "fights": 11, "wins": 10, "win_pct": 90.9
        },
        {
            "id": 2, "name": "Boxer B", "weight": 160, "height": 170,
            "reach": 10, "age": 2, "weight_class": "MIDDLEWEIGHT", 
            "fights": 12, "wins": 8, "win_pct": 66.7
        },
        {
            "id": 3, "name": "Boxer C", "weight": 155, "height": 175,
            "reach": 10, "age": 3, "weight_class": "LIGHTWEIGHT", 
            "fights": 13, "wins": 7, "win_pct": 53.8
        }
    ]

    assert leaderboard == expected_result, f"Expected {expected_result}, got {leaderboard}"

    expected_query = normalize_whitespace("""
        SELECT id, name, weight, height, reach, age, fights, wins,
               (wins * 1.0 / fights) AS win_pct
        FROM boxers
        WHERE fights > 0
        ORDER BY wins DESC
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ()

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"


def test_get_leaderboard_by_win_pct(mock_cursor):
    """Test retrieving the leaderboard of boxers sorted by win percentage."""
    mock_cursor.fetchall.return_value = [
        (1, "Boxer A", 150, 180, 10, 1, 11, 10, 10 / 11),
        (2, "Boxer B", 160, 170, 10, 2, 12, 8, 8 / 12),
        (3, "Boxer C", 155, 175, 10, 3, 13, 7, 7 / 13)
    ]

    leaderboard = get_leaderboard(sort_by="win_pct")

    expected_result = [
        {
            "id": 1, "name": "Boxer A", "weight": 150, "height": 180,
            "reach": 10, "age": 1, "weight_class": "LIGHTWEIGHT", 
            "fights": 11, "wins": 10, "win_pct": 90.9
        },
        {
            "id": 2, "name": "Boxer B", "weight": 160, "height": 170,
            "reach": 10, "age": 2, "weight_class": "MIDDLEWEIGHT", 
            "fights": 12, "wins": 8, "win_pct": 66.7
        },
        {
            "id": 3, "name": "Boxer C", "weight": 155, "height": 175,
            "reach": 10, "age": 3, "weight_class": "LIGHTWEIGHT", 
            "fights": 13, "wins": 7, "win_pct": 53.8
        }
    ]

    assert leaderboard == expected_result, f"Expected {expected_result}, got {leaderboard}"

    expected_query = normalize_whitespace("""
        SELECT id, name, weight, height, reach, age, fights, wins,
               (wins * 1.0 / fights) AS win_pct
        FROM boxers
        WHERE fights > 0
        ORDER BY win_pct DESC
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ()

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}"


def test_get_leaderboard_invalid_sort():
    """Test invalid 'sort_by' parameter."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: invalid_param"):
        get_leaderboard(sort_by="invalid_param")
