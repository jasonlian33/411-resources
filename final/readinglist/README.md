# Reading List API

## Overview

This Flask-based RESTful API allows users to:

- Register, authenticate, and manage their account.
- Create, read, update, and delete books in a shared catalog.
- Maintain a personal reading list: add/remove books, navigate through it, “read” books programmatically, and rearrange entries.
- View reading list statistics and a leaderboard of popular books by read count.

Authentication is managed via Flask-Login.

---

## Endpoints

### 1. Health Check

- **Route:** `/api/health`
- **Method:** GET
- **Purpose:** Verify that the service is up and running.
- **Request Parameters:** None
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/health
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Service is running"
  }
  ```

---

## User Management

### 2. Create User

- **Route:** `/api/create-user`
- **Method:** PUT
- **Purpose:** Register a new user account.
- **Request Body (JSON):**
  - `username` (string, required)
  - `password` (string, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "username": "alice", "password": "secret" }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "User 'alice' created successfully"
  }
  ```

### 3. Login

- **Route:** `/api/login`
- **Method:** POST
- **Purpose:** Authenticate a user.
- **Request Body (JSON):**
  - `username` (string, required)
  - `password` (string, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "username": "alice", "password": "secret" }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "User 'alice' logged in successfully"
  }
  ```

### 4. Logout

- **Route:** `/api/logout`
- **Method:** POST
- **Purpose:** Log out the current user.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/logout
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "User logged out successfully"
  }
  ```

### 5. Change Password

- **Route:** `/api/change-password`
- **Method:** POST
- **Purpose:** Change the current user’s password.
- **Authentication:** Required
- **Request Body (JSON):**
  - `new_password` (string, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "new_password": "newsecret" }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Password changed successfully"
  }
  ```

### 6. Reset Users

- **Route:** `/api/reset-users`
- **Method:** DELETE
- **Purpose:** Drop and recreate the users table (deletes all users).
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X DELETE http://localhost:5001/api/reset-users
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Users table recreated successfully"
  }
  ```

---

## Book Catalog

### 7. Reset Books

- **Route:** `/api/reset-books`
- **Method:** DELETE
- **Purpose:** Drop and recreate the books table (deletes all books).
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X DELETE http://localhost:5001/api/reset-books
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Books table recreated successfully"
  }
  ```

### 8. Create Book

- **Route:** `/api/create-book`
- **Method:** POST
- **Purpose:** Add a new book to the catalog.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string, required)
  - `title` (string, required)
  - `year` (integer, required)
  - `genre` (string, required)
  - `length` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  {
    "author": "George Orwell",
    "title": "1984",
    "year": 1949,
    "genre": "Dystopian",
    "length": 328
  }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book '1984' by George Orwell added successfully"
  }
  ```

### 9. Delete Book

- **Route:** `/api/delete-book/<book_id>`
- **Method:** DELETE
- **Purpose:** Remove a book from the catalog by ID.
- **Authentication:** Required
- **Path Parameters:**
  - `book_id` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X DELETE http://localhost:5001/api/delete-book/1
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book with ID 1 deleted successfully"
  }
  ```

### 10. Get All Books (Catalog)

- **Route:** `/api/get-all-books-from-catalog`
- **Method:** GET
- **Purpose:** Retrieve all non-deleted books; optionally sort by read count.
- **Authentication:** Required
- **Query Parameters:**
  - `sort_by_read_count` (bool, optional; default `false`)
- **Response:**
  - `status` (string)
  - `message` (string)
  - `books` (array of objects)
- **Example Request:**

  ```
  curl -X GET "http://localhost:5001/api/get-all-books-from-catalog?sort_by_read_count=true"
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Books retrieved successfully",
    "books": [
      { "id": 2, "author": "Orwell", "title": "Animal Farm", "year": 1945, "genre": "Political Satire", "length": 112, "read_count": 5 },
      { "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328, "read_count": 3 }
    ]
  }
  ```

### 11. Get Book by ID (Catalog)

- **Route:** `/api/get-book-from-catalog-by-id/<book_id>`
- **Method:** GET
- **Purpose:** Retrieve a specific book by its ID.
- **Authentication:** Required
- **Path Parameters:**
  - `book_id` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
  - `book` (object)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-book-from-catalog-by-id/1
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book retrieved successfully",
    "book": { "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328, "read_count": 3 }
  }
  ```

### 12. Get Book by Compound Key

