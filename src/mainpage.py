import customtkinter as ctk
import sqlite3
import db_users as db_users
import requests
from io import BytesIO
from PIL import Image, ImageTk
import threading
import time
import requests
import queue
from io import StringIO 
from urllib.request import urlopen
import os

class mainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        

        label = ctk.CTkLabel(self, text= "main page", font=("Arial", 20))
        
        label.pack(pady =20)

        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login")
        )
        back_button.pack(pady=20)


        canvas = ctk.CTkCanvas(self, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        self.image_frame = ctk.CTkFrame(canvas)
        self.image_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.show_image()
 

    def show_image(self):
        # Directory containing cached images
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"
        row, column = 0, 0  # Start positions for the grid layout
    
        start_time = time.time()  # Start timer for performance tracking
    
        # Iterate through all files in the cache directory
        for file_name in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, file_name)
    
            # Ensure the file is an image
            if os.path.isfile(file_path) and file_name.endswith(('.jpg', '.png', '.jpeg')):
                # Open and resize the image
                img = Image.open(file_path).resize((250, 350))
                photo = ctk.CTkImage(light_image=img, size=(250, 350))
    
                # Display the image in the grid
                img_label = ctk.CTkLabel(self.image_frame, image=photo)
                img_label.image = photo  # Keep a reference to avoid garbage collection
                img_label.grid(row=row, column=column, padx=10, pady=10)
    
                # Extract title from the file name (replace underscores with spaces)
                title = os.path.splitext(file_name)[0].replace("_", " ")
    
                # Create a label for the title below the image
                title_label = ctk.CTkLabel(
                    self.image_frame,
                    text=title,
                    font=("Arial", 14),
                    text_color="white",
                    anchor="center"
                )
                title_label.grid(row=row + 1, column=column, padx=10, pady=(0, 20))
    
                # Update column and row for the next image
                column += 1
                if column == 5:  # Move to the next row after 5 images
                    column = 0
                    row += 2
    
        # End timer and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to load images: {elapsed_time:.2f} seconds")
    