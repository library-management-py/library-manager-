import customtkinter as ctk
import db_users as db_users
from PIL import Image, ImageTk
import queue
import os
import random
from tkinter import ttk


class mainpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Main layout
        parent_frame = ctk.CTkFrame(self, fg_color="#FCF1D8") 
        parent_frame.grid(row=0, column=0, sticky="nsew")
        self.separator_line = ctk.CTkFrame(parent_frame, height=2, fg_color="black")
        self.separator_line.grid(row=1, column=1, sticky="ew", padx=0, pady=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)

        # Header frame (will be on the left side)
        self.header_frame = ctk.CTkFrame(parent_frame, width=250, fg_color="#FCF1D8") 
        self.header_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=10, pady=10)
        self.header_frame.grid_propagate(False)  # Keep width fixed

        # Left frame (now will be at the top of right side)
        self.left_frame = ctk.CTkFrame(parent_frame, height=50, fg_color="#FCF1D8")
        self.left_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.left_frame.grid_propagate(False)

        

        # Segmented button 
        self.segmented_var = ctk.StringVar(value="basic search")
        self.segmented_button = ctk.CTkSegmentedButton(
            self.header_frame,
            values=["basic search", "advanced search"],
            command=self.segmented_buttons,
            variable=self.segmented_var,
            fg_color="white", 
            selected_color="white",
            unselected_color="lightgray",
            text_color="black",
            corner_radius=10  # Rounded corners
        )
        self.segmented_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Option menu
        self.option_menu = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Alphabetically", "By Date - Oldest to Newest", "By Date - Newest to Oldest"],
            command=self.option_selected,  
            fg_color="white",
            dropdown_fg_color="#FCF1D8",  # Dropdown background color
            button_color="white",         # Button background color
            button_hover_color="white", # Hover effect for the button
            text_color="black",
            dropdown_text_color="black",
            dropdown_hover_color="#E8E8E8"      # Text color
        )
        self.option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e") 
        self.option_menu.set("Sort By")

        # Create search widgets in header_frame (left side)
        self.create_search_widgets(header_frame=self.header_frame)

        # Canvas and image frame (right side, below left_frame)
        self.canvas = ctk.CTkCanvas(parent_frame, highlightthickness=0, bg="#FCF1D8")
        self.canvas.grid(row=1, column=1, sticky="nsew")

        # Frame inside Canvas for Grid Layout
        self.image_frame = ctk.CTkFrame(self.canvas)
        self.image_frame.configure(fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(parent_frame, orientation="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

        # Show Images in Grid
        self.show_image()
        # Show Basic Search by Default
        self.segmented_buttons("basic search")

        # Back Button (at bottom of header_frame)
        self.back_button = ctk.CTkButton(
            self.header_frame, text="Back to Login",
            command=lambda: controller.show_frame("Login")
            ,fg_color="black",  # Transparent inside
            text_color="white",      # Black text
            border_width=2,          # Black border
            border_color="black",
            hover_color="#E8E8E8"
        )
        self.back_button.grid(row=10, column=0, columnspan=2, pady=(5, 20))


    def create_search_widgets(self, header_frame):
        # Basic Search Label and Entry
        self.basic_search_label = ctk.CTkLabel(header_frame, text="Search for books:", text_color="black",font=("Arial",18))
        self.basic_search_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))
        self.basic_search_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter search term",fg_color="transparent",text_color="black")
        self.basic_search_entry.bind("<Return>", lambda event: self.search_function())

        # Advanced Search Fields
        self.author_label = ctk.CTkLabel(header_frame, text="Author:", text_color="black")
        self.author_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter author's name",fg_color="transparent")

        self.title_label_adv = ctk.CTkLabel(header_frame, text="Title:", text_color="black")
        self.title_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter book title",fg_color="transparent")

        self.genre_label = ctk.CTkLabel(header_frame, text="Genre:", text_color="black")
        self.genre_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter book genre",fg_color="transparent")

        self.year_label = ctk.CTkLabel(header_frame, text="Year:", text_color="black")
        self.year_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter year of publication",fg_color="transparent")

        self.isbn_label = ctk.CTkLabel(header_frame, text="ISBN:", text_color="black")
        self.isbn_entry = ctk.CTkEntry(header_frame, placeholder_text="Enter ISBN number",fg_color="transparent")

        # Buttons with transparent inside and black borders
        self.basic_search_button = ctk.CTkButton(
            header_frame,
            text="Search",
            command=self.search_function,
            fg_color="transparent",  # Transparent inside
            text_color="black",      # Black text
            border_width=2,          # Black border
            border_color="black"
            ,    hover_color="#E8E8E8"
        )

        self.advanced_search_button = ctk.CTkButton(
            header_frame,
            text="Advanced Search",
            command=self.advanced_search_function,
            fg_color="transparent",  # Transparent inside
            text_color="black",      # Black text
            border_width=2,          # Black border
            border_color="black",
                hover_color="#E8E8E8"
        )

        self.profile_button = ctk.CTkButton(
            header_frame,
            text="profile",
            command=self.on_porfile,
            fg_color="black",  # Transparent inside
            text_color="white",      # Black text
            border_width=2,          # Black border
            border_color="black",
                hover_color="#E8E8E8"
        )
        self.profile_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")




    def on_porfile(self):
        self.controller.show_frame("profilepage")


    def segmented_buttons(self, value):
        # Hide all widgets
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

        self.basic_search_label.grid_forget()
        self.basic_search_entry.grid_forget()
        self.basic_search_button.grid_forget()
        self.advanced_search_button.grid_forget()

        if value == "basic search":
            # Show Basic Search Widgets
            self.basic_search_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            self.basic_search_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            self.basic_search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")

        elif value == "advanced search":
            # Show Advanced Search Widgets
            self.author_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            self.author_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            self.title_label_adv.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            self.title_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            self.genre_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
            self.genre_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            self.year_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            self.year_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            self.isbn_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
            self.isbn_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

            self.advanced_search_button.grid(row=6, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")
    def on_book_page_button(self,title):
        self.controller.title_transfer.append(title)

        self.controller.show_frame("bookpage")

    def on_mouse_scroll(self, event):
        if event.delta > 0:  # for scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.delta < 0:  # for scroll down
            self.canvas.yview_scroll(1, "units")   
 
    def sort(self):
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"

        file_list = os.listdir(cache_dir)
        file = sorted(file_list)
        self.show_image(file_list=file)

 
    def show_image(self,file_list = None):
        # Directory containing cached images
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"
        row, column = 0, 0  # Start positions for the grid layout

        if file_list is None:
            file_list = os.listdir(cache_dir)
            random.shuffle(file_list)
        # go through all files in the cache directory
        for file_name in file_list:
            
            file_path = os.path.join(cache_dir, file_name)


            # Ensure the file is an image
            if os.path.isfile(file_path) and file_name.endswith(('.jpg', '.png', '.jpeg')):
                # Open and resize the image
                img = Image.open(file_path).resize((250, 350))
                photo = ctk.CTkImage(light_image=img, size=(250, 350))

            

                # this is where the image is displayed
                img_label = ctk.CTkLabel(self.image_frame, image=photo,text="")
                img_label.image = photo  # Keep a reference to avoid garbage collection
                img_label.grid(row=row, column=column, padx=10, pady=10)

                # Extract title from the file name (replace underscores with spaces)
                title = os.path.splitext(file_name)[0].replace("_", " ")
                
                title_button = ctk.CTkButton(
                self.image_frame,
                text=title,
                command=lambda t=title: self.on_book_page_button(t)
                ,fg_color="transparent",  # Transparent inside
                text_color="black",      # Black text
                border_width=2,          # Black border
                border_color="black",
                hover_color="#E8E8E8",
                font=("Arial", 13),   # Pass the title
                )
                title_button.grid(row=row + 1, column=column, padx=10, pady=(0, 20))

                # Update column and row for the next image
                column += 1
                if column == 4:  # Move to the next row after 3 images
                    column = 0
                    row += 2
        self.image_frame.update_idletasks()  # Ensure all geometry updates are processed
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def sort_by_date(self,state):
        db_users.cursor.execute("SELECT published_date, title FROM books")
        dates_title = db_users.cursor.fetchall()

        if state == "oldest to newest":
          sorted_dates = sorted(dates_title, key=lambda x: x[0])  # Oldest to Newest

            

        elif state == "newest to oldest":
            sorted_dates = sorted(dates_title, key=lambda x: x[0], reverse=True)
        unique_dates = list(dict.fromkeys(sorted_dates))

        file_list = []
        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"

        for _, title in unique_dates:  
            # get filename from title
            filename = f"{title.replace(' ', '_')}.jpg"
            file_path = os.path.join(cache_dir, filename)

            if os.path.isfile(file_path):
                file_list.append(filename)


        self.show_image(file_list=file_list)

    def option_selected(self, value):
        if value == "Alphabetically":
            self.sort()
        elif value == "By Date - Oldest to Newest":
            self.sort_by_date("oldest to newest")
        elif value == "By Date - Newest to Oldest":
            self.sort_by_date("newest to oldest")

    def search_function(self,event=None):
       search_input = self.basic_search_entry.get().lower()
       
       # Clear the current grid
       for widget in self.image_frame.winfo_children():
           widget.destroy()
       
       # If the search input is empty, reload all images
       if not search_input.strip():
           self.show_image()
           return
       
       # Filter and rebuild based on search input
       cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"
       file_list = os.listdir(cache_dir)
       filtered_files = []
       
       # Match titles with the search input
       for file_name in file_list:
           title = os.path.splitext(file_name)[0].replace("_", " ").lower()
           if search_input in title:
               filtered_files.append(file_name)
       
       # Show the filtered images
       self.show_image(file_list=filtered_files)

       self.canvas.update_idletasks()
       self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def advanced_search_function(self):
        title_value = self.title_entry.get().lower()
        author_value = self.author_entry.get().lower()
        date_value = self.year_entry.get()
        isbn_value= self.isbn_entry.get()

        title_list = []
        author_list = []
        date_list = []
        isbn_list = []

        db_users.cursor.execute("SELECT title, author, published_date, isbn FROM books ")
        rows = db_users.cursor.fetchall()

        for row in rows:
            title_list.append(row[0].lower())
            author_list.append(row[1].lower())
            date_list.append(str(row[2]))
            isbn_list.append(row[3])
        #clear the grid
        for widget in self.image_frame.winfo_children():
           widget.destroy()
    
        #reload if empty

        cache_dir = r"C:\Users\btats the kid\Desktop\code\library management\cached_images"
        file_list = os.listdir(cache_dir)
        filtered_files = []
        for file_name in file_list:
            title = os.path.splitext(file_name)[0].replace("_", " ").lower()

            # Fetch corresponding author, isbn, and year from the database
            db_users.cursor.execute(
                "SELECT author, isbn, published_date FROM books WHERE LOWER(title) LIKE ?", (f"%{title}%",)
            )
            result = db_users.cursor.fetchone()

            # Extract author, isbn, and year if available
            if result:
                author, isbn, year = result
            else:
                author, isbn, year = None, None, None

            # Match based on partial or exact year
            if (title_value and title_value in title) or \
               (author_value and author and author_value in author.lower()) or (date_value and year and date_value in str(year)) or  (isbn_value and isbn and isbn_value == isbn): 
               
              
                if file_name not in filtered_files:  # Avoid duplicates
                    filtered_files.append(file_name)


        self.show_image(file_list=filtered_files)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def rebuild_grid(self, widgets):
      
        row, column = 0, 0  # Start grid position
        for image_widget, title_widget in widgets:
            # Re-grid the image widget
            image_widget.grid(row=row, column=column, padx=10, pady=10)
            # Re-grid the title widget
            title_widget.grid(row=row + 1, column=column, padx=10, pady=(0, 20))
            
            # Update column and row for next widgets
            column += 1
            if column == 3:  # Move to the next row after 3 images
                column = 0
                row += 2
           
           
    
            
           
    