- **Route:** `/api/get-book-from-catalog-by-compound-key`
- **Method:** GET
- **Purpose:** Retrieve a book by author, title, and year.
- **Authentication:** Required
- **Query Parameters:**
  - `author` (string, required)
  - `title` (string, required)
  - `year` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
  - `book` (object)
- **Example Request:**

  ```
  curl -G http://localhost:5001/api/get-book-from-catalog-by-compound-key \
    --data-urlencode "author=Orwell" \
    --data-urlencode "title=1984" \
    --data-urlencode "year=1949"
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book retrieved successfully",
    "book": { "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328, "read_count": 3 }
  }
  ```

### 13. Get Random Book

- **Route:** `/api/get-random-book`
- **Method:** GET
- **Purpose:** Retrieve a random book from the catalog.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
  - `book` (object)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-random-book
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Random book retrieved successfully",
    "book": { "id": 2, "author": "Orwell", "title": "Animal Farm", "year": 1945, "genre": "Political Satire", "length": 112, "read_count": 5 }
  }
  ```

---

## Reading List: Add / Remove

### 14. Add Book to Reading List

- **Route:** `/api/add-book-to-reading-list`
- **Method:** POST
- **Purpose:** Add a catalog book by compound key to the user’s reading list.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string, required)
  - `title` (string, required)
  - `year` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "author": "Orwell", "title": "1984", "year": 1949 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book '1984' by Orwell (1949) added to reading list"
  }
  ```

### 15. Remove Book by Compound Key

- **Route:** `/api/remove-book-from-reading-list`
- **Method:** DELETE
- **Purpose:** Remove a book from the reading list by compound key.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string, required)
  - `title` (string, required)
  - `year` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "author": "Orwell", "title": "1984", "year": 1949 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book '1984' by Orwell (1949) removed from reading list"
  }
  ```

### 16. Remove Book by Selection Number

- **Route:** `/api/remove-book-from-reading-list-by-selection-number/<selection_number>`
- **Method:** DELETE
- **Purpose:** Remove a book from the reading list by its selection index.
- **Authentication:** Required
- **Path Parameters:**
  - `selection_number` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X DELETE http://localhost:5001/api/remove-book-from-reading-list-by-selection-number/1
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book at selection number 1 removed from reading list"
  }
  ```

### 17. Clear Reading List

- **Route:** `/api/clear-reading-list`
- **Method:** POST
- **Purpose:** Remove all books from the reading list.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/clear-reading-list
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Reading List cleared"
  }
  ```

---

## Reading List: “Reading” Operations

### 18. Read Current Book

- **Route:** `/api/read-current-book`
- **Method:** POST
- **Purpose:** Mark the current reading-list book as read and advance the pointer.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
  - `book` (object: the book just read)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/read-current-book
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Now reading current book",
    "book": {
      "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328
    }
  }
  ```

### 19. Read Entire Reading List

- **Route:** `/api/read-entire-reading-list`
- **Method:** POST
- **Purpose:** Mark all books in the reading list as read.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/read-entire-reading-list
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Reading entire reading list"
  }
  ```

### 20. Read Rest of Reading List

- **Route:** `/api/read-rest-of-reading-list`
- **Method:** POST
- **Purpose:** Mark all remaining books from the current pointer onward as read.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/read-rest-of-reading-list
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Reading rest of the reading list"
  }
  ```

### 21. Rewind Reading List

- **Route:** `/api/rewind-reading-list`
- **Method:** POST
- **Purpose:** Reset the current pointer to the first book.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/rewind-reading-list
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Reading List rewound to the first book"
  }
  ```

### 22. Go to Selection Number

- **Route:** `/api/go-to-selection-number/<selection_number>`
- **Method:** POST
- **Purpose:** Set the current pointer to a specific selection index.
- **Authentication:** Required
- **Path Parameters:**
  - `selection_number` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/go-to-selection-number/2
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Now reading from selection number 2"
  }
  ```

### 23. Go to Random Selection

- **Route:** `/api/go-to-random-selection`
- **Method:** POST
- **Purpose:** Set the current pointer to a random book in the reading list.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```
  curl -X POST http://localhost:5001/api/go-to-random-selection
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Now reading from random selection number 3"
  }
  ```

---

## Reading List: Viewing

### 24. Get All Books (Reading List)

