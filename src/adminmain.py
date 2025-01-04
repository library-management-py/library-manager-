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


        # Save the controller
               # Save the controller
        self.controller = controller

        # Set background color to beige
        self.configure(fg_color="#FCF1D8")  # Beige background

        # Title Label
        title_label = ctk.CTkLabel(
            self, text="Admin Main Page", font=("Arial", 24, "bold"), text_color="black"
        )
        title_label.pack(pady=20)

        # Back to Login Button
        back_button = ctk.CTkButton(
            self,
            text="Back to Log In",
            command=lambda: self.controller.show_frame("Login"),
            fg_color="black",  # Dark button
            text_color="white",  # White text
            font=("Arial", 14),
            corner_radius=8,
            width=200,
        )
        back_button.pack(pady=20)

        # Book Management Section
        book_label = ctk.CTkLabel(
            self, text="Manage Books", font=("Arial", 18, "bold"), text_color="black"
        )
        book_label.pack(pady=20)

        # Add Book Section
        self.book_title_field = ctk.CTkEntry(
            self, placeholder_text="Book Title", width=250, fg_color="white", text_color="black", corner_radius=8
        )
        self.book_title_field.pack(pady=5)

        self.book_author_field = ctk.CTkEntry(
            self, placeholder_text="Author", width=250, fg_color="white", text_color="black", corner_radius=8
        )
        self.book_author_field.pack(pady=5)

        self.book_year_field = ctk.CTkEntry(
            self, placeholder_text="Year of Publication", width=250, fg_color="white", text_color="black", corner_radius=8
        )
        self.book_year_field.pack(pady=5)

        add_book_button = ctk.CTkButton(
            self,
            text="Add Book",
            command=self.add_book,
            fg_color="black",  # Dark button
            text_color="white",  # White text
            font=("Arial", 14),
            corner_radius=8,
            width=200,
        )
        add_book_button.pack(pady=10)

        # Delete Book Section
        self.delete_book_field = ctk.CTkEntry(
            self, placeholder_text="Book Title to Delete", width=250, fg_color="white", text_color="black", corner_radius=8
        )
        self.delete_book_field.pack(pady=5)

        delete_book_button = ctk.CTkButton(
            self,
            text="Delete Book",
            command=self.delete_book,
            fg_color="black",  # Dark button
            text_color="white",  # White text
            font=("Arial", 14),
            corner_radius=8,
            width=200,
        )
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