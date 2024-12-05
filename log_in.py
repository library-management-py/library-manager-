import customtkinter as ctk

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("log in")

        label = ctk.CTkLabel(self, text= "Welcome, please log in", font=("Arial",30 ))
        

        username_field = ctk.CTkEntry(self, width=200, font=("Arial", 10))
        password_field = ctk.CTkEntry(self, width=200, font=("Arial", 10))

        username_label = ctk.CTkLabel(self, text= "username: ", font=("Arial", 17))
        
        password_label = ctk.CTkLabel(self, text= "password: ", font=("Arial", 17))
       

        

        self.enter_button = ctk.CTkButton(self, text="enter")
        self.admin_page_log_in = ctk.CTkButton(self, text="admin page")

        self.close_button = ctk.CTkButton(self, text="close")
        
        label.pack(pady=20)
        username_label.pack(pady=20)
        username_field.pack(pady=10)
        password_label.pack(pady=20)
        password_field.pack(pady=10)
        self.enter_button.pack(pady=20)
        self.close_button.pack(pady=20)
        self.admin_page_log_in.pack(pady =20)
