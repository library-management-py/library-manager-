import os
import requests
import sqlite3

# Database connection
db_path = r"C:\Users\btats the kid\Desktop\code\library management\database.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

