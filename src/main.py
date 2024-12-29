import customtkinter as ctk
from tkinter import messagebox

import admin_login as admin_login
import adminmain as adminmain
import signup as signup
import book_page as bookpage
import mainpage as mainpage
import db_users as db_users
import profile_page




class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("1980x1080")
        self.title("Library management system")

        self.title_transfer = []

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, admin_login.adminpage, adminmain.adminmainpage,mainpage.mainpage, signup.signup,bookpage.bookpage,profile_page.profilepage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if hasattr(frame, "on_show"):
            frame.on_show()
        
        frame.tkraise()

class Login(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.configure(fg_color="#FCF1D8") 
        self.controller = controller

        self.username_field = ctk.CTkEntry(self, width=200, font=("Arial", 10),fg_color="transparent")
        self.password_field = ctk.CTkEntry(self, width=200, font=("Arial", 10), show = "*",fg_color="transparent")

        self.label = ctk.CTkLabel(self, text= "log in", font=("Arial",30 ),text_color="black")
        self.username_label = ctk.CTkLabel(self, text= "username: ", font=("Arial", 17),text_color="black")
        self.password_label = ctk.CTkLabel(self, text= "password: ", font=("Arial", 17),text_color="black")   

        self.enter_button = ctk.CTkButton(self, text="enter", command= self.on_enter,fg_color="black", text_color="white")
        self.admin_page_log_in = ctk.CTkButton(self, text="admin page", command= lambda: controller.show_frame("adminpage"),text_color="white",fg_color="black")
        self.close_button = ctk.CTkButton(self, text="close", command=self.on_close,fg_color="black", text_color="white")
        self.signup_button = ctk.CTkButton(self,text="sign up", command= lambda: controller.show_frame("signup"),fg_color="black", text_color="white")
        

        self.label.pack(pady=20)
        self.username_label.pack(pady=20)
        self.username_field.pack(pady=10)
        self.password_label.pack(pady=20)
        self.password_field.pack(pady=10)
        self.enter_button.pack(pady=20)
        self.close_button.pack(pady=20)
        self.admin_page_log_in.pack(pady =20)
        self.signup_button.pack(pady=20)



    def on_enter(self):
        username_value = self.username_field.get()
        password_value = self.password_field.get()
         

        rows = db_users.cursor.execute("SELECT username, password FROM users").fetchall()
        authenticate = False
        for row in rows:
            if row[0] == username_value and row[1] == password_value:
                authenticate = True
                break
        if authenticate:
            self.controller.show_frame("mainpage")
        else:
            messagebox.showwarning("failed")


    def on_close(self):
        exit(0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
