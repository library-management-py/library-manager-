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

import customtkinter as ctk

class mainpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header Frame
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(expand=True, padx=20, pady=20)  # Centered frame

        # Page Title
        self.title_label = ctk.CTkLabel(header_frame, text="Main Page", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Search Type Segmented Button
        self.segmented_var = ctk.StringVar(value="basic search")
        self.segmented_button = ctk.CTkSegmentedButton(
            header_frame, values=["basic search", "advanced search"],
            command=self.segmented_buttons, variable=self.segmented_var
        )
        self.segmented_button.grid(row=1, column=0, columnspan=2, pady=(10, 20))

        # Basic Search Label
        self.basic_search_label = ctk.CTkLabel(header_frame, text="Search for books:")
        self.basic_search_label.grid(row=2, column=0, columnspan=2, pady=(10, 10))
        self.basic_search_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter search term")

        # Advanced Search Fields (Hidden by Default)
        self.author_label = ctk.CTkLabel(header_frame, text="Author:")
        self.author_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter author's name")

        self.title_label_adv = ctk.CTkLabel(header_frame, text="Title:")
        self.title_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter book title")

        self.genre_label = ctk.CTkLabel(header_frame, text="Genre:")
        self.genre_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter book genre")

        self.year_label = ctk.CTkLabel(header_frame, text="Year:")
        self.year_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter year of publication")

        self.isbn_label = ctk.CTkLabel(header_frame, text="ISBN:")
        self.isbn_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter ISBN number")

        # Search Button
        self.search_button = ctk.CTkButton(header_frame, text="Search")
        self.search_button.grid(row=8, column=0, columnspan=2, pady=(10, 10))

        # Back Button
        self.back_button = ctk.CTkButton(
            header_frame, text="Back to Login",
            command=lambda: controller.show_frame("Login")
        )
        self.back_button.grid(row=9, column=0, columnspan=2, pady=(5, 20))

        # Show Basic Search by Default
        self.segmented_buttons("basic search")

        

        # Canvas and Scrollbar Section
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

        # Frame inside Canvas for Grid Layout
        self.image_frame = ctk.CTkFrame(self.canvas)  
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        self.image_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Show Images in Grid
        self.show_image()


    def segmented_buttons(self,value):
        self.author_label.grid_forget()
        self.author_entry.grid_forget()
        self.title_label_adv.grid_forget()
        self.title_entry.grid_forget()
        self.genre_label.grid_forget()
        self.genre_entry.grid_forget()
        self.year_label.grid_forget()
        self.year_entry.grid_forget()
        self.isbn_label.grid_forget()
        self.isbn_entry.grid_forget()

        # Hide Basic Search Widgets
        self.basic_search_label.grid_forget()
        self.basic_search_entry.grid_forget()

        if value == "basic search":
            self.basic_search_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            self.basic_search_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        elif value == "advanced search":
            # Remove basic search label
            self.basic_search_label.grid_forget()

            self.author_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            self.author_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            self.title_label_adv.grid(row=3, column=0, padx=10, pady=5, sticky="e")
            self.title_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            self.genre_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            self.genre_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            self.year_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
            self.year_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

            self.isbn_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
            self.isbn_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    def on_book_page_button(self):

        self.controller.show_frame("bookpage")

    def on_mouse_scroll(self, event):
        if event.delta > 0:  # for scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.delta < 0:  # for scroll down
            self.canvas.yview_scroll(1, "units")   

    def button_maker(self,title):
        test_button = ctk.CTkButton(self.image_frame,text=title, border_width=0,fg_color="transparent", command=self.on_book_page_button)
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
                if column == 3:  # Move to the next row after 5 images
                    column = 0
                    row += 2

        # End timer
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to load images: {elapsed_time:.2f} seconds")
