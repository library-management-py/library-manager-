import customtkinter as ctk
import os
from PIL import Image

class bookpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 

        # Left frame
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Right frame
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Back button
        back_button = ctk.CTkButton(
            self.right_frame, text="Back to Main Page", command=lambda: controller.show_frame("mainpage")
        )
        back_button.pack(pady=20)

        # Label for displaying titles
        self.title_label = ctk.CTkLabel(self.right_frame, text="Title List", font=("Arial", 16))
        self.title_label.pack(pady=20)

    def on_show(self):
        # Get the updated title_transfer list from the controller
        titles = self.controller.title_transfer
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"


        self.description = ctk.CTkLabel(self.right_frame, text= "description description description description description description description description ")
        self.description.pack(pady=10)


        for file_name in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, file_name)
            title = os.path.splitext(file_name)[0].replace("_", " ")
            if os.path.isfile(file_path) and file_name.endswith(('.jpg', '.png', '.jpeg')):
                if title in titles:
                    img = Image.open(file_path).resize((250, 350))
                    photo = ctk.CTkImage(light_image=img, size=(250, 350))
                    # Display the image in the grid
                    img_label = ctk.CTkLabel(self.left_frame, image=photo)
                    img_label.image = photo  # Keep a reference to avoid garbage collection
                    img_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Print the list for debugging
        print("Title Transfer List:", titles)
        
        # Update the label text with the titles
        self.title_label.configure(text="\n".join(titles))
        self.controller.title_transfer.clear()
