import customtkinter as ctk
import os
from PIL import Image
import db_users
import sys

class bookpage(ctk.CTkFrame):
    def __init__(self, parent, controller, cache_dir=None,base_dir=None):
        super().__init__(parent)
        self.controller = controller

        base_dir = base_dir if base_dir else os.path.dirname(os.path.abspath(__file__))

        # Set the cache directory
        self.cache_dir = cache_dir if cache_dir else os.path.join(base_dir, "cached_images")
        if not os.path.exists(self.cache_dir):
            raise FileNotFoundError(f"Cache directory not found: {self.cache_dir}")

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
            command=lambda: self.back_to_main(),
            font=("Arial", 14),
            fg_color="black",
            text_color="white",
        )
        self.back_button.pack(anchor="n", pady=20)

        # Label for displaying titles
        self.title_label = ctk.CTkLabel(self.right_frame, text="Title List", font=("Arial", 24), text_color="black")
        self.title_label.pack(pady=20)

        # Initialize buttons as None
        self.borrow_button = None
        self.return_button = None
        self.img_label = None  # Add this to track the image label
        
    def clean_frames(self):
        # Clean up the left frame
        for widget in self.left_frame.winfo_children():
            widget.destroy()
            
        # Clean up the right frame, preserving the back button and title label
        for widget in self.right_frame.winfo_children():
            if widget not in [self.back_button, self.title_label]:
                widget.destroy()

    def back_to_main(self):
        self.controller.title_transfer.clear()
        self.update_profile_page()
        self.controller.show_frame("mainpage")

    def on_show(self):
        # Clean up previous content
        self.clean_frames()
        
        titles = self.controller.title_transfer.copy()

        
        self.update_profile_page()

        # Clear title_label before updating it
        self.title_label.configure(text="")
        
        query = "SELECT id, title, description, borrowed FROM books"
        db_users.cursor.execute(query)
        all_books = db_users.cursor.fetchall()

        # Create description label if it doesn't exist
        self.description_label = ctk.CTkLabel(
            self.right_frame, 
            text="Description", 
            text_color="black", 
            font=("Arial", 16, "bold")
        )
        self.description_label.pack(pady=(10, 5))

        for book in all_books:
            book_id, book_title, book_description, borrowed_status = book

            if titles and titles[0] == book_title:
                # Display the description in the right frame
                self.description = ctk.CTkLabel(
                    self.right_frame, 
                    text=book_description, 
                    wraplength=400, 
                    justify="left", 
                    text_color="black", 
                    font=("Arial", 20)
                )
                self.description.pack(pady=10)

                # Add Borrow Button
                self.borrow_button = ctk.CTkButton(
                    self.right_frame,
                    text="BORROW" if borrowed_status == 'no' else "ALREADY BORROWED",
                    command=lambda b_id=book_id, b_status=borrowed_status: self.borrow_book(b_id, b_status),
                    font=("Arial", 16),
                    fg_color="green" if borrowed_status == 'no' else "gray",
                    text_color="white"
                )
                self.borrow_button.pack(pady=10)

                # Add Return Button
                self.return_button = ctk.CTkButton(
                    self.right_frame,
                    text="RETURN",
                    command=lambda b_id=book_id: self.return_book(b_id) if borrowed_status == 'yes' else None,
                    font=("Arial", 16),
                    fg_color="red" if borrowed_status == 'yes' else "gray",
                    text_color="white"
                )
                self.return_button.pack(pady=10)
                break

        # Display image
        if titles:
            for file_name in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, file_name)
                title = os.path.splitext(file_name)[0].replace("_", " ")
                if os.path.isfile(file_path) and file_name.endswith((".jpg", ".png", ".jpeg")):
                    if title in titles:
                        img = Image.open(file_path).resize((500, 700))
                        photo = ctk.CTkImage(light_image=img, size=(500, 700))
                        self.img_label = ctk.CTkLabel(self.left_frame, image=photo, text=" ")
                        self.img_label.image = photo
                        self.left_frame.columnconfigure(0, weight=1, minsize=50)
                        self.img_label.grid(row=6, column=1, padx=30, pady=5, sticky="w")
                        break

        self.title_label.configure(text="\n".join(titles) if titles else "No title selected.")

    def borrow_book(self, book_id, borrowed_status):
        if borrowed_status == 'no':
            update_query = "UPDATE books SET borrowed = 'yes' WHERE id = ?"
            db_users.cursor.execute(update_query, (book_id,))
            db_users.connection.commit()
            self.update_profile_page()  # Update profile page with borrowed books
            self.on_show()  # Refresh the book page

    def return_book(self, book_id):
        update_query = "UPDATE books SET borrowed = 'no' WHERE id = ?"
        db_users.cursor.execute(update_query, (book_id,))
        db_users.connection.commit()
        self.update_profile_page()
        self.on_show()

    def update_profile_page(self):
        profile_page = self.controller.frames.get("profilepage")
        if profile_page:
            query = "SELECT title FROM books WHERE borrowed = 'yes'"
            db_users.cursor.execute(query)
            borrowed_books = db_users.cursor.fetchall()
            borrowed_books_list = "\n".join([f"• {book[0]}" for book in borrowed_books]) if borrowed_books else "No books borrowed."
            profile_page.update_borrowed_books(borrowed_books_list)

    def zoom_in_frame(self, scale_factor=20.0):
        window = self.controller.winfo_toplevel()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        new_width = int(screen_width / scale_factor)
        new_height = int(screen_height / scale_factor)
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2
        window.geometry(f"{new_width}x{new_height}+{x_offset}+{y_offset}")
        ctk.set_widget_scaling(scale_factor)

    def reset_zoom(self):
        window = self.controller.winfo_toplevel()
        window.geometry("1920x1080")
        ctk.set_widget_scaling(1.0)