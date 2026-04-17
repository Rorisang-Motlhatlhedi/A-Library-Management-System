import tkinter as tk
from tkinter import ttk
from Books import BooksCRUD


class BooksWindow:
    def __init__(self, window, database):
        self.window = window
        self.window.title("Books Management")
        self.window.geometry("900x600")
        self.window.configure(bg="#f5f5f5")

        self.db = database
        self.books_crud = BooksCRUD(database)

        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="Books Management",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5"
        )
        title_label.pack(pady=10)

        # Form Frame
        form_frame = tk.LabelFrame(
            self.window,
            text="Book Information",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            padx=20,
            pady=10
        )
        form_frame.pack(padx=20, pady=10, fill="x")

        # ISBN
        tk.Label(form_frame, text="ISBN:", bg="#f5f5f5", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.isbn_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.isbn_entry.grid(row=0, column=1, padx=10, pady=5)

        # Title
        tk.Label(form_frame, text="Title:", bg="#f5f5f5", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.title_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)

        # Author
        tk.Label(form_frame, text="Author:", bg="#f5f5f5", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.author_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)

        # Genre
        tk.Label(form_frame, text="Genre:", bg="#f5f5f5", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.genre_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.genre_entry.grid(row=3, column=1, padx=10, pady=5)

        # Availability
        tk.Label(form_frame, text="Availability:", bg="#f5f5f5", font=("Arial", 10)).grid(row=4, column=0, sticky="w",
                                                                                          pady=5)
        self.availability_var = tk.StringVar(value="Available")
        availability_combo = ttk.Combobox(
            form_frame,
            textvariable=self.availability_var,
            values=["Available", "Checked Out"],
            state="readonly",
            width=28,
            font=("Arial", 10)
        )
        availability_combo.grid(row=4, column=1, padx=10, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="#f5f5f5")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Add Book", bg="#4CAF50", fg="white", width=12,
                  command=self.add_book, cursor="hand2").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Book", bg="#FF9800", fg="white", width=12,
                  command=self.update_book, cursor="hand2").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Book", bg="#f44336", fg="white", width=12,
                  command=self.delete_book, cursor="hand2").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear Fields", bg="#9E9E9E", fg="white", width=12,
                  command=self.clear_fields, cursor="hand2").grid(row=0, column=3, padx=5)

        # Search Frame
        search_frame = tk.Frame(self.window, bg="#f5f5f5")
        search_frame.pack(padx=20, pady=5, fill="x")

        tk.Label(search_frame, text="Search:", bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=40, font=("Arial", 10))
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", bg="#2196F3", fg="white",
                  command=self.search_books, cursor="hand2").pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", bg="#607D8B", fg="white",
                  command=self.load_books, cursor="hand2").pack(side="left", padx=5)

        # Treeview Frame
        tree_frame = tk.Frame(self.window, bg="#f5f5f5")
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ISBN", "Title", "Author", "Genre", "Availability"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        # Define columns
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Availability", text="Availability")

        self.tree.column("ISBN", width=120)
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Genre", width=120)
        self.tree.column("Availability", width=120)

        self.tree.pack(fill="both", expand=True)

        # Bind selection event
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    #Load all the books into a treeview
    def load_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.books_crud.read_all_books()
        for book in books:
            self.tree.insert("", "end", values=book)

    def add_book(self):

        if self.books_crud.create_book(
                self.title_entry.get(),
                self.author_entry.get(),
                self.isbn_entry.get(),
                self.genre_entry.get(),
                self.availability_var.get()
        ):
            self.load_books()
            self.clear_fields()

    def update_book(self):

        if self.books_crud.update_book(
                self.isbn_entry.get(),
                self.title_entry.get(),
                self.author_entry.get(),
                self.genre_entry.get(),
                self.availability_var.get()
        ):
            self.load_books()
            self.clear_fields()

    def delete_book(self):

        if self.books_crud.delete_book(self.isbn_entry.get()):
            self.load_books()
            self.clear_fields()

    def search_books(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_entry.get()
        books = self.books_crud.search_books(search_term)
        for book in books:
            self.tree.insert("", "end", values=book)

    #clear all the inputs fields
    def clear_fields(self):

        self.isbn_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.availability_var.set("Available")
        self.search_entry.delete(0, tk.END)

    #Fill fields when a record is selected
    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.clear_fields()
            self.isbn_entry.insert(0, values[0])
            self.title_entry.insert(0, values[1])
            self.author_entry.insert(0, values[2])
            self.genre_entry.insert(0, values[3])
            self.availability_var.set(values[4])