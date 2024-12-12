import customtkinter as ctk
import db_users


class signup(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Title Label
        label = ctk.CTkLabel(self, text="Sign Up", font=("Arial", 24))
        label.pack(pady=20)

        # Username Field
        username_label = ctk.CTkLabel(self, text="Username:", font=("Arial", 14))
        username_label.pack(pady=5)
        self.username_field = ctk.CTkEntry(self, width=200)
        self.username_field.pack(pady=5)

        # Email Field
        email_label = ctk.CTkLabel(self, text="Email:", font=("Arial", 14))
        email_label.pack(pady=5)
        self.email_field = ctk.CTkEntry(self, width=200)
        self.email_field.pack(pady=5)

        # Password Field
        password_label = ctk.CTkLabel(self, text="Password:", font=("Arial", 14))
        password_label.pack(pady=5)
        self.password_field = ctk.CTkEntry(self, width=200, show="*")
        self.password_field.pack(pady=5)

        # Confirm Password Field
        confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:", font=("Arial", 14))
        confirm_password_label.pack(pady=5)
        self.confirm_password_field = ctk.CTkEntry(self, width=200, show="*")
        self.confirm_password_field.pack(pady=5)

        # Enter Button
        enter_button = ctk.CTkButton(
            self, text="Sign Up", command=self.on_enter
        )
        enter_button.pack(pady=10)

        # Back Button
        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login")
        )
        back_button.pack(pady=10)

    def on_enter(self):
        # Get values from the input fields
        username_value = self.username_field.get()
        email_value = self.email_field.get()
        password_value = self.password_field.get()
        confirm_password_value = self.confirm_password_field.get()
        db_users.cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username_value, email_value, password_value)
       )

        db_users.connection.commit()
        
        
            
