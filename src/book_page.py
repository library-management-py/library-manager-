import customtkinter as ctk 


class bookpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        back_button = ctk.CTkButton(
            self, text="back to main page", command=lambda: controller.show_frame("mainpage")
        )
        back_button.pack(pady =20)