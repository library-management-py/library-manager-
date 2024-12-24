import customtkinter as ctk
import os
from PIL import Image
import db_users
class bookpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="beige")
        # Configure layout
        self.grid_columnconfigure(0, weight=3)  # Left frame (Image)
        self.grid_columnconfigure(1, weight=2)  # Right frame (Description)
        self.grid_rowconfigure(0, weight=1)

        # Left frame for book cover
        self.left_frame = ctk.CTkFrame(self, fg_color="beige")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Right frame for book details
        self.right_frame = ctk.CTkFrame(self, fg_color="beige")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # Back button
        self.back_button = ctk.CTkButton(
            self.right_frame,
            text="Back to Main Page",
            command=lambda: controller.show_frame("mainpage"),
            font=("Arial", 14),
            fg_color="black",
            text_color="white",
        )
        self.back_button.pack(anchor="n", pady=20)

        # Label for displaying titles
        self.title_label = ctk.CTkLabel(self.right_frame, text="Title List", font=("Arial", 24), text_color="black")
        self.title_label.pack(pady=20)

    def on_show(self):
        # Get the updated title_transfer list from the controller
        titles = self.controller.title_transfer
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"
        query = "SELECT title, Description FROM books"
        db_users.cursor.execute(query)
        all_descriptions = db_users.cursor.fetchall()
        

        if not hasattr(self, 'description_label'):
            self.description_label = ctk.CTkLabel(self.right_frame, text="Description", text_color="black", font=("Arial", 16, "bold"))
            self.description_label.pack(pady=(10, 5))

        for names in all_descriptions:

            if titles[0] == names[0]:
                if hasattr(self, 'description'):
                    self.description.destroy()
        # Display the description in the right frame
                self.description = ctk.CTkLabel(self.right_frame, text=names[1], wraplength=400, justify="left",text_color="black",font=("Arial", 20))
                self.description.pack(pady=10)
                break  



        
        # showing images
        for file_name in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, file_name)
            title = os.path.splitext(file_name)[0].replace("_", " ")
            if os.path.isfile(file_path) and file_name.endswith(('.jpg', '.png', '.jpeg')):
                if title in titles:
                    img = Image.open(file_path).resize((500, 700))  # Zoomed-in size
                    photo = ctk.CTkImage(light_image=img, size=(500, 700))
                    # Display the image in the grid
                    img_label = ctk.CTkLabel(self.left_frame, image=photo,text=" ")
                    img_label.image = photo  # Keep a reference to avoid garbage collection
                    self.left_frame.columnconfigure(0, weight=1, minsize=50)  # Add a spacer column
                    img_label.grid(row=6, column=1, padx=30, pady=5, sticky="w")

        
        # Update the label text with the titles
        self.title_label.configure(text="\n".join(titles))
        self.controller.title_transfer.clear()
    def zoom_in_frame(self, scale_factor=20.0):

        # Get the main application window
        window = self.controller.winfo_toplevel()

        # Get the current screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate new dimensions based on the scale factor
        new_width = int(screen_width / scale_factor)
        new_height = int(screen_height / scale_factor)

        # Center the zoomed-in window on the screen
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2

        # Update the window geometry
        window.geometry(f"{new_width}x{new_height}+{x_offset}+{y_offset}")

        # Optionally scale the CTk widgets
        ctk.set_widget_scaling(scale_factor)



    def reset_zoom(self):

        # Get the main application window
        window = self.controller.winfo_toplevel()

        # Reset to default size (1920x1080 for your case)
        window.geometry("1920x1080")

        # Reset widget scaling to normal
        ctk.set_widget_scaling(1.0)
