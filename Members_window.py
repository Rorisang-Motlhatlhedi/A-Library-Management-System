import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

from Memebers import MembersCRUD


class MembersWindow:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Members Management")
        self.master.geometry("750x550")
        #self.master.configure(bg="#f5f5f5")

        self.db = database
        self.members_crud = MembersCRUD(database)

        self.create()
        self.load_members()

    def create(self):

        container = LabelFrame(self.master, text="Member Management", font=("Arial", 20))
        container.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        # MEMBERSHIP ID
        self.membership_text = StringVar()
        membership_label = Label(container, text="Membership ID:", font=("Arial", 12))
        membership_label.grid(row=0, column=0, pady=20)
        self.membership_entry = Entry(container, textvariable=self.membership_text)
        self.membership_entry.grid(row=0, column=1)

        # NAME
        self.name_text = StringVar()
        name_label = Label(container, text="Name:", font=("Arial", 12))
        name_label.grid(row=0, column=2)
        self.name_entry = Entry(container, textvariable=self.name_text)
        self.name_entry.grid(row=0, column=3)

        # CONTACT INFO
        self.contact_text = StringVar()
        contact_label = Label(container, text="Contact Info:", font=("Arial", 12))
        contact_label.grid(row=1, column=0, pady=20)
        self.contact_entry = Entry(container, textvariable=self.contact_text)
        self.contact_entry.grid(row=1, column=1)

        # Member type label
        member_label = Label(container, text="Member Type:", font=("Arial", 12))
        member_label.grid(row=1, column=2)

        # Member type menu
        self.type_text = StringVar()
        self.type_text.set("Select option")
        self.member_type = ["Student", "Senior", "Staff"]
        self.member_options = OptionMenu(container, self.type_text, *self.member_type)
        self.member_options.grid(row=1, column=3)

        # add button
        add_btn = Button(container, text="Add member", width=15, bg="blue", fg="white", command=self.add_member)
        add_btn.grid(row=2, column=0, pady=10, padx=25)

        # update
        update_btn = Button(container, text="Update member", width=15, bg="darkgreen", fg="white", command=self.update_member)
        update_btn.grid(row=2, column=1, pady=10, padx=25)

        # delete
        delete_btn = Button(container, text="Delete member", width=15, bg="red", fg="white", command=self.delete_member)
        delete_btn.grid(row=2, column=2, pady=10, padx=25)

        # clear
        clear_btn = Button(container, text="Clear fields", width=15, bg="grey", fg="white", command=self.clear_fields)
        clear_btn.grid(row=2, column=3, pady=10, padx=25)

        # SEARCH SECTION
        search_label = Label(self.master, text="Search:", font=("Arial", 12))
        search_label.grid(row=3, column=0, padx=10, pady=20, sticky="w")

        self.search = StringVar()
        self.search_entry = Entry(self.master, textvariable=self.search, width=40)
        self.search_entry.grid(row=3, column=1, padx= 10, pady=20, sticky="w")

        search_btn = Button(self.master, text="Search", width=12, bg="lightblue", fg="black", command=self.search_members)
        search_btn.grid(row=3, column=2, padx=10, pady=20, sticky="w")

        display_all = Button(self.master, text="Display all", width=12, bg="lightgreen", fg="black", command=self.load_members)
        display_all.grid(row=3, column=3, padx= 10, pady=20, sticky="w")

        # List
        self.member_list = Treeview(self.master, columns=("Id", "Name", "Contact Info", "Member Type"),
                                    show="headings")
        self.member_list.heading("Id", text="Id")
        self.member_list.heading("Name", text="Name")
        self.member_list.heading("Contact Info", text="Contact Info")
        self.member_list.heading("Member Type", text="Member Type")

        # editing column widths
        self.member_list.column("Id", width=50, anchor="center")
        self.member_list.column("Name", width=150, anchor="w")
        self.member_list.column("Contact Info", width=150, anchor="w")
        self.member_list.column("Member Type", width=150, anchor="center")
        self.member_list.grid(row=4, column=0, rowspan=6, columnspan=3, padx=10, sticky="w")

        # scrollbar
        scrollbar = Scrollbar(self.master)
        scrollbar.grid(row=4, column=3)

        # bind scrollbar and list box
        self.member_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.member_list.yview)

        # bind on select
        self.member_list.bind('<<TreeviewSelect>>', self.on_select)




    #Load all members into the treeview
    def load_members(self):

        for item in self.member_list.get_children():
            self.member_list.delete(item)

        members = self.members_crud.read_all_members()
        for member in members:
            self.member_list.insert("", "end", values=member)


    def add_member(self):
        try:
            member_id = int(self.membership_text.get())
            if self.members_crud.create_member(
                self.name_text.get(),
                member_id,
                self.contact_text.get(),
                self.type_text.get()
            ):
                self.load_members()
                self.clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Invalid Id")

    def on_select(self, event):

        selected_item_id = self.member_list.focus()
        self.selected_item = self.member_list.item(selected_item_id)['values']

        if self.selected_item:
            self.membership_entry.delete(0, END)
            self.membership_entry.insert(0, self.selected_item[0])
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, self.selected_item[1])
            self.contact_entry.delete(0, END)
            self.contact_entry.insert(0, self.selected_item[2])
            self.type_text.set(self.selected_item[3])

    def update_member(self):

        if self.members_crud.update_member(
                self.membership_text.get(),
                self.name_text.get(),
                self.contact_text.get(),
                self.type_text.get()
        ):
            self.load_members()
            self.clear_fields()



    def delete_member(self):

        if self.members_crud.delete_member(self.membership_text.get()):
            self.load_members()
            self.clear_fields()


    def search_members(self):

        for item in self.member_list.get_children():
            self.member_list.delete(item)

        search_term = self.search.get()
        members = self.members_crud.search_members(search_term)
        for member in members:
            self.member_list.insert("", "end", values=member)

    def clear_fields(self):

        self.membership_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.type_text.set("SELECT OPTION")
        #self.search_entry.delete(0, tk.END)


