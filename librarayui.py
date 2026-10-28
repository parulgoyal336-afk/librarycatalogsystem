"""
Library Catalog System - Graphical User Interface (Tkinter)
Run:  python library_gui.py
Requires library_catalog.py in the same folder (reuses its classes).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from library_catalog import (
    Library, FictionBook, NonFictionBook, ReferenceBook,
)

# ---------- Colour palette ----------
NAVY = "#1f2a44"
ACCENT = "#2f6fed"
ACCENT_DARK = "#2457be"
BG = "#f4f6fb"
CARD = "#ffffff"
TEXT = "#1f2937"
MUTED = "#6b7280"
GREEN = "#15803d"
RED = "#b91c1c"
ROW_ALT = "#f8faff"
ROW_BORROWED = "#fff1f1"

TYPE_FIELDS = {
    "Fiction": "Fiction Type (e.g. Mystery)",
    "Non-Fiction": "Subject (e.g. History)",
    "Reference": "Edition (e.g. 2nd)",
}


def extra_info(book):
    """Return the subclass-specific detail for display in the table."""
    if isinstance(book, FictionBook):
        return book.fiction_type
    if isinstance(book, NonFictionBook):
        return book.subject
    if isinstance(book, ReferenceBook):
        return f"{book.edition} edition"
    return ""


class AddBookDialog(tk.Toplevel):
    """Popup form for adding a new book."""

    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save
        self.title("Add New Book")
        self.configure(bg=CARD, padx=24, pady=20)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Add New Book", font=("Segoe UI", 15, "bold"),
                 bg=CARD, fg=NAVY).grid(row=0, column=0, columnspan=2,
                                        sticky="w", pady=(0, 14))

        self.type_var = tk.StringVar(value="Fiction")
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.extra_var = tk.StringVar()

        self._label("Book Type", 1)
        combo = ttk.Combobox(self, textvariable=self.type_var, state="readonly",
                             values=list(TYPE_FIELDS), width=34)
        combo.grid(row=1, column=1, pady=6, padx=(12, 0))
        combo.bind("<<ComboboxSelected>>", self._update_extra_label)

        self._label("Title", 2)
        self.title_entry = ttk.Entry(self, textvariable=self.title_var, width=37)
        self.title_entry.grid(row=2, column=1, pady=6, padx=(12, 0))

        self._label("Author", 3)
        ttk.Entry(self, textvariable=self.author_var, width=37).grid(
            row=3, column=1, pady=6, padx=(12, 0))

        self.extra_label = self._label(TYPE_FIELDS["Fiction"], 4)
        ttk.Entry(self, textvariable=self.extra_var, width=37).grid(
            row=4, column=1, pady=6, padx=(12, 0))

        btns = tk.Frame(self, bg=CARD)
        btns.grid(row=5, column=0, columnspan=2, sticky="e", pady=(16, 0))
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(btns, text="Save Book", style="Accent.TButton",
                   command=self._save).pack(side="right", padx=8)

        self.title_entry.focus_set()
        self.bind("<Return>", lambda e: self._save())
        self.bind("<Escape>", lambda e: self.destroy())

    def _label(self, text, row):
        lbl = tk.Label(self, text=text, bg=CARD, fg=MUTED,
                       font=("Segoe UI", 10), anchor="w", width=26)
        lbl.grid(row=row, column=0, sticky="w")
        return lbl

    def _update_extra_label(self, _event=None):
        self.extra_label.config(text=TYPE_FIELDS[self.type_var.get()])

    def _save(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        extra = self.extra_var.get().strip()
        if not title or not author or not extra:
            messagebox.showwarning("Missing details",
                                   "Please fill in all fields.", parent=self)
            return
        kind = self.type_var.get()
        if kind == "Fiction":
            book = FictionBook(title, author, extra)
        elif kind == "Non-Fiction":
            book = NonFictionBook(title, author, extra)
        else:
            book = ReferenceBook(title, author, extra)
        self.on_save(book)
        self.destroy()


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Catalog System")
        self.geometry("1000x620")
        self.minsize(860, 520)
        self.configure(bg=BG)

        self.library = Library()
        self._load_sample_data()

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        self._setup_styles()
        self._build_header()
        self._build_toolbar()
        self._build_table()
        self._build_statusbar()

        self.search_var.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    # ---------- setup ----------
    def _load_sample_data(self):
        self.library.books.extend([
            FictionBook("The Hobbit", "J.R.R. Tolkien", "Fantasy"),
            FictionBook("Gone Girl", "Gillian Flynn", "Thriller"),
            NonFictionBook("Sapiens", "Yuval Noah Harari", "History"),
            NonFictionBook("Atomic Habits", "James Clear", "Self-Help"),
            ReferenceBook("Oxford English Dictionary", "Oxford Press", "2nd"),
            ReferenceBook("Encyclopaedia Britannica", "Britannica", "15th"),
        ])

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=CARD, fieldbackground=CARD,
                        foreground=TEXT, rowheight=34, borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=NAVY, foreground="white",
                        font=("Segoe UI", 10, "bold"), relief="flat", padding=8)
        style.map("Treeview.Heading", background=[("active", NAVY)])
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])
        style.configure("TButton", font=("Segoe UI", 10), padding=(14, 7))
        style.configure("Accent.TButton", background=ACCENT, foreground="white")
        style.map("Accent.TButton",
                  background=[("active", ACCENT_DARK), ("pressed", ACCENT_DARK)])
        style.configure("TCombobox", padding=5)

    def _build_header(self):
        header = tk.Frame(self, bg=NAVY, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="\U0001F4DA  Library Catalog System",
                 font=("Segoe UI", 18, "bold"), bg=NAVY, fg="white"
                 ).pack(side="left", padx=24)
        self.stats_label = tk.Label(header, font=("Segoe UI", 10),
                                    bg=NAVY, fg="#c7d2fe")
        self.stats_label.pack(side="right", padx=24)

    def _build_toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=(18, 8))

        tk.Label(bar, text="Search", bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).pack(side="left")
        entry = ttk.Entry(bar, textvariable=self.search_var, width=32,
                          font=("Segoe UI", 10))
        entry.pack(side="left", padx=(8, 16), ipady=3)
        entry.focus_set()

        tk.Label(bar, text="Show", bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).pack(side="left")
        flt = ttk.Combobox(bar, textvariable=self.filter_var, state="readonly",
                           values=["All", "Available", "Borrowed",
                                   "Fiction", "Non-Fiction", "Reference"],
                           width=12)
        flt.pack(side="left", padx=8)
        flt.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        ttk.Button(bar, text="+ Add Book", style="Accent.TButton",
                   command=self.open_add).pack(side="right")

    def _build_table(self):
        card = tk.Frame(self, bg=CARD, highlightbackground="#e5e7eb",
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=24, pady=(4, 8))

        cols = ("title", "author", "genre", "details", "status")
        self.tree = ttk.Treeview(card, columns=cols, show="headings",
                                 selectmode="browse")
        for col, text, width in [("title", "Title", 260),
                                 ("author", "Author", 190),
                                 ("genre", "Genre", 110),
                                 ("details", "Details", 150),
                                 ("status", "Status", 100)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w")
        self.tree.tag_configure("odd", background=ROW_ALT)
        self.tree.tag_configure("borrowed", background=ROW_BORROWED)

        scroll = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", lambda e: self._update_buttons())
        self.tree.bind("<Double-1>", lambda e: self.show_details())
        self.tree.bind("<Delete>", lambda e: self.remove_selected())

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=24, pady=(0, 10))
        self.btn_details = ttk.Button(actions, text="View Details",
                                      command=self.show_details)
        self.btn_borrow = ttk.Button(actions, text="Borrow",
                                     style="Accent.TButton",
                                     command=self.borrow_selected)
        self.btn_return = ttk.Button(actions, text="Return",
                                     command=self.return_selected)
        self.btn_remove = ttk.Button(actions, text="Remove",
                                     command=self.remove_selected)
        for b in (self.btn_details, self.btn_borrow, self.btn_return):
            b.pack(side="left", padx=(0, 8))
        self.btn_remove.pack(side="right")
        self._update_buttons()

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status_var, anchor="w", bg="#e5e7eb",
                 fg=MUTED, font=("Segoe UI", 9), padx=24, pady=4
                 ).pack(fill="x", side="bottom")

    # ---------- helpers ----------
    def set_status(self, msg):
        self.status_var.set(msg)

    def selected_book(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.library.books[int(sel[0])]

    def _matches(self, book):
        kw = self.search_var.get().strip().lower()
        if kw and kw not in book.title.lower() and kw not in book.author.lower():
            return False
        f = self.filter_var.get()
        if f == "Available":
            return book.check_availability()
        if f == "Borrowed":
            return not book.check_availability()
        if f in ("Fiction", "Non-Fiction", "Reference"):
            return book.genre == f
        return True

    def refresh(self):
        selected = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for idx, book in enumerate(self.library.books):
            if not self._matches(book):
                continue
            tags = []
            if not book.check_availability():
                tags.append("borrowed")
            elif shown % 2:
                tags.append("odd")
            status = "Available" if book.check_availability() else "Borrowed"
            self.tree.insert("", "end", iid=str(idx), tags=tags,
                             values=(book.title, book.author, book.genre,
                                     extra_info(book), status))
            shown += 1
        if selected and self.tree.exists(selected[0]):
            self.tree.selection_set(selected[0])

        total = len(self.library.books)
        avail = sum(b.check_availability() for b in self.library.books)
        self.stats_label.config(
            text=f"{total} books   |   {avail} available   |   {total - avail} borrowed")
        self.set_status(f"Showing {shown} of {total} books")
        self._update_buttons()

    def _update_buttons(self):
        book = self.selected_book()
        if book is None:
            for b in (self.btn_details, self.btn_borrow,
                      self.btn_return, self.btn_remove):
                b.state(["disabled"])
            return
        self.btn_details.state(["!disabled"])
        self.btn_remove.state(["!disabled"])
        can_borrow = book.check_availability() and not isinstance(book, ReferenceBook)
        self.btn_borrow.state(["!disabled"] if can_borrow else ["disabled"])
        self.btn_return.state(["!disabled"] if not book.check_availability()
                              else ["disabled"])

    # ---------- actions ----------
    def open_add(self):
        AddBookDialog(self, self.add_book)

    def add_book(self, book):
        if self.library.find_by_title(book.title):
            messagebox.showinfo("Duplicate", f"'{book.title}' is already in the catalog.")
            return
        self.library.books.append(book)
        self.refresh()
        self.set_status(f"Added '{book.title}'")

    def remove_selected(self):
        book = self.selected_book()
        if not book:
            return
        if messagebox.askyesno("Remove book", f"Remove '{book.title}' from the catalog?"):
            self.library.books.remove(book)
            self.refresh()
            self.set_status(f"Removed '{book.title}'")

    def borrow_selected(self):
        book = self.selected_book()
        if not book:
            return
        if isinstance(book, ReferenceBook):
            messagebox.showinfo("Not allowed", "Reference books are for in-library use only.")
            return
        if not book.check_availability():
            messagebox.showinfo("Unavailable", "This book is already borrowed.")
            return
        book.update_availability(False)
        self.refresh()
        self.set_status(f"Borrowed '{book.title}'")

    def return_selected(self):
        book = self.selected_book()
        if not book:
            return
        if book.check_availability():
            messagebox.showinfo("Not borrowed", "This book was not borrowed.")
            return
        book.update_availability(True)
        self.refresh()
        self.set_status(f"Returned '{book.title}'")

    def show_details(self):
        book = self.selected_book()
        if not book:
            return
        status = "Available" if book.check_availability() else "Borrowed"
        messagebox.showinfo(
            "Book Details",
            f"Title: {book.title}\nAuthor: {book.author}\nGenre: {book.genre}\n"
            f"Details: {extra_info(book)}\nStatus: {status}")


if __name__ == "__main__":
    LibraryApp().mainloop()