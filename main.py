import tkinter as tk
from tkinter import ttk, messagebox
from Books_window import BooksWindow
from Members_window import MembersWindow
from Database import Database


class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book and Member Management System")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # This initializes the database
        self.db = Database()

        #This creates the main interface
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Library Management System",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=30)

        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Manage your library's books and members efficiently",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666"
        )
        subtitle_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=50)

        # Books Management Button
        books_btn = tk.Button(
            button_frame,
            text="📚 Manage Books",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self.open_books_window
        )
        books_btn.grid(row=0, column=0, padx=20, pady=10)

        # Members Management Button
        members_btn = tk.Button(
            button_frame,
            text="👥 Manage Members",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2,
            cursor="hand2",
            command=self.open_members_window
        )
        members_btn.grid(row=1, column=0, padx=20, pady=10)

        # Exit Button
        exit_btn = tk.Button(
            button_frame,
            text="❌ Exit",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=20,
            cursor="hand2",
            command=self.root.quit
        )
        exit_btn.grid(row=2, column=0, padx=20, pady=10)

        # Footer
        footer_label = tk.Label(
            self.root,
            text="SSX361 Project - LBMMS",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#999"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def open_books_window(self):
        books_win = tk.Toplevel(self.root)
        BooksWindow(books_win, self.db)

    def open_members_window(self):
        members_win = tk.Toplevel(self.root)
        MembersWindow(members_win, self.db)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()