import customtkinter as ctk
import db_users as db_users
from tkinter import messagebox

class signup(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Set the background color of the main frame to beige
        self.configure(bg_color="#FCF1D8", fg_color="#FCF1D8")

        # Title Label
        label = ctk.CTkLabel(self, text="Sign Up", font=("Arial", 24), text_color="black")
        label.pack(pady=20)

        # Username Field
        username_label = ctk.CTkLabel(self, text="Username:", font=("Arial", 14), text_color="black")
        username_label.pack(pady=5)
        self.username_field = ctk.CTkEntry(self, width=200, fg_color="transparent", text_color="black")
        self.username_field.pack(pady=5)

        # Email Field
        email_label = ctk.CTkLabel(self, text="Email:", font=("Arial", 14), text_color="black")
        email_label.pack(pady=5)
        self.email_field = ctk.CTkEntry(self, width=200, fg_color="transparent", text_color="black")
        self.email_field.pack(pady=5)

        # Password Field
        password_label = ctk.CTkLabel(self, text="Password:", font=("Arial", 14), text_color="black")
        password_label.pack(pady=5)
        self.password_field = ctk.CTkEntry(self, width=200, show="*", fg_color="transparent", text_color="black")
        self.password_field.pack(pady=5)

        # Confirm Password Field
        confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:", font=("Arial", 14), text_color="black")
        confirm_password_label.pack(pady=5)
        self.confirm_password_field = ctk.CTkEntry(self, width=200, show="*", fg_color="transparent", text_color="black")
        self.confirm_password_field.pack(pady=5)

        # Enter Button
        enter_button = ctk.CTkButton(
            self, text="Sign Up", command=self.on_enter, fg_color="black", text_color="white", width=150
        )
        enter_button.pack(pady=10)

        # Back Button
        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login"), fg_color="black", text_color="white", width=150
        )
        back_button.pack(pady=10)
    def on_enter(self):
        # Get values from the input fields
        username_value = self.username_field.get().strip()
        email_value = self.email_field.get().strip()
        password_value = self.password_field.get().strip()
        confirm_password_value = self.confirm_password_field.get().strip()

        # Check for empty fields
        if not username_value or not email_value or not password_value or not confirm_password_value:
            messagebox.showwarning("Input Error", "All fields are required. Please fill out all fields.")
            return

        # Check if email ends with '@gmail.com'
        if not email_value.endswith("@gmail.com"):
            messagebox.showwarning("Input Error", "Email must end with '@gmail.com'.")
            return

        # Check if passwords match
        if password_value != confirm_password_value:
            messagebox.showwarning("Input Error", "Passwords do not match. Please try again.")
            return

        # Insert into the database
        db_users.cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username_value, email_value, password_value)
        )
        db_users.connection.commit()

        # Show success message
        messagebox.showinfo("Success", "Account created successfully!")

        # Clear the input fields after successful signup
        self.username_field.delete(0, "end")
        self.email_field.delete(0, "end")
        self.password_field.delete(0, "end")
        self.confirm_password_field.delete(0, "end")

        # Optionally navigate to the login page
        self.controller.show_frame("Login")
