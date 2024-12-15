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
import os

class mainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(header_frame, text="Main Page", font=("Arial", 20))
        label.pack()

        search_label = ctk.CTkLabel(header_frame, text="Search:", font=("Arial", 14))
        search_label.pack(pady=(10, 5))

        searchbar = ctk.CTkEntry(header_frame, width=200)
        searchbar.pack(pady=(0, 20))

        back_button = ctk.CTkButton(
            header_frame, text="Back to Login", command=lambda: controller.show_frame("Login")
        )
        back_button.pack(pady=(10, 20))

        # Canvas and Scrollbar Section
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

        # Frame inside Canvas for Grid Layout
        self.image_frame = ctk.CTkFrame(self.canvas)  # Nested frame for grid layout
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        self.image_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Show Images in Grid
        self.show_image()

    def on_book_page_button(self):
        self.controller.show_frame("bookpage")

    def on_mouse_scroll(self, event):
        if event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.delta < 0:  # Scroll down
            self.canvas.yview_scroll(1, "units")   
    def button_maker(self,title):
        test_button = ctk.CTkButton(self.image_frame,text=title,border_width=0,fg_color="transparent", command=self.on_book_page_button)
        return test_button
 

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
                title_button = self.button_maker(title=title)
                title_button.grid(row=row + 1, column=column, padx=10, pady=(0, 20))

                # Update column and row for the next image
                column += 1
                if column == 5:  # Move to the next row after 5 images
                    column = 0
                    row += 2

        # End timer and calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to load images: {elapsed_time:.2f} seconds")
