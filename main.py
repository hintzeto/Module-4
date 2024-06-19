import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import io
import sqlite3

class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)
        self.title("User Management System")
        self.geometry("1000x500")
        self.set_theme("breeze")
        
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, AddUserPage, ViewUsersPage, AddPointsPage, EditUserPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="User Management System", font=("Arial", 16))
        label.pack(pady=10, padx=10)
        
        add_user_button = ttk.Button(self, text="Add User",
                                     command=lambda: controller.show_frame("AddUserPage"))
        add_user_button.pack()
        
        view_users_button = ttk.Button(self, text="View Users",
                                       command=lambda: controller.show_frame("ViewUsersPage"))
        view_users_button.pack()
        
        add_points_button = ttk.Button(self, text="Add Points",
                                       command=lambda: controller.show_frame("AddPointsPage"))
        add_points_button.pack()

class AddUserPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Add User", font=("Arial", 16))
        label.pack(pady=10, padx=10)
        
        self.fname_var = StringVar()
        self.lname_var = StringVar()
        self.username_var = StringVar()
        
        fname_label = ttk.Label(self, text="First Name:")
        fname_label.pack(pady=5)
        self.fname_entry = ttk.Entry(self, textvariable=self.fname_var)
        self.fname_entry.pack(pady=5)
        
        lname_label = ttk.Label(self, text="Last Name:")
        lname_label.pack(pady=5)
        self.lname_entry = ttk.Entry(self, textvariable=self.lname_var)
        self.lname_entry.pack(pady=5)
        
        username_label = ttk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(pady=5)
        
        add_user_button = ttk.Button(self, text="Add User", command=self.add_user)
        add_user_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)
    
    def add_user(self):
        fname = self.fname_var.get()
        lname = self.lname_var.get()
        username = self.username_var.get()
        rankID = get_bronze_rank_id()

        if fname and lname and username:
            try:
                conn = sqlite3.connect('typing.db')
                conn.execute("INSERT INTO User (fname, lname, username, rankID, points) VALUES (?, ?, ?, ?, ?)",
                             (fname, lname, username, rankID, 0))  # Initialize points to 0
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"User {fname} {lname} successfully added to the database.")
                self.fname_entry.delete(0, 'end')
                self.lname_entry.delete(0, 'end')
                self.username_entry.delete(0, 'end')
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

class ViewUsersPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="View Users", font=("Arial", 16))
        label.pack(pady=10, padx=10)
        
        # Create a canvas and a frame for the content
        self.canvas = tk.Canvas(self)
        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        self.image_labels = {}
        
        refresh_button = ttk.Button(self, text="Refresh", command=self.view_users)
        refresh_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)
        
        self.frame.bind("<Configure>", self.on_frame_configure)
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def view_users(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        conn = sqlite3.connect('typing.db')
        cursor = conn.execute("""
            SELECT User.ID, User.fname, User.lname, User.username, User.points, Rank.rankname, Rank.icon
            FROM User
            JOIN Rank ON User.rankID = Rank.ID
        """)
        
        for row in cursor:
            user_id, fname, lname, username, points, rankname, icon_blob = row
            row_frame = ttk.Frame(self.frame)
            row_frame.pack(fill="x")
            
            tk.Label(row_frame, text=user_id, width=10).pack(side="left")
            tk.Label(row_frame, text=fname, width=20).pack(side="left")
            tk.Label(row_frame, text=lname, width=20).pack(side="left")
            tk.Label(row_frame, text=username, width=20).pack(side="left")
            tk.Label(row_frame, text=rankname, width=20).pack(side="left")
            
            # Load and resize the image
            image = Image.open(io.BytesIO(icon_blob))
            image = image.resize((50, 50), Image.LANCZOS)  # Resize to 50x50 pixels
            photo_image = ImageTk.PhotoImage(image)
            
            self.image_labels[user_id] = photo_image  # Keep a reference to avoid garbage collection
            image_label = tk.Label(row_frame, image=photo_image, width=50)
            image_label.pack(side="left")
            
            tk.Label(row_frame, text=points, width=10).pack(side="left")

            edit_button = ttk.Button(row_frame, text="Edit", command=lambda uid=user_id, fn=fname, ln=lname, un=username: self.edit_user(uid, fn, ln, un))
            edit_button.pack(side="left")

            delete_button = ttk.Button(row_frame, text="Delete", command=lambda uid=user_id: self.delete_user(uid))
            delete_button.pack(side="left")
        
        conn.close()

    def edit_user(self, user_id, fname, lname, username):
        edit_page = self.controller.frames["EditUserPage"]
        edit_page.load_user(user_id, fname, lname, username)
        self.controller.show_frame("EditUserPage")

    def delete_user(self, user_id):
        confirm = messagebox.askyesno("Delete User", "Are you sure you want to delete this user?")
        if confirm:
            try:
                conn = sqlite3.connect('typing.db')
                conn.execute("DELETE FROM User WHERE ID = ?", (user_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User successfully deleted.")
                self.view_users()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

class AddPointsPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Add Points to User", font=("Arial", 16))
        label.pack(pady=10, padx=10)
        
        self.username_var = StringVar()
        self.points_var = StringVar()
        
        username_label = ttk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(pady=5)
        
        points_label = ttk.Label(self, text="Points:")
        points_label.pack(pady=5)
        self.points_entry = ttk.Entry(self, textvariable=self.points_var)
        self.points_entry.pack(pady=5)
        
        add_points_button = ttk.Button(self, text="Add Points", command=self.add_points)
        add_points_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)
    
    def add_points(self):
        username = self.username_var.get()
        points = self.points_var.get()

        if username and points.isdigit():
            try:
                points = int(points)
                conn = sqlite3.connect('typing.db')
                cursor = conn.execute("SELECT ID FROM User WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result:
                    user_id = result[0]
                    conn.execute("UPDATE User SET points = points + ? WHERE ID = ?", (points, user_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", f"Added {points} points to user {username}.")
                    self.username_entry.delete(0, 'end')
                    self.points_entry.delete(0, 'end')
                else:
                    messagebox.showwarning("Input Error", "Username not found.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required and points must be a number.")

class EditUserPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Edit User", font=("Arial", 16))
        label.pack(pady=10, padx=10)

        self.fname_var = StringVar()
        self.lname_var = StringVar()
        self.username_var = StringVar()
        self.user_id = None

        fname_label = ttk.Label(self, text="First Name:")
        fname_label.pack(pady=5)
        self.fname_entry = ttk.Entry(self, textvariable=self.fname_var)
        self.fname_entry.pack(pady=5)

        lname_label = ttk.Label(self, text="Last Name:")
        lname_label.pack(pady=5)
        self.lname_entry = ttk.Entry(self, textvariable=self.lname_var)
        self.lname_entry.pack(pady=5)

        username_label = ttk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(pady=5)

        update_user_button = ttk.Button(self, text="Update User", command=self.update_user)
        update_user_button.pack(pady=10)

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("ViewUsersPage"))
        back_button.pack(pady=10)

    def load_user(self, user_id, fname, lname, username):
        self.user_id = user_id
        self.fname_var.set(fname)
        self.lname_var.set(lname)
        self.username_var.set(username)

    def update_user(self):
        fname = self.fname_var.get()
        lname = self.lname_var.get()
        username = self.username_var.get()

        if fname and lname and username:
            try:
                conn = sqlite3.connect('typing.db')
                conn.execute("UPDATE User SET fname = ?, lname = ?, username = ? WHERE ID = ?",
                             (fname, lname, username, self.user_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"User {fname} {lname} successfully updated.")
                self.controller.show_frame("ViewUsersPage")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

def get_bronze_rank_id():
    conn = sqlite3.connect('typing.db')
    cursor = conn.execute("SELECT ID FROM Rank WHERE rankname = 'Bronze'")
    bronze_rank_id = cursor.fetchone()[0]
    conn.close()
    return bronze_rank_id

if __name__ == "__main__":
    app = App()
    app.mainloop()
