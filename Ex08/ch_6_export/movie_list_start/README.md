# Movie List Console App

## Overview
This program is a Python console application for managing a small movie database.
You can view movies by category or year, add new movies, add new categories, and delete movies.

## How To Run
1. Open a terminal in this folder.
2. Run the program:

```bash
python ui.py
```

If your system uses `python3`, run:

```bash
python3 ui.py
```

## Command Reference
- `cat`: View movies in a selected category.
- `year`: View movies released in a selected year.
- `add`: Add a new movie (name, year, minutes, category ID).
- `addcat`: Add a new category by name.
- `del`: Delete a movie by movie ID.
- `exit`: Exit the program.

## Database Structure
The program uses SQLite with two tables:

### Category
- `categoryID` (INTEGER, primary key)
- `name` (TEXT)

### Movie
- `movieID` (INTEGER, primary key)
- `categoryID` (INTEGER, foreign key to `Category.categoryID`)
- `name` (TEXT)
- `year` (INTEGER)
- `minutes` (INTEGER)

A category can have many movies, and each movie belongs to one category.

## Example Usage
```text
The Movie List program

COMMAND MENU
cat    - View movies by category
year   - View movies by year
add    - Add a movie
addcat - Add a category
del    - Delete a movie
exit   - Exit program

Command: addcat
Category Name: Drama
Drama was added to database.

Command: add
Name: Interstellar
Year: 2014
Minutes: 169
Category ID: 4
Interstellar was added to database.

Command: year
Year: 2014

MOVIES - 2014
ID  Name                                  Year  Mins  Category
...
```

## Possible Future Improvements
- Validate movie IDs before deleting to avoid deleting non-existing records.
- Prevent duplicate category names.
- Add an `edit` command for updating movies.
- Add sorting options (name, year, runtime).
- Add automated tests for `db.py` and `ui.py`.
- Improve error handling for database connection failures.
