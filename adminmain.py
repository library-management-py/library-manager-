import customtkinter as ctk


class adminmainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Admin main page", font=("Arial", 20))

        label.pack(pady =20)
        back_button = ctk.CTkButton(
            self, text="Back to admin log in", command=lambda: controller.show_frame("adminpage")
        )

        back_button.pack(pady =10)