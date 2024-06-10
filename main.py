import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox

def get_bronze_id():
    conn = sqlite3.connect("typing.db")
    cursor = conn.execute("SELECT ID FROM Rank WHERE rankname = 'Bronze'")
    bronze_id = cursor.fetchone()[0]
    conn.close
    return bronze_id

def add_user():
    fname = entry_fname.get()