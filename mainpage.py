import customtkinter as ctk
import sqlite3
import db_users
import requests
from io import BytesIO
from PIL import Image, ImageTk
import asyncio
import aiohttp


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

 
        db_users.cursor.execute("SELECT img_url, title FROM books")
        book = db_users.cursor.fetchall()

        row = 0  # Track the current row
        column = 0  # Track the current column

        

        for element in book:
            img_url = element[0]  # Get the image URL
            title = element[1]

            # Fetch the JSON response
            response = requests.get(img_url)
            response.raise_for_status()
            response_json = response.json()
        
            # Extract the direct image URL
            actual_image = response_json.get("url")
            if not actual_image:
                print(f"No 'url' found in response: {response_json}")
                continue  # Skip if 'url' key is missing
            
            # Fetch the actual image
            actual_response = requests.get(actual_image)
            actual_response.raise_for_status()
        
            img = Image.open(BytesIO(actual_response.content)).resize((250, 350))  # Resize to fit 3 in a row
            photo = ctk.CTkImage(light_image=img, size=(250, 350))  # Set image size to match

        
            # Create a label to display the image
            img_label = ctk.CTkLabel(self.image_frame, image=photo)
            img_label.image = photo  # Keep a reference to avoid garbage collection
            img_label.grid(row=row, column=column, padx=10, pady=10)  # Position the image in grid

            # Create a label for the title below the image
            title_label = ctk.CTkLabel(
                self.image_frame,
                text=title,
                font=("Arial", 14),
                text_color="white",
                anchor="center"  # Center-align the text
            )
            title_label.grid(row=row + 1, column=column, padx=10, pady=(0, 20))

            # Update column and row for the next image
            column += 1
            if column == 5:  # Move to the next row after 3 images
                column = 0
                row += 2
        





