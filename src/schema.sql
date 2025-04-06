CREATE TABLE authors (
    author_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE
);

CREATE TABLE publishers (
    publisher_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50),
    validation_year DATE
);

CREATE TABLE books (
    book_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(60),
    author_id INT REFERENCES authors(author_id) ON DELETE CASCADE,
    publisher_id INT REFERENCES publishers(publisher_id) ON DELETE SET NULL,
    publish_date DATE,
    isbn VARCHAR(17)
);

CREATE TABLE genres (
    genre_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE book_genre (
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    genre_id INT REFERENCES genres(genre_id) ON DELETE CASCADE,
    UNIQUE (book_id, genre_id)
);

CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    email VARCHAR(80) UNIQUE,
    password TEXT
);

CREATE TABLE history (
    history_id BIGSERIAL PRIMARY KEY,
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    operation VARCHAR(50),
    operation_date DATE
);

CREATE TABLE storage (
    storage_id BIGSERIAL PRIMARY KEY,
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    count INT CHECK (count >= 0)
);


INSERT INTO authors (first_name, last_name, birth_date)
VALUES ('George', 'Orwell', '1903-06-25'),
       ('J.K.', 'Rowling', '1965-07-31'),
       ('J.R.R.', 'Tolkien', '1892-01-03'),
       ('Harper', 'Lee', '1926-04-28'),
       ('Isaac', 'Asimov', '1920-01-02');

INSERT INTO publishers (name, validation_year)
VALUES
    ('Penguin Books', '2005-12-01'),
    ('Bloomsbury Publishing', '2012-07-03'),
    ('HarperCollins', '2017-05-30'),
    ('Houghton Mifflin Harcourt', '2024-11-12');

INSERT INTO books (name, author_id, publisher_id, publish_date, isbn)
VALUES ('1984', 1, 1, '1949-06-08', '978-0-452-52983-4'),
       ('Harry Potter and the Sorcerer''s Stone', 2, 2, '1997-06-26', '978-0-7475-3269-9'),
       ('The Hobbit', 3, 3, '1937-09-21', '978-0-618-96863-3'),
       ('To Kill a Mockingbird', 4, 4, '1960-07-11', '978-0-06-112008-4'),
       ('Foundation', 5, 1, '1951-06-01', '978-0-553-80371-0'),
       ('The Catcher in the Rye', 4, 2, '1951-07-16', '978-0-316-76948-0'),
       ('The Fellowship of the Ring', 3, 3, '1954-07-29', '978-0-618-00222-8'),
       ('Brave New World', 1, 4, '1932-08-01', '978-0-06-085052-1');

INSERT INTO genres (name)
VALUES ('Dystopian'),
       ('Fantasy'),
       ('Adventure'),
       ('Classics'),
       ('Science Fiction'),
       ('Mystery'),
       ('Romance'),
       ('Historical Fiction'),
       ('Horror'),
       ('Thriller');

INSERT INTO book_genre (book_id, genre_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
       (5, 5),
       (6, 6),
       (7, 3),
       (8, 1);

INSERT INTO users (first_name, last_name, birth_date, email, password)
VALUES ('John', 'Doe', '1990-01-15', 'johndoe@example.com', 'password123'),
       ('Alice', 'Smith', '1985-06-22', 'alicesmith@example.com', 'password456'),
       ('Bob', 'Johnson', '1978-11-09', 'bobjohnson@example.com', 'password789');

INSERT INTO history (book_id, user_id, operation, operation_date)
VALUES (1, 1, 'Borrowed', '2025-04-01'),
       (2, 1, 'Returned', '2022-04-02'),
       (3, 3, 'Borrowed', '2023-04-03'),
       (4, 2, 'Borrowed', '2023-04-04'),
       (5, 2, 'Returned', '2023-04-05'),
       (6, 3, 'Borrowed', '2022-04-06'),
       (7, 2, 'Returned', '2022-04-07'),
       (8, 3, 'Borrowed', '2024-04-08');

INSERT INTO storage (book_id, count)
VALUES (1, 12),
       (2, 8),
       (3, 10),
       (4, 6),
       (5, 15),
       (6, 9),
       (7, 7),
       (8, 5);