"""
Library Catalog System
Covers:
  Experiment 7  - Basic Python concepts (Book class, methods)
  Experiment 8  - Inheritance (Fiction, NonFiction, Reference books)
  Experiment 9  - Project structure (Library class: add/remove/search/display)
  Experiment 10 - User interaction (command-line interface)
"""


# ---------------------------------------------------------------
# Experiment 7: Basic Python Concepts - Book class
# ---------------------------------------------------------------
class Book:
    def __init__(self, title, author, genre, available=True):
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

    def display_details(self):
        status = "Available" if self.available else "Borrowed"
        print(f"Title : {self.title}")
        print(f"Author: {self.author}")
        print(f"Genre : {self.genre}")
        print(f"Status: {status}")

    def check_availability(self):
        return self.available

    def update_availability(self, status):
        self.available = status


# ---------------------------------------------------------------
# Experiment 8: Inheritance - subclasses of Book
# ---------------------------------------------------------------
class FictionBook(Book):
    def __init__(self, title, author, fiction_type, available=True):
        super().__init__(title, author, "Fiction", available)
        self.fiction_type = fiction_type  # e.g. Mystery, Fantasy, Sci-Fi

    def display_details(self):
        super().display_details()
        print(f"Type  : {self.fiction_type}")


class NonFictionBook(Book):
    def __init__(self, title, author, subject, available=True):
        super().__init__(title, author, "Non-Fiction", available)
        self.subject = subject  # e.g. History, Science

    def display_details(self):
        super().display_details()
        print(f"Subject: {self.subject}")


class ReferenceBook(Book):
    """Reference books are for in-library use only and cannot be borrowed."""

    def __init__(self, title, author, edition, available=True):
        super().__init__(title, author, "Reference", available)
        self.edition = edition

    def display_details(self):
        super().display_details()
        print(f"Edition: {self.edition}")
        print("Note  : In-library use only")


# ---------------------------------------------------------------
# Experiment 9: Project Structure - Library class
# ---------------------------------------------------------------
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"'{book.title}' added to the catalog.")

    def remove_book(self, title):
        book = self.find_by_title(title)
        if book:
            self.books.remove(book)
            print(f"'{book.title}' removed from the catalog.")
        else:
            print("Book not found.")

    def find_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def search(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books
                if keyword in b.title.lower() or keyword in b.author.lower()]

    def display_available(self):
        available = [b for b in self.books if b.check_availability()]
        if not available:
            print("No books are currently available.")
            return
        for book in available:
            book.display_details()
            print("-" * 30)

    def display_all(self):
        if not self.books:
            print("The catalog is empty.")
            return
        for book in self.books:
            book.display_details()
            print("-" * 30)

    def borrow_book(self, title):
        book = self.find_by_title(title)
        if not book:
            print("Book not found.")
        elif isinstance(book, ReferenceBook):
            print("Reference books cannot be borrowed.")
        elif not book.check_availability():
            print("Sorry, this book is already borrowed.")
        else:
            book.update_availability(False)
            print(f"You have borrowed '{book.title}'.")

    def return_book(self, title):
        book = self.find_by_title(title)
        if not book:
            print("Book not found.")
        elif book.check_availability():
            print("This book was not borrowed.")
        else:
            book.update_availability(True)
            print(f"Thank you for returning '{book.title}'.")


# ---------------------------------------------------------------
# Experiment 10: User Interaction - Command Line Interface
# ---------------------------------------------------------------
def add_book_menu(library):
    print("\nBook type:  1. Fiction   2. Non-Fiction   3. Reference")
    choice = input("Choose type: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()

    if choice == "1":
        library.add_book(FictionBook(title, author, input("Fiction type (e.g. Mystery): ").strip()))
    elif choice == "2":
        library.add_book(NonFictionBook(title, author, input("Subject: ").strip()))
    elif choice == "3":
        library.add_book(ReferenceBook(title, author, input("Edition: ").strip()))
    else:
        print("Invalid book type.")


def main():
    library = Library()

    # Sample data so the catalog is not empty on first run
    library.books.extend([
        FictionBook("The Hobbit", "J.R.R. Tolkien", "Fantasy"),
        NonFictionBook("Sapiens", "Yuval Noah Harari", "History"),
        ReferenceBook("Oxford English Dictionary", "Oxford Press", "2nd"),
    ])

    menu = """
===== LIBRARY CATALOG SYSTEM =====
1. Add a book
2. Remove a book
3. Search books (title/author)
4. Display available books
5. Display all books
6. Borrow a book
7. Return a book
8. Exit
"""
    while True:
        print(menu)
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_book_menu(library)
        elif choice == "2":
            library.remove_book(input("Title to remove: ").strip())
        elif choice == "3":
            results = library.search(input("Search keyword: ").strip())
            if results:
                for book in results:
                    book.display_details()
                    print("-" * 30)
            else:
                print("No matching books found.")
        elif choice == "4":
            library.display_available()
        elif choice == "5":
            library.display_all()
        elif choice == "6":
            library.borrow_book(input("Title to borrow: ").strip())
        elif choice == "7":
            library.return_book(input("Title to return: ").strip())
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
