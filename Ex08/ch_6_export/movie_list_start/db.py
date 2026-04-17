import sqlite3
from pathlib import Path
from contextlib import closing

from objects import Category, Movie

conn = None

def connect():
    """
    Open a connection to the SQLite database.
    """
    global conn
    if not conn:
        DB_FILE = Path(__file__).resolve().parent / "movies.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    """
    Close the active database connection.
    """
    if conn:
        conn.close()

def make_category(row):
    """
    Convert a database row into a Category object.

    Args:
        row: The SQLite row containing category data.

    """
    return Category(row["categoryID"], row["categoryName"])

def make_movie(row):
    """
    Convert a database row into a Movie object.

    Args:
        row: The SQLite row containing movie and category data.

    """
    return Movie(row["movieID"], row["name"], row["year"], row["minutes"],
            make_category(row))

def make_movie_list(results):
    """
    Build a list of Movie objects from query results.

    Args:
        results: The rows returned by a movie query.

    """
    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

def get_categories() -> list[Category]:
    """
    Get all categories from the database.
    """
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id: int) -> Category | None:
    """
    Get one category by its ID.
    """
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_movies_by_category(category_id: int) -> list[Movie]:
    """
    Get all movies that belong to one category.

    Args:
        category_id: The category ID to filter by.

    """
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    return make_movie_list(results)

def get_movies_by_year(year: int) -> list[Movie]:
    """
    Get all movies released in a given year.

    Args:
        year: The release year to filter by.

    """
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    return make_movie_list(results)

def add_movie(movie: Movie) -> None:
    """
    Insert a new movie into the database.
    """
    sql = '''INSERT INTO Movie (categoryID, name, year, minutes) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie.category.id, movie.name, movie.year,
                        movie.minutes))
        conn.commit()

def add_category(name: str) -> None:
    """
    Insert a new category into the database.
    """
    sql = '''INSERT INTO Category (name) 
             VALUES (?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (name,))
        conn.commit()

def delete_movie(movie_id: int) -> None:
    """
    Delete a movie from the database by ID.
    """
    sql = '''DELETE FROM Movie WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie_id,))
        conn.commit()