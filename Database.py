import sqlite3
from tkinter import messagebox


class Database:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_tables()

    #Create and returns a database connection
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    #Create Books and Members tables if they don't exist
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                availability TEXT NOT NULL
            )
        ''')

        # Create Members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Members (
                membership_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                membership_type TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    #Execute a query with error handling
    def execute_query(self, query, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", f"Duplicate entry: {str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return False

    #Fetch data from database with error handling
    def fetch_query(self, query, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return []