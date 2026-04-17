from tkinter import messagebox


class MembersCRUD:
    def __init__(self, database):
        self.db = database

    def create_member(self, name, membership_id, contact, membership_type):
        """Insert a new member record into the database"""
        # Validation
        if not all([name, membership_id, contact, membership_type]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False

        try:
            membership_id_converted = int(membership_id)
            query = '''
                INSERT INTO Members (membership_id, name, contact, membership_type)
                VALUES (?, ?, ?, ?)
            '''
            success = self.db.execute_query(query, (membership_id_converted, name, contact, membership_type))

            if success:
                messagebox.showinfo("Success", "Member added successfully!")
            return success

        except ValueError as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")
            return False

    def read_all_members(self):
        """Retrieve all member records from the database"""
        query = "SELECT membership_id, name, contact, membership_type FROM Members"
        return self.db.fetch_query(query)

    def read_member_by_id(self, membership_id):
        """Retrieve a specific member by Membership ID"""
        query = "SELECT membership_id, name, contact, membership_type FROM Members WHERE membership_id = ?"
        results = self.db.fetch_query(query, (membership_id,))
        return results[0] if results else None

    def update_member(self, membership_id, name, contact, membership_type):
        """Modify an existing member record"""
        # Validation
        if not all([name, membership_id, contact, membership_type]):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False
        try:
            membership_id_converted = int(membership_id)
            # Check if member exists
            if not self.read_member_by_id(membership_id_converted):
                messagebox.showwarning("Not Found", "Member with this ID does not exist!")
                return False

            query = '''
                UPDATE Members
                SET name = ?, contact = ?, membership_type = ?
                WHERE membership_id = ?
            '''
            success = self.db.execute_query(query, (name, contact, membership_type, membership_id_converted))

            if success:
                messagebox.showinfo("Success", "Member updated successfully!")
            return success
        except ValueError as e:
            messagebox.showwarning("Error", f"An error occurred!: {e}")
            return False

    def delete_member(self, membership_id):
        """Remove a member record from the database"""
        if not membership_id:
            messagebox.showwarning("Validation Error", "Membership ID is required!")
            return False

        try:
            membership_id_converted = int(membership_id)
            # Check if member exists
            if not self.read_member_by_id(membership_id_converted):
                messagebox.showwarning("Not Found", "Member with this ID does not exist!")
                return False

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete",
                                          f"Are you sure you want to delete member with ID: {membership_id_converted}?")
            if not confirm:
                return False

            query = "DELETE FROM Members WHERE membership_id = ?"
            success = self.db.execute_query(query, (membership_id_converted,))

            if success:
                messagebox.showinfo("Success", "Member deleted successfully!")
            return success
        except ValueError as e:
            messagebox.showwarning("Error", f"An error occurred!: {e}")

    #Search members by name, membership ID, or contact
    def search_members(self, search_term):
        query = '''
            SELECT membership_id, name, contact, membership_type FROM Members
            WHERE name LIKE ? OR membership_id LIKE ? OR contact LIKE ?
        '''
        search_pattern = f"%{search_term}%"
        return self.db.fetch_query(query, (search_pattern, search_pattern, search_pattern))