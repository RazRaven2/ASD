from dataclasses import dataclass

@dataclass
class Category:
    """
    Store category data for a movie category.

    Args:
        id: The category ID.
        name: The category name.

    Returns:
        Category: A category data object.
    """
    id:int = 0
    name:str = ""
        
@dataclass
class Movie:
    """
    Store movie data including its category.

    Args:
        id: The movie ID.
        name: The movie title.
        year: The release year.
        minutes: The runtime in minutes.
        category: The category object for the movie.

    Returns:
        Movie: A movie data object.
    """
    id:int = 0
    name:str = ""
    year:int = 0
    minutes:int = 0
    category:Category = None
