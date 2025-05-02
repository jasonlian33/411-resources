import logging
import os
import time
from typing import List

from readinglist.models.book_model import Books
from readinglist.utils.api_utils import get_random
from readinglist.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class ReadinglistModel:
    """
    A class to manage a readinglist of books.

    """

    def __init__(self):
        """Initializes the ReadinglistModel with an empty readinglist and the current list set to 1.

        The readinglist is a list of Books, and the current list number is 1-indexed.
        The TTL (Time To Live) for book caching is set to a default value from the environment variable "TTL",
        which defaults to 60 seconds if not set.

        """
        self.current_list_number = 1
        self.readinglist: List[int] = []
        self._book_cache: dict[int, Books] = {}
        self._ttl: dict[int, float] = {}
        self.ttl_seconds = int(os.getenv("TTL", 60))  # Default TTL is 60 seconds


    ##################################################
    # Book Management Functions
    ##################################################

    def _get_book_from_cache_or_db(self, book_id: int) -> Books:
        """
        Retrieves a book by ID, using the internal cache if possible.

        This method checks whether a cached version of the book is available
        and still valid. If not, it queries the database, updates the cache, and returns the book.

        Args:
            book_id (int): The unique ID of the book to retrieve.

        Returns:
            Books: The book object corresponding to the given ID.

        Raises:
            ValueError: If the book cannot be found in the database.
        """
        now = time.time()

        if book_id in self._book_cache and self._ttl.get(book_id, 0) > now:
            logger.debug(f"Book ID {book_id} retrieved from cache")
            return self._book_cache[book_id]

        try:
            book = Books.get_book_by_id(book_id)
            logger.info(f"Book ID {book_id} loaded from DB")
        except ValueError as e:
            logger.error(f"Book ID {book_id} not found in DB: {e}")
            raise ValueError(f"Book ID {book_id} not found in database") from e

        self._book_cache[book_id] = book
        self._ttl[book_id] = now + self.ttl_seconds
        return book

    def add_book_to_readinglist(self, book_id: int) -> None:
        """
        Adds a book to the readinglist by ID, using the cache or database lookup.

        Args:
            book_id (int): The ID of the book to add to the readinglist.

        Raises:
            ValueError: If the book ID is invalid or already exists in the readinglist.
        """
        logger.info(f"Received request to add book with ID {book_id} to the readinglist")

        book_id = self.validate_book_id(book_id, check_in_readinglist=False)

        if book_id in self.readinglist:
            logger.error(f"Book with ID {book_id} already exists in the readinglist")
            raise ValueError(f"Book with ID {book_id} already exists in the readinglist")

        try:
            book = self._get_book_from_cache_or_db(book_id)
        except ValueError as e:
            logger.error(f"Failed to add book: {e}")
            raise

        self.readinglist.append(book.id)
        logger.info(f"Successfully added to readinglist: {book.author} - {book.title} ({book.year})")


    def remove_book_by_book_id(self, book_id: int) -> None:
        """Removes a book from the readinglist by its book ID.

        Args:
            book_id (int): The ID of the book to remove from the readinglist.

        Raises:
            ValueError: If the readinglist is empty or the book ID is invalid.

        """
        logger.info(f"Received request to remove book with ID {book_id}")

        self.check_if_empty()
        book_id = self.validate_book_id(book_id)

        if book_id not in self.readinglist:
            logger.warning(f"Book with ID {book_id} not found in the readinglist")
            raise ValueError(f"Book with ID {book_id} not found in the readinglist")

        self.readinglist.remove(book_id)
        logger.info(f"Successfully removed book with ID {book_id} from the readinglist")

    def remove_book_by_list_number(self, list_number: int) -> None:
        """Removes a book from the readinglist by its list number (1-indexed).

        Args:
            list_number (int): The list number of the book to remove.

        Raises:
            ValueError: If the readinglist is empty or the list number is invalid.

        """
        logger.info(f"Received request to remove book at list number {list_number}")

        self.check_if_empty()
        list_number = self.validate_list_number(list_number)
        readinglist_index = list_number - 1

        logger.info(f"Successfully removed book at list number {list_number}")
        del self.readinglist[readinglist_index]

    def clear_readinglist(self) -> None:
        """Clears all books from the readinglist.

        Clears all books from the readinglist. If the readinglist is already empty, logs a warning.

        """
        logger.info("Received request to clear the readinglist")

        try:
            if self.check_if_empty():
                pass
        except ValueError:
            logger.warning("Clearing an empty readinglist")

        self.readinglist.clear()
        logger.info("Successfully cleared the readinglist")


    ##################################################
    # Readinglist Retrieval Functions
    ##################################################


    def get_all_books(self) -> List[Books]:
        """Returns a list of all books in the readinglist using cached book data.

        Returns:
            List[Books]: A list of all books in the readinglist.

        Raises:
            ValueError: If the readinglist is empty.
        """
        self.check_if_empty()
        logger.info("Retrieving all books in the readinglist")
        return [self._get_book_from_cache_or_db(book_id) for book_id in self.readinglist]

    def get_book_by_book_id(self, book_id: int) -> Books:
        """Retrieves a book from the readinglist by its book ID using the cache or DB.

        Args:
            book_id (int): The ID of the book to retrieve.

        Returns:
            Book: The book with the specified ID.

        Raises:
            ValueError: If the readinglist is empty or the book is not found.
        """
        self.check_if_empty()
        book_id = self.validate_book_id(book_id)
        logger.info(f"Retrieving book with ID {book_id} from the readinglist")
        book = self._get_book_from_cache_or_db(book_id)
        logger.info(f"Successfully retrieved book: {book.author} - {book.title} ({book.year})")
        return book

    def get_book_by_list_number(self, list_number: int) -> Books:
        """Retrieves a book from the readinglist by its list number (1-indexed).

        Args:
            list_number (int): The list number of the book to retrieve.

        Returns:
            Book: The book at the specified list number.

        Raises:
            ValueError: If the readinglist is empty or the list number is invalid.
        """
        self.check_if_empty()
        list_number = self.validate_list_number(list_number)
        readinglist_index = list_number - 1

        logger.info(f"Retrieving book at lit number {list_number} from readinglist")
        book_id = self.readinglist[readinglist_index]
        book = self._get_book_from_cache_or_db(book_id)
        logger.info(f"Successfully retrieved book: {book.author} - {book.title} ({book.year})")
        return book

    def get_current_book(self) -> Books:
        """Returns the current book being read.

        Returns:
            Book: The currently read book.

        Raises:
            ValueError: If the readinglist is empty.
        """
        self.check_if_empty()
        logger.info("Retrieving the current book being read")
        return self.get_book_by_list_number(self.current_list_number)

    def get_readinglist_length(self) -> int:
        """Returns the number of books in the readinglist.

        Returns:
            int: The total number of books in the readinglist.

        """
        length = len(self.readinglist)
        logger.info(f"Retrieving readinglist length: {length} books")
        return length

    def get_readinglist_page_count(self) -> int:
        """
        Returns the total length of the readinglist in pages using cached book.

        Returns:
            int: The total length of all books in the readinglist in pages.
        """
        total_duration = sum(self._get_book_from_cache_or_db(book_id).length for book_id in self.readinglist)
        logger.info(f"Retrieving total readinglist length: {total_duration} pages")
        return total_duration


    ##################################################
    # Readinglist Movement Functions
    ##################################################


    def go_to_list_number(self, list_number: int) -> None:
        """Sets the current list number to the specified list number.

        Args:
            list_number (int): The list number to set as the current list.

        Raises:
            ValueError: If the readinglist is empty or the list number is invalid.

        """
        self.check_if_empty()
        list_number = self.validate_list_number(list_number)
        logger.info(f"Setting current list number to {list_number}")
        self.current_list_number = list_number

    def go_to_random_list(self) -> None:
        """Sets the current list number to a randomly selected list.

        Raises:
            ValueError: If the readinglist is empty.

        """
        self.check_if_empty()

        # Get a random index using the random.org API
        random_list = get_random(self.get_readinglist_length())

        logger.info(f"Setting current list number to random list: {random_list}")
        self.current_list_number = random_list

    def move_book_to_beginning(self, book_id: int) -> None:
        """Moves a book to the beginning of the readinglist.

        Args:
            book_id (int): The ID of the book to move.

        Raises:
            ValueError: If the readinglist is empty or the book ID is invalid.

        """
        logger.info(f"Moving book with ID {book_id} to the beginning of the readinglist")
        self.check_if_empty()
        book_id = self.validate_book_id(book_id)

        self.readinglist.remove(book_id)
        self.readinglist.insert(0, book_id)

        logger.info(f"Successfully moved book with ID {book_id} to the beginning")

    def move_book_to_end(self, book_id: int) -> None:
        """Moves a bok to the end of the readinglist.

        Args:
            book_id (int): The ID of the book to move.

        Raises:
            ValueError: If the readinglist is empty or the book ID is invalid.

        """
        logger.info(f"Moving book with ID {book_id} to the end of the readinglist")
        self.check_if_empty()
        book_id = self.validate_book_id(book_id)

        self.readinglist.remove(book_id)
        self.readinglist.append(book_id)

        logger.info(f"Successfully moved book with ID {book_id} to the end")

    def move_book_to_list_number(self, book_id: int, list_number: int) -> None:
        """Moves a book to a specific list number in the readinglist.

        Args:
            book_id (int): The ID of the book to move.
            list_number (int): The list number to move the book to (1-indexed).

        Raises:
            ValueError: If the readinglist is empty, the book ID is invalid, or the list number is out of range.

        """
        logger.info(f"Moving book with ID {book_id} to list number {list_number}")
        self.check_if_empty()
        book_id = self.validate_book_id(book_id)
        list_number = self.validate_list_number(list_number)

        readinglist_index = list_number - 1

        self.readinglist.remove(book_id)
        self.readinglist.insert(readinglist_index, book_id)

        logger.info(f"Successfully moved book with ID {book_id} to list number {list_number}")

    def swap_books_in_readinglist(self, book1_id: int, book2_id: int) -> None:
        """Swaps the positions of two books in the readinglist.

        Args:
            book1_id (int): The ID of the first book to swap.
            book2_id (int): The ID of the second book to swap.

        Raises:
            ValueError: If the readinglist is empty, either book ID is invalid, or attempting to swap the same book.

        """
        logger.info(f"Swapping book with IDs {book1_id} and {book2_id}")
        self.check_if_empty()
        book1_id = self.validate_book_id(book1_id)
        book2_id = self.validate_book_id(book2_id)

        if book1_id == book2_id:
            logger.error(f"Cannot swap a book with itself: {book1_id}")
            raise ValueError(f"Cannot swap a book with itself: {book1_id}")

        index1, index2 = self.readinglist.index(book1_id), self.readinglist.index(book2_id)

        self.readinglist[index1], self.readinglist[index2] = self.readinglist[index2], self.readinglist[index1]

        logger.info(f"Successfully swapped books with IDs {book1_id} and {book2_id}")


    ##################################################
    # Readinglist Read Functions
    ##################################################


    def read_current_book(self) -> None:
        """Reads the current book and advances the readinglist.

        Raises:
            ValueError: If the readinglist is empty.

        """
        self.check_if_empty()
        current_book = self.get_book_by_list_number(self.current_list_number)

        logger.info(f"Reading book: {current_book.title} (ID: {current_book.id}) at list number: {self.current_list_number}")
        current_book.update_read_count()
        logger.info(f"Updated read count for book: {current_book.title} (ID: {current_book.id})")

        self.current_list_number = (self.current_list_number % self.get_readinglist_length()) + 1
        logger.info(f"Advanced to list number: {self.current_list_number}")

    def read_entire_readinglist(self) -> None:
        """Reads all books in the readinglist from the beginning.

        Raises:
            ValueError: If the readinglist is empty.

        """
        self.check_if_empty()
        logger.info("Starting to read the entire readinglist.")

        self.current_list_number = 1
        for _ in range(self.get_readinglist_length()):
            self.read_current_book()

        logger.info("Finished reading the entire readinglist.")

    def read_rest_of_readinglist(self) -> None:
        """Reads the remaining books in the readinglist from the current list onward.

        Raises:
            ValueError: If the readinglist is empty.

        """
        self.check_if_empty()
        logger.info(f"Reading the rest of the readinglist from list number: {self.current_list_number}")

        for _ in range(self.get_readinglist_length() - self.current_list_number + 1):
            self.read_current_book()

        logger.info("Finished reading the rest of the readinglist.")

    def rewind_readinglist(self) -> None:
        """Resets the readinglist to the first list.

        Raises:
            ValueError: If the readinglist is empty.

        """
        self.check_if_empty()
        self.current_list_number = 1
        logger.info("Rewound readinglist to the first list.")


    ##################################################
    # Utility Functions
    ##################################################


    ####################################################################################################
    #
    # Note: I am only testing these things once. EG I am not testing that everything rejects an empty
    # list as they all do so by calling this helper
    #
    ####################################################################################################

    def validate_book_id(self, book_id: int, check_in_readinglist: bool = True) -> int:
        """
        Validates the given book ID.

        Args:
            book_id (int): The book ID to validate.
            check_in_readinglist (bool, optional): If True, verifies the ID is present in the readinglist.
                                                If False, skips that check. Defaults to True.

        Returns:
            int: The validated book ID.

        Raises:
            ValueError: If the book ID is not a non-negative integer,
                        not found in the readinglist (if check_in_readinglist=True),
                        or not found in the database.
        """
        try:
            book_id = int(book_id)
            if book_id < 0:
                raise ValueError
        except ValueError:
            logger.error(f"Invalid book id: {book_id}")
            raise ValueError(f"Invalid book id: {book_id}")

        if check_in_readinglist and book_id not in self.readinglist:
            logger.error(f"Book with id {book_id} not found in readinglist")
            raise ValueError(f"Book with id {book_id} not found in readinglist")

        try:
            self._get_book_from_cache_or_db(book_id)
        except Exception as e:
            logger.error(f"Book with id {book_id} not found in database: {e}")
            raise ValueError(f"Book with id {book_id} not found in database")

        return book_id

    def validate_list_number(self, list_number: int) -> int:
        """
        Validates the given list number, ensuring it is within the readinglist's range.

        Args:
            list_number (int): The list number to validate.

        Returns:
            int: The validated list number.

        Raises:
            ValueError: If the list number is not a valid positive integer or is out of range.

        """
        try:
            list_number = int(list_number)
            if not (1 <= list_number <= self.get_readinglist_length()):
                raise ValueError(f"Invalid list number: {list_number}")
        except ValueError as e:
            logger.error(f"Invalid list number: {list_number}")
            raise ValueError(f"Invalid list number: {list_number}") from e

        return list_number

    def check_if_empty(self) -> None:
        """
        Checks if the readinglist is empty and raises a ValueError if it is.

        Raises:
            ValueError: If the readinglist is empty.

        """
        if not self.readinglist:
            logger.error("Readinglist is empty")
            raise ValueError("Readinglist is empty")
