import os
import requests
import sqlite3
import sys
# Database connection
if hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller executable
    db_path = os.path.join(sys._MEIPASS, "database.db")
else:
    # Running from the source code
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

