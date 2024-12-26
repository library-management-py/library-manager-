import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
import json 
import requests
from tkinter import messagebox
import db_users

class adminmainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        label = ctk.CTkLabel(self, text="Admin main page", font=("Arial", 20))

        label.pack(pady =20)
        main_page_button = ctk.CTkButton(
            self, text="back to log in", command=lambda: self.controller.show_frame("Login")
        )
        main_page_button.pack(pady=20)

    # Book Management Section
        book_label = ctk.CTkLabel(self, text="Manage Books", font=("Arial", 17))
        book_label.pack(pady=20)

        self.book_title_field = ctk.CTkEntry(self, placeholder_text="Book Title")
        self.book_title_field.pack(pady=5)

        self.book_author_field = ctk.CTkEntry(self, placeholder_text="Author")
        self.book_author_field.pack(pady=5)

        self.book_year_field = ctk.CTkEntry(self, placeholder_text="Year of Publication")
        self.book_year_field.pack(pady=5)

        add_book_button = ctk.CTkButton(self, text="Add Book", command=self.add_book)
        add_book_button.pack(pady=10)

        self.delete_book_field = ctk.CTkEntry(self, placeholder_text="Book Title to Delete")
        self.delete_book_field.pack(pady=5)

        delete_book_button = ctk.CTkButton(self, text="Delete Book", command=self.delete_book)
        delete_book_button.pack(pady=10)

    def add_book(self):
        title = self.book_title_field.get()
        author = self.book_author_field.get()
        year = self.book_year_field.get()
        if not title or not author or not year:
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            db_users.cursor.execute(
                "INSERT INTO books (title, author, published_date) VALUES (?, ?, ?)",
                (title, author, year)
            )
            db_users.connection.commit()
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.book_title_field.delete(0, "end")
            self.book_author_field.delete(0, "end")
            self.book_year_field.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def delete_book(self):
        title = self.delete_book_field.get()

        if not title:
            messagebox.showerror("Error", "Book title is required to delete a book!")
            return

        try:
            db_users.cursor.execute("DELETE FROM books WHERE title = ?", (title,))
            db_users.connection.commit()
            if db_users.cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Book '{title}' deleted successfully!")
            else:
                messagebox.showinfo("Info", f"No book found with title '{title}'")
            self.delete_book_field.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {e}")  