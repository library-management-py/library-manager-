import customtkinter as ctk
from tkinter import messagebox
import db_users as db_users


class adminpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Ensure the controller is accessible
        
        # Set frame background color to beige
        self.configure(fg_color="#FCF1D8")
        
        # Title
        label = ctk.CTkLabel(self, text="Admin Page", font=("Arial", 20), text_color="black")
        label.pack(pady=20)

        # Admin Login Section
        admin_username_label = ctk.CTkLabel(self, text="Admin Username:", font=("Arial", 17), text_color="black")
        admin_password_label = ctk.CTkLabel(self, text="Admin Password:", font=("Arial", 17), text_color="black")

        # Transparent entries with black text
        self.admin_username_field = ctk.CTkEntry(self, width=200, font=("Arial", 10), fg_color="transparent", text_color="black")
        self.admin_password_field = ctk.CTkEntry(self, width=200, font=("Arial", 10), show="*", fg_color="transparent", text_color="black")

        # Buttons with black background and white text
        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login"),
            fg_color="black", text_color="white"
        )
        enter_button = ctk.CTkButton(
            self, text="Enter", command=self.on_enter,
            fg_color="black", text_color="white"
        )

        # Layout
        admin_username_label.pack(pady=10)
        self.admin_username_field.pack(pady=5)
        admin_password_label.pack(pady=10)
        self.admin_password_field.pack(pady=5)
        enter_button.pack(pady=20)
        back_button.pack(pady=10)


    def on_enter(self):
        entered_username = self.admin_username_field.get()
        entered_password = self.admin_password_field.get()

        # Query the database for matching credentials
        db_users.cursor.execute("SELECT username, password FROM admins WHERE username = ?", (entered_username,))
        result = db_users.cursor.fetchone()

        if result:
            db_username, db_password = result
            if entered_password == db_password:
                messagebox.showinfo("Success", "Login Successful!")
                self.controller.show_frame("adminmainpage")
            else:
                messagebox.showerror("Error", "Invalid Password!")
        else:
            messagebox.showerror("Error", "Username not found!")
