import customtkinter as ctk

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("log in")

        label = ctk.CTkLabel(self, text= "Welcome, please log in")
        self.enter_button = ctk.CTkButton(self, text="enter")
        self.enter_button.pack(pady=20)

        self.close_button = ctk.CTkButton(self, text="close")
        self.close_button.pack(pady=20)