- **Route:** `/api/get-all-books-from-reading-list`
- **Method:** GET
- **Purpose:** Retrieve all books in the user’s reading list.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `books` (array of objects)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-all-books-from-reading-list
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "books": [
      { "selection": 1, "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328 },
      { "selection": 2, "id": 2, "author": "Orwell", "title": "Animal Farm", "year": 1945, "genre": "Political Satire", "length": 112 }
    ]
  }
  ```

### 25. Get Book by Selection Number

- **Route:** `/api/get-book-from-reading-list-by-selection-number/<selection_number>`
- **Method:** GET
- **Purpose:** Retrieve a specific book from the reading list by its index.
- **Authentication:** Required
- **Path Parameters:**
  - `selection_number` (integer)
- **Response:**
  - `status` (string)
  - `book` (object)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-book-from-reading-list-by-selection-number/1
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "book": { "selection": 1, "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328 }
  }
  ```

### 26. Get Current Book

- **Route:** `/api/get-current-book`
- **Method:** GET
- **Purpose:** Retrieve the book at the current reading-list pointer.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `current_book` (object)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-current-book
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "current_book": { "selection": 1, "id": 1, "author": "Orwell", "title": "1984", "year": 1949, "genre": "Dystopian", "length": 328 }
  }
  ```

### 27. Get Reading List Length

- **Route:** `/api/get-reading-list-length`
- **Method:** GET
- **Purpose:** Retrieve the number of books and total pages in the reading list.
- **Authentication:** Required
- **Response:**
  - `status` (string)
  - `readinglist_length` (integer)
  - `readinglist_page_count` (integer)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/get-reading-list-length
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "readinglist_length": 2,
    "readinglist_page_count": 440
  }
  ```

---

## Arrange Reading List

### 28. Move Book to Beginning

- **Route:** `/api/move-book-to-beginning`
- **Method:** POST
- **Purpose:** Reorder a reading-list book to the first position.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string, required)
  - `title` (string, required)
  - `year` (integer, required)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "author": "Orwell", "title": "Animal Farm", "year": 1945 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book 'Animal Farm' by Orwell moved to beginning"
  }
  ```

### 29. Move Book to End

- **Route:** `/api/move-book-to-end`
- **Method:** POST
- **Purpose:** Reorder a reading-list book to the last position.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string)
  - `title` (string)
  - `year` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "author": "Orwell", "title": "1984", "year": 1949 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book '1984' by Orwell moved to end"
  }
  ```

### 30. Move Book to Selection Number

- **Route:** `/api/move-book-to-selection-number`
- **Method:** POST
- **Purpose:** Reorder a reading-list book to a specific index.
- **Authentication:** Required
- **Request Body (JSON):**
  - `author` (string)
  - `title` (string)
  - `year` (integer)
  - `selection_number` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "author": "Orwell", "title": "1984", "year": 1949, "selection_number": 1 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Book '1984' by Orwell moved to selection 1"
  }
  ```

### 31. Swap Books in Reading List

- **Route:** `/api/swap-books-in-reading-list`
- **Method:** POST
- **Purpose:** Swap two books by their selection indices.
- **Authentication:** Required
- **Request Body (JSON):**
  - `selection_number_1` (integer)
  - `selection_number_2` (integer)
- **Response:**
  - `status` (string)
  - `message` (string)
- **Example Request:**

  ```json
  { "selection_number_1": 1, "selection_number_2": 2 }
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "message": "Swapped books: Orwell - 1984 <-> Orwell - Animal Farm"
  }
  ```

---

## Leaderboard / Stats

### 32. Book Leaderboard

- **Route:** `/api/book-leaderboard`
- **Method:** GET
- **Purpose:** Retrieve a leaderboard of catalog books sorted by read count.
- **Response:**
  - `status` (string)
  - `leaderboard` (array of book objects)
- **Example Request:**

  ```
  curl -X GET http://localhost:5001/api/book-leaderboard
  ```

- **Example Response:**

  ```json
  {
    "status": "success",
    "leaderboard": [
      {
        "id": 2,
        "author": "Orwell",
        "title": "Animal Farm",
        "year": 1945,
        "genre": "Political Satire",
        "length": 112,
        "read_count": 5
      },
      {
        "id": 1,
        "author": "Orwell",
        "title": "1984",
        "year": 1949,
        "genre": "Dystopian",
        "length": 328,
        "read_count": 3
      }
    ]
  }
  ```
