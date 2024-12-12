import customtkinter as ctk
import sqlite3
import db_users
import requests
from io import BytesIO
from PIL import Image, ImageTk



class mainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text= "main page", font=("Arial", 20))
        
        label.pack(pady =20)

        back_button = ctk.CTkButton(
            self, text="Back to Login", command=lambda: controller.show_frame("Login")
        )
        back_button.pack(pady=20)


        db_users.cursor.execute("SELECT img_url FROM books")
        first_book = db_users.cursor.fetchone()

        if first_book:
            img_url = first_book[0]  # Get the first book's URL
            
            # Fetch the JSON response
            response = requests.get(img_url)
            response.raise_for_status()
            response_json = response.json()

            # Extract the direct image URL
            working_image = response_json.get("url")
            if not working_image:
                print(f"No 'url' found in response: {response_json}")
                return  # Exit if the 'url' key is missing

            # Fetch the actual image
            working_response = requests.get(working_image)
            working_response.raise_for_status()

            # Open, resize, and display the image
            img = Image.open(BytesIO(working_response.content)).resize((150, 200))  # Resize the image
            photo = ctk.CTkImage(light_image=img, size=(150, 200))  # Use CTkImage for scaling

            # Create a label to display the image
            img_label = ctk.CTkLabel(self, image=photo)
            img_label.image = photo  # Keep a reference to avoid garbage collection
            img_label.pack(pady=10)


