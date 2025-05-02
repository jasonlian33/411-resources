DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL CHECK(year >= 1900),
    genre TEXT NOT NULL,
    pagelength INTEGER NOT NULL CHECK(duration > 0),
    read_count INTEGER DEFAULT 0,
    UNIQUE(artist, title, year)
);

CREATE INDEX idx_books_author_title ON books(author, title);
CREATE INDEX idx_books_year ON books(year);
CREATE INDEX idx_books_read_count ON books(read_count);