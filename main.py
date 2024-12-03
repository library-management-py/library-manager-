import customtkinter as ctk
from log_in import LoginPage
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = LoginPage() 
app.geometry("800x600")


app.mainloop()
