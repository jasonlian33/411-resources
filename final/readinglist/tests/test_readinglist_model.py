import pytest

from readinglist.models.readinglist_model import ReadinglistModel
from readinglist.models.book_model import Books


@pytest.fixture()
def readinglist_model():
    """Fixture to provide a new instance of ReadinglistModel for each test."""
    return ReadinglistModel()

"""Fixtures providing sample books for the tests."""
@pytest.fixture
def book_mockingbird(session):
    """Fixture for "To Kill a Mockingbird" by Harper Lee."""
    book = Books(
        author="Harper Lee",
        title="To Kill a Mockingbird",
        year=1960,
        genre="Southern Gothic",
        length=281
    )
    session.add(book)
    session.commit()
    return book

@pytest.fixture
def book_1984(session):
    """Fixture for "1984" by George Orwell."""
    book = Books(
        author="George Orwell",
        title="1984",
        year=1949,
        genre="Dystopian Fiction",
        length=328
    )
    session.add(book)
    session.commit()
    return book

@pytest.fixture
def sample_readinglist(book_mockingbird, book_1984):
    """Fixture for a sample readinglist."""
    return [book_mockingbird, book_1984]

##################################################
# Add / Remove Book Management Test Cases
##################################################


def test_add_book_to_readinglist(readinglist_model, book_mockingbird, mocker):
    """Test adding a book to the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)
    readinglist_model.add_book_to_readinglist(1)
    assert len(readinglist_model.readinglist) == 1
    assert readinglist_model.readinglist[0] == 1


def test_add_duplicate_book_to_readinglist(readinglist_model, book_mockingbird, mocker):
    """Test error when adding a duplicate book to the readinglist by ID."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=[book_mockingbird] * 2)
    readinglist_model.add_book_to_readinglist(1)
    with pytest.raises(ValueError, match="Book with ID 1 already exists in the readinglist"):
        readinglist_model.add_book_to_readinglist(1)


def test_remove_book_from_readinglist_by_book_id(readinglist_model, mocker):
    """Test removing a book from the readinglist by book_id."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)

    readinglist_model.readinglist = [1,2]

    readinglist_model.remove_book_by_book_id(1)
    assert len(readinglist_model.readinglist) == 1, f"Expected 1 book, but got {len(readinglist_model.readinglist)}"
    assert readinglist_model.readinglist[0] == 2, "Expected book with id 2 to remain"


def test_remove_book_by_list_number(readinglist_model):
    """Test removing a book from the readinglist by list number."""
    readinglist_model.readinglist = [1,2]
    assert len(readinglist_model.readinglist) == 2

    readinglist_model.remove_book_by_list_number(1)
    assert len(readinglist_model.readinglist) == 1, f"Expected 1 book, but got {len(readinglist_model.readinglist)}"
    assert readinglist_model.readinglist[0] == 2, "Expected book with id 2 to remain"


def test_clear_readinglist(readinglist_model):
    """Test clearing the entire readinglist."""
    readinglist_model.readinglist.append(1)

    readinglist_model.clear_readinglist()
    assert len(readinglist_model.readinglist) == 0, "Readinglist should be empty after clearing"


# ##################################################
# # Readinglisting Management Test Cases
# ##################################################


def test_move_book_to_list_number(readinglist_model, sample_readinglist, mocker):
    """Test moving a book to a specific list number in the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.move_book_to_list_number(2, 1)  # Move Book 2 to the first position
    assert readinglist_model.readinglist[0] == 2, "Expected Book 2 to be in the first position"
    assert readinglist_model.readinglist[1] == 1, "Expected Book 1 to be in the second position"


def test_swap_books_in_readinglist(readinglist_model, sample_readinglist, mocker):
    """Test swapping the positions of two books in the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.swap_books_in_readinglist(1, 2)  # Swap positions of Book 1 and Book 2
    assert readinglist_model.readinglist[0] == 2, "Expected Book 2 to be in the first position"
    assert readinglist_model.readinglist[1] == 1, "Expected Book 1 to be in the second position"


def test_swap_book_with_itself(readinglist_model, book_mockingbird, mocker):
    """Test swapping the position of a book with itself raises an error."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=[book_mockingbird] * 2)
    readinglist_model.readinglist.append(1)

    with pytest.raises(ValueError, match="Cannot swap a book with itself"):
        readinglist_model.swap_books_in_readinglist(1, 1)  # Swap positions of Book 1 with itself


