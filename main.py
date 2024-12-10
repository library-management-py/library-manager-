import customtkinter as ctk
import admin_login
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("800x600")
        self.title("Multi-Page App")


        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Add all pages to the app
        for F in (Login, admin_login.adminpage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the main page initially
        self.show_frame("Login")

    def show_frame(self, page_name):
        """Bring the specified frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

class Login(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        self.username_field = ctk.CTkEntry(self, width=200, font=("Arial", 10))
        self.password_field = ctk.CTkEntry(self, width=200, font=("Arial", 10), show = "*")

        self.label = ctk.CTkLabel(self, text= "Welcome, please log in", font=("Arial",30 ))
        self.username_label = ctk.CTkLabel(self, text= "username: ", font=("Arial", 17))
        self.password_label = ctk.CTkLabel(self, text= "password: ", font=("Arial", 17))   

        self.enter_button = ctk.CTkButton(self, text="enter", command= self.on_enter)
        self.admin_page_log_in = ctk.CTkButton(self, text="admin page", command= lambda: controller.show_frame("adminpage"))
        self.close_button = ctk.CTkButton(self, text="close", command=self.on_close)
        
        self.label.pack(pady=20)
        self.username_label.pack(pady=20)
        self.username_field.pack(pady=10)
        self.password_label.pack(pady=20)
        self.password_field.pack(pady=10)
        self.enter_button.pack(pady=20)
        self.close_button.pack(pady=20)
        self.admin_page_log_in.pack(pady =20)


    def on_enter(self):
        username_value = self.username_field.get()
        password_value = self.password_field.get()
        if (len(username_value) >= 8 or len(password_value) >= 8):
            messagebox.showwarning("fLUDGE you")
        else:
            print(f"username {username_value}")
            print(f"username {username_value}")
    def on_close(self):
        exit(0)


# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()

