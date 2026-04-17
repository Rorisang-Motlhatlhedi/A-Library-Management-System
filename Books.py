from tkinter import messagebox


class BooksCRUD:
    def __init__(self, database):
        self.db = database

#Insert a new book record into the database
    def create_book(self, title, author, isbn, genre, availability):

        # Validationn
        if not all([title, author, isbn, genre, availability]):
            messagebox.showwarning("Validation Error", "All fields are required.")
            return False

        if not isbn.strip():
            messagebox.showwarning("Validation Error", "ISBN cannot be empty.")
            return False

        query = '''
            INSERT INTO Books (isbn, title, author, genre, availability)
            VALUES (?, ?, ?, ?, ?)
        '''
        success = self.db.execute_query(query, (isbn, title, author, genre, availability))

        if success:
            messagebox.showinfo("Success", "Book was successfully added.")
        return success

#Retrieve all book records from the database
    def read_all_books(self):
        query = "SELECT isbn, title, author, genre, availability FROM Books"
        return self.db.fetch_query(query)

#Retrive a specifc book by the ISBN
    def read_book_by_isbn(self, isbn):
        query = "SELECT isbn, title, author, genre, availability FROM Books WHERE isbn = ?"
        results = self.db.fetch_query(query, (isbn,))
        return results[0] if results else None

#Makes changes to an existing book record
    def update_book(self, isbn, title, author, genre, availability):
        # Validation
        if not all([title, author, isbn, genre, availability]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False

        # Check if book exists
        if not self.read_book_by_isbn(isbn):
            messagebox.showwarning("Not Found", "Book with this ISBN does not exist!")
            return False

        query = '''
            UPDATE Books
            SET title = ?, author = ?, genre = ?, availability = ?
            WHERE isbn = ?
        '''
        success = self.db.execute_query(query, (title, author, genre, availability, isbn))

        if success:
            messagebox.showinfo("Success", "Book updated successfully!")
        return success

#Deletes a book record from the database
    def delete_book(self, isbn):
        if not isbn:
            messagebox.showwarning("Validation Error", "ISBN is required")
            return False

        # Check if book exists
        if not self.read_book_by_isbn(isbn):
            messagebox.showwarning("Not Found", "Book with this ISBN does not exist")
            return False

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the book with ISBN: {isbn}?")
        if not confirm:
            return False

        query = "DELETE FROM Books WHERE isbn = ?"
        success = self.db.execute_query(query, (isbn,))

        if success:
            messagebox.showinfo("Success", "Book deleted successfully.")
        return success

#Searches books by the title, author, genre and availability
    def search_books(self, search_term):
        query = '''
            SELECT isbn, title, author, genre, availability FROM Books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
        '''
        search_pattern = f"%{search_term}%"
        return self.db.fetch_query(query, (search_pattern, search_pattern, search_pattern, search_pattern))