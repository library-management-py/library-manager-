import customtkinter as ctk 
import db_users



class bookpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side ="left",fill ="both", expand =True, padx=10 , pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        back_button = ctk.CTkButton(
            self.right_frame, text="back to main page", command=lambda: controller.show_frame("mainpage")
        )


        labe_description = ctk.CTkLabel(self,text="description")
        labe_description.pack(pady=20)
        back_button.pack(pady =20)

   
 





