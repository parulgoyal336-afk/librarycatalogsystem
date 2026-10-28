# 📚 Library Catalog System

A library catalog application written in **Python** that demonstrates object-oriented programming (classes, inheritance, encapsulation) with both a **command-line interface** and a **Tkinter graphical interface**.

Developed as a lab project for **Python Programming (CONT_26CAH-606)**, BCA Semester VI.

## Features
- Add books of three types: Fiction, Non-Fiction and Reference
- Remove books (with confirmation)
- Search by title or author (live search in the GUI)
- Filter by Available, Borrowed, Fiction, Non-Fiction or Reference
- Borrow and return books; reference books cannot be borrowed
- Live counters for total, available and borrowed books
- Input validation and clear error messages

## OOP Concepts Used
| Class | Description |
|---|---|
| `Book` | Parent class with title, author, genre and availability |
| `FictionBook`, `NonFictionBook`, `ReferenceBook` | Subclasses that inherit from `Book` and add their own attributes |
| `Library` | Manages the collection: add, remove, search, borrow, return |
| `LibraryApp`, `AddBookDialog` | Tkinter GUI classes |

## Tech Stack
- Python 3.8+
- Tkinter / ttk (included with Python, no extra packages needed)

## How to Run
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/library-catalog-system.git
cd library-catalog-system

# 2. Run the GUI version
python library_gui.py

# 3. Or run the command-line version
python library_catalog.py
```

## Documentation
The full project report and flowchart are in the [`docs/`](docs/) folder.

## Future Improvements
- Save the catalog to a file or database (SQLite)
- Member login, due dates and fines
- Reports and export to Excel/PDF

## Author
**<Your Name>**, BCA, Semester VI
