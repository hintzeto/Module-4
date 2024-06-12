import sqlite3
from tkinter import messagebox, StringVar
from ttkthemes import ThemedTk
from tkinter import ttk

# Function to get the rank ID for Bronze
def get_bronze_rank_id():
    conn = sqlite3.connect('typing.db')
    cursor = conn.execute("SELECT ID FROM Rank WHERE rankname = 'Bronze'")
    bronze_rank_id = cursor.fetchone()[0]
    conn.close()
    return bronze_rank_id

# Function to add user to the database
def add_user():
    fname = fname_var.get()
    lname = lname_var.get()
    username = username_var.get()
    rankID = get_bronze_rank_id()

    if fname and lname and username:
        try:
            conn = sqlite3.connect('typing.db')
            conn.execute("INSERT INTO User (fname, lname, username, rankID) VALUES (?, ?, ?, ?)",
                         (fname, lname, username, rankID))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"User {fname} {lname} successfully added to the database.")
            entry_fname.delete(0, 'end')
            entry_lname.delete(0, 'end')
            entry_username.delete(0, 'end')
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Set up the Tkinter GUI with ttkthemes
root = ThemedTk(theme="equilux")  # You can change "breeze" to any other theme provided by ttkthemes
root.title("Add New User")
root.geometry("400x300")

# Configure the root grid to center the frame
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Main frame for better padding and organization
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

# Ensure the frame expands to fill the window
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Inner frame to hold the form elements
inner_frame = ttk.Frame(frame)
inner_frame.grid(row=0, column=0, padx=10, pady=10)

# Variables for entries
fname_var = StringVar()
lname_var = StringVar()
username_var = StringVar()

# Labels and entries for user input within the inner frame
ttk.Label(inner_frame, text="First Name:").grid(row=0, column=0, sticky='e', pady=5, padx=5)
entry_fname = ttk.Entry(inner_frame, textvariable=fname_var, width=30)
entry_fname.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(inner_frame, text="Last Name:").grid(row=1, column=0, sticky='e', pady=5, padx=5)
entry_lname = ttk.Entry(inner_frame, textvariable=lname_var, width=30)
entry_lname.grid(row=1, column=1, pady=5, padx=5)

ttk.Label(inner_frame, text="Username:").grid(row=2, column=0, sticky='e', pady=5, padx=5)
entry_username = ttk.Entry(inner_frame, textvariable=username_var, width=30)
entry_username.grid(row=2, column=1, pady=5, padx=5)

# Button to submit the data within the inner frame
ttk.Button(inner_frame, text="Add User", command=add_user).grid(row=3, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
