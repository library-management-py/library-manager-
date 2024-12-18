import customtkinter as ctk


class profilepage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="profile page", font=("Arial", 20))

        label.pack(pady =20)
        back_button = ctk.CTkButton(
            self, text="back to main page", command=lambda: controller.show_frame("mainpage")
        )

        back_button.pack(pady = 10)
