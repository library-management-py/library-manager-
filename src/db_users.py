import os
import requests
import sqlite3

# Database connection
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

