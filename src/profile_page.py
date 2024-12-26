import customtkinter as ctk
import db_users

class profilepage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")  # Add background color for better visibility

        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="My Profile", 
            font=("Arial", 24, "bold"),
            text_color="black"
        )
        title_label.pack(pady=30)

        # Settings Section
        self.settings_var = ctk.StringVar(value="hide")
        self.settings_button = ctk.CTkSegmentedButton(
            self,
            values=["hide", "show settings"],
            command=self.toggle_settings,
            variable=self.settings_var,
            fg_color="black",
            selected_color="gray",
            unselected_color="black",
            text_color="white"
        )
        self.settings_button.pack(pady=20)

        # Settings Frame (initially hidden)
        self.settings_frame = ctk.CTkFrame(self, fg_color="#f0f0f0")
        
        # Email Settings
        self.email_label = ctk.CTkLabel(
            self.settings_frame,
            text="New Email:",
            font=("Arial", 16),
            text_color="black"
        )
        self.email_entry = ctk.CTkEntry(
            self.settings_frame,
            font=("Arial", 14),
            width=200
        )
        
        # Password Settings
        self.password_label = ctk.CTkLabel(
            self.settings_frame,
            text="New Password:",
            font=("Arial", 16),
            text_color="black"
        )
        self.password_entry = ctk.CTkEntry(
            self.settings_frame,
            font=("Arial", 14),
            width=200,
            show="*"
        )
        
        # Update Button
        self.update_button = ctk.CTkButton(
            self.settings_frame,
            text="Update Profile",
            command=self.update_profile,
            font=("Arial", 14),
            fg_color="black",
            text_color="white"
        )

        # Back button
        back_button = ctk.CTkButton(
            self, 
            text="Back to Main Page", 
            command=lambda: controller.show_frame("mainpage"),
            font=("Arial", 14),
            fg_color="black",
            text_color="white"
        )
        back_button.pack(pady=20)

        # Create a frame for borrowed books section
        self.borrowed_frame = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.borrowed_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Borrowed Books Section Header
        self.borrowed_books_label = ctk.CTkLabel(
            self.borrowed_frame,
            text="📚 Currently Borrowed Books:",
            font=("Arial", 18, "bold"),
            text_color="black"
        )
        self.borrowed_books_label.pack(pady=(20, 10), padx=20, anchor="w")

        # Borrowed Books List
        self.borrowed_books_text = ctk.CTkLabel(
            self.borrowed_frame,
            text="No books borrowed.",
            font=("Arial", 16),
            text_color="black",
            justify="left",
            wraplength=400
        )
        self.borrowed_books_text.pack(pady=(0, 20), padx=40, anchor="w")

    def toggle_settings(self, value):
        if value == "show settings":
            self.settings_frame.pack(pady=20, padx=40, fill="x")
            self.email_label.pack(pady=5)
            self.email_entry.pack(pady=5)
            self.password_label.pack(pady=5)
            self.password_entry.pack(pady=5)
            self.update_button.pack(pady=20)
        else:
            self.settings_frame.pack_forget()

    def update_profile(self):
        new_email = self.email_entry.get()
        new_password = self.password_entry.get()
        current_user = self.controller.logged_in_user

        if new_email or new_password:
            update_query = "UPDATE users SET"
            update_values = []
            
            if new_email:
                update_query += " email = ?"
                update_values.append(new_email)
            
            if new_password:
                if new_email:  # Add comma if both fields are being updated
                    update_query += ","
                update_query += " password = ?"
                update_values.append(new_password)
            
            update_query += " WHERE username = ?"
            update_values.append(current_user)

            db_users.cursor.execute(update_query, tuple(update_values))
            db_users.connection.commit()

            # Clear the entries after successful update
            self.email_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            
            # Hide settings panel
            self.settings_var.set("hide")
            self.toggle_settings("hide")

    def update_borrowed_books(self, borrowed_books_list):
        self.borrowed_books_text.configure(text=borrowed_books_list)