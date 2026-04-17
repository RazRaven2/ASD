#!/usr/bin/env/python3

import db
from objects import Category, Movie

def display_welcome() -> None:
    print("The Movie List program")
    print()    
    display_menu()

def display_menu() -> None:
    print("COMMAND MENU")
    print("cat    - View movies by category")
    print("year   - View movies by year")
    print("add    - Add a movie")
    print("addcat - Add a category")
    print("del    - Delete a movie")
    print("exit   - Exit program")
    print()    

def display_categories() -> None:
    print("CATEGORIES")
    categories = db.get_categories()    
    for category in categories:
        print(f"{category.id}. {category.name}")
    print()

def prompt_for_category() -> Category | None:
    """Prompt user for category ID, validate existence, return Category or None."""
    category_id = get_int("Category ID: ")
    category = db.get_category(category_id)
    if category is None:
        print("There is no category with that ID.\n")
        return None
    return category

def display_movies_generic(fetch_fn, title_term: str) -> None:
    """Generic helper to fetch and display a movie list."""
    print()
    movies = fetch_fn()
    display_movies(movies, title_term)
    
def display_movies(movies: list[Movie], title_term: str) -> None:
    print(f"MOVIES - {title_term}")

    print(f"{'ID':<4}{'Name':<38}{'Year':<6}{'Mins':<6}{'Category':<10}")
    print("-" * 63)
    for movie in movies:
        print(f"{movie.id:<4d}{movie.name:<38}{movie.year:<6d}"
              f"{movie.minutes:<6d}{movie.category.name:<10}")
    print()  

def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid whole number. Please try again.\n")

def display_movies_by_category() -> None:
    category = prompt_for_category()
    if category is not None:
        display_movies_generic(lambda: db.get_movies_by_category(category.id), 
                               category.name.upper())

def display_movies_by_year() -> None:
    year = get_int("Year: ")
    display_movies_generic(lambda: db.get_movies_by_year(year), str(year))

def add_movie() -> None:
    name        = input("Name: ")
    year        = get_int("Year: ")
    minutes     = get_int("Minutes: ")
    
    category = prompt_for_category()
    if category is None:
        print("Movie NOT added.\n")
    else:
        movie = Movie(name=name, year=year, minutes=minutes,
                      category=category)
        db.add_movie(movie)
        print(f"{name} was added to database.\n")
    
def delete_movie() -> None:
    movie_id = get_int("Movie ID: ")
    db.delete_movie(movie_id)
    print(f"Movie ID {movie_id} was deleted from database.\n")

def add_category() -> None:
    name = input("Category Name: ")
    db.add_category(name)
    print(f"{name} was added to database.\n")

COMMANDS = {
    "cat": display_movies_by_category,
    "year": display_movies_by_year,
    "add": add_movie,
    "addcat": add_category,
    "del": delete_movie,
}
        
def main() -> None:
    db.connect()
    display_welcome()
    display_categories()
    
    while True:        
        command = input("Command: ").lower()
        if command == "exit":
            break
        elif command in COMMANDS:
            COMMANDS[command]()
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()
            
    db.close()
    print("Bye!")

if __name__ == "__main__":
    main()