def test_move_book_to_end(readinglist_model, sample_readinglist, mocker):
    """Test moving a book to the end of the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.move_book_to_end(1)  # Move Book 1 to the end
    assert readinglist_model.readinglist[1] == 1, "Expected Book 1 to be at the end"


def test_move_book_to_beginning(readinglist_model, sample_readinglist, mocker):
    """Test moving a book to the beginning of the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.move_book_to_beginning(2)  # Move Book 2 to the beginning
    assert readinglist_model.readinglist[0] == 2, "Expected Book 2 to be at the beginning"


##################################################
# Book Retrieval Test Cases
##################################################


def test_get_book_by_list_number(readinglist_model, book_mockingbird, mocker):
    """Test successfully retrieving a book from the readinglist by list number."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)
    readinglist_model.readinglist.append(1)

    retrieved_book = readinglist_model.get_book_by_list_number(1)
    assert retrieved_book.id == 1
    assert retrieved_book.title == 'To Kill a Mockingbird'
    assert retrieved_book.author == 'Harper Lee'
    assert retrieved_book.year == 1960
    assert retrieved_book.length == 281
    assert retrieved_book.genre == 'Southern Gothic'


def test_get_all_books(readinglist_model, sample_readinglist, mocker):
    """Test successfully retrieving all books from the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])

    all_books = readinglist_model.get_all_books()

    assert len(all_books) == 2
    assert all_books[0].id == 1
    assert all_books[1].id == 2


def test_get_book_by_book_id(readinglist_model, book_mockingbird, mocker):
    """Test successfully retrieving a book from the readinglist by book ID."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)
    readinglist_model.readinglist.append(1)

    retrieved_book = readinglist_model.get_book_by_book_id(1)

    assert retrieved_book.id == 1
    assert retrieved_book.title == 'To Kill a Mockingbird'
    assert retrieved_book.author == 'Harper Lee'
    assert retrieved_book.year == 1960
    assert retrieved_book.length == 281
    assert retrieved_book.genre == 'Southern Gothic'

def test_get_current_book(readinglist_model, book_mockingbird, mocker):
    """Test successfully retrieving the current book from the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)

    readinglist_model.readinglist.append(1)

    current_book = readinglist_model.get_current_book()
    assert current_book.id == 1
    assert current_book.title == 'To Kill a Mockingbird'
    assert current_book.author == 'Harper Lee'
    assert current_book.year == 1960
    assert current_book.length == 281
    assert current_book.genre == 'Southern Gothic'


def test_get_readinglist_length(readinglist_model):
    """Test getting the length of the readinglist."""
    readinglist_model.readinglist.extend([1, 2])
    assert readinglist_model.get_readinglist_length() == 2, "Expected readinglist length to be 2"


def test_get_readinglist_page_count(readinglist_model, sample_readinglist, mocker):
    """Test getting the total page count of the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", side_effect=sample_readinglist)
    readinglist_model.readinglist.extend([1, 2])
    assert readinglist_model.get_readinglist_page_count() == 609, "Expected readinglist page count to be 609 seconds"


##################################################
# Utility Function Test Cases
##################################################


def test_check_if_empty_non_empty_readinglist(readinglist_model):
    """Test check_if_empty does not raise error if readinglist is not empty."""
    readinglist_model.readinglist.append(1)
    try:
        readinglist_model.check_if_empty()
    except ValueError:
        pytest.fail("check_if_empty raised ValueError unexpectedly on non-empty readinglist")


def test_check_if_empty_empty_readinglist(readinglist_model):
    """Test check_if_empty raises error when readinglist is empty."""
    readinglist_model.clear_readinglist()
    with pytest.raises(ValueError, match="Readinglist is empty"):
        readinglist_model.check_if_empty()


def test_validate_book_id(readinglist_model, mocker):
    """Test validate_book_id does not raise error for valid book ID."""
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", return_value=True)

    readinglist_model.readinglist.append(1)
    try:
        readinglist_model.validate_book_id(1)
    except ValueError:
        pytest.fail("validate_book_id raised ValueError unexpectedly for valid book ID")


def test_validate_book_id_no_check_in_readinglist(readinglist_model, mocker):
    """Test validate_book_id does not raise error for valid book ID when the id isn't in the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", return_value=True)
    try:
        readinglist_model.validate_book_id(1, check_in_readinglist=False)
    except ValueError:
        pytest.fail("validate_book_id raised ValueError unexpectedly for valid book ID")


def test_validate_book_id_invalid_id(readinglist_model):
    """Test validate_book_id raises error for invalid book ID."""
    with pytest.raises(ValueError, match="Invalid book id: -1"):
        readinglist_model.validate_book_id(-1)

    with pytest.raises(ValueError, match="Invalid book id: invalid"):
        readinglist_model.validate_book_id("invalid")


