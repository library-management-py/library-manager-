import customtkinter as ctk
from tkinter import messagebox
import db_users


class adminpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="Admin Page", font=("Arial", 20))
        
        

        admin_username_label = ctk.CTkLabel(self, text= "admin username: ", font=("Arial", 17))
        admin_password_label = ctk.CTkLabel(self, text= "admin password: ", font=("Arial", 17))   

        self.admin_username_field = ctk.CTkEntry(self, width=200, font=("Arial", 10))
        self.admin_password_field = ctk.CTkEntry(self, width=200, font=("Arial", 10))

        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login")
        )
        enter_button = ctk.CTkButton(
            self, text="enter", command= self.on_enter
        )


        label.pack(pady=20)
        admin_username_label.pack(pady=10)
        self.admin_username_field.pack(pady=5)
        admin_password_label.pack(pady=10)
        self.admin_password_field.pack(pady=5)
        back_button.pack(pady=20)
        enter_button.pack(pady=20)






    def on_enter(self):
        username_value = self.admin_username_field.get()
        password_value = self.admin_password_field.get()
        db_users.cursor.execute("SELECT username FROM admins")
        rows_username = db_users.cursor.fetchall()
        db_users.cursor.execute("SELECT password FROM admins")
        rows_passwords = db_users.cursor.fetchall()
        authenticate = True

        for element in rows_username:
            if username_value != element[0]:
                authenticate = False
                break
        for element_2 in rows_passwords:
            if password_value != element_2[0]:
                authenticate = False
                break

        if authenticate == True:
            self.controller.show_frame("adminmainpage")
                
        else:
             print("username or password don't exist in database")


            
                           
        
        