def test_validate_book_id_not_in_readinglist(readinglist_model, book_mockingbird, mocker):
    """Test validate_book_id raises error for book ID not in the readinglist."""
    mocker.patch("readinglist.models.readinglist_model.Books.get_book_by_id", return_value=book_mockingbird)
    readinglist_model.readinglist.append(1)
    with pytest.raises(ValueError, match="Book with id 2 not found in readinglist"):
        readinglist_model.validate_book_id(2)


def test_validate_list_number(readinglist_model):
    """Test validate_list_number does not raise error for valid list number."""
    readinglist_model.readinglist.append(1)
    try:
        readinglist_model.validate_list_number(1)
    except ValueError:
        pytest.fail("validate_list_number raised ValueError unexpectedly for valid list number")

@pytest.mark.parametrize("list_number, expected_error", [
    (0, "Invalid list number: 0"),
    (2, "Invalid list number: 2"),
    ("invalid", "Invalid list number: invalid"),
])
def test_validate_list_number_invalid(readinglist_model, list_number, expected_error):
    """Test validate_list_number raises error for invalid list numbers."""
    readinglist_model.readinglist.append(1)

    with pytest.raises(ValueError, match=expected_error):
        readinglist_model.validate_list_number(list_number)



##################################################
# Playback Test Cases
##################################################


def test_play_current_book(readinglist_model, sample_readinglist, mocker):
    """Test reading the current book."""
    mock_update_read_count = mocker.patch(
        "readinglist.models.readinglist_model.Books.update_read_count"
    )
    mocker.patch(
        "readinglist.models.readinglist_model.Books.get_book_by_id",
        side_effect=sample_readinglist
    )

    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.read_current_book()

    # CURRENT_SELECTION_NUMBER updated to 2
    assert readinglist_model.current_list_number == 2, \
        f"Expected selection number to be 2, but got {readinglist_model.current_list_number}"

    mock_update_read_count.assert_called_once_with()

    readinglist_model.read_current_book()
    assert readinglist_model.current_list_number == 1, \
        f"Expected selection number to be 1, but got {readinglist_model.current_list_number}"
    mock_update_read_count.assert_called_with()


def test_rewind_readinglist(readinglist_model):
    """Test rewinding the iterator to the beginning of the readinglist."""
    readinglist_model.readinglist.extend([1, 2])
    readinglist_model.reading_list_number = 2

    readinglist_model.rewind_readinglist()
    assert readinglist_model.current_list_number == 1, "Expected to rewind to the first list"


def test_go_to_list_number(readinglist_model):
    """Test moving the iterator to a specific list number in the readinglist."""
    readinglist_model.readinglist.extend([1, 2])

    readinglist_model.go_to_list_number(2)
    assert readinglist_model.current_list_number == 2, "Expected to be at list 2 after moving book"


def test_go_to_random_list(readinglist_model, mocker):
    """Test that go_to_random_list sets a valid random list number."""
    readinglist_model.readinglist.extend([1, 2])

    mocker.patch("readinglist.models.readinglist_model.get_random", return_value=2)

    readinglist_model.go_to_random_list()
    assert readinglist_model.current_list_number == 2, "Current list number should be set to the random value"


def test_read_entire_readinglist(readinglist_model, sample_readinglist, mocker):
    """Test playing the entire readinglist."""
    mock_update_read_count = mocker.patch("readinglist.models.readinglist_model.Books.update_read_count")
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1,2])

    readinglist_model.read_entire_readinglist()

    # Check that all play counts were updated
    mock_update_read_count.assert_any_call()
    assert mock_update_read_count.call_count == len(readinglist_model.readinglist)

    # Check that the current list number was updated back to the first book
    assert readinglist_model.current_list_number == 1, "Expected to loop back to the beginning of the readinglist"


def test_read_rest_of_readinglist(readinglist_model, sample_readinglist, mocker):
    """Test playing from the current position to the end of the readinglist.

    """
    mock_update_read_count = mocker.patch("readinglist.models.readinglist_model.Books.update_read_count")
    mocker.patch("readinglist.models.readinglist_model.ReadinglistModel._get_book_from_cache_or_db", side_effect=sample_readinglist)

    readinglist_model.readinglist.extend([1, 2])
    readinglist_model.current_list_number = 2

    readinglist_model.read_rest_of_readinglist()

    # Check that play counts were updated for the remaining books
    mock_update_read_count.assert_any_call()
    assert mock_update_read_count.call_count == 1

    assert readinglist_model.current_list_number == 1, "Expected to loop back to the beginning of the readinglist"