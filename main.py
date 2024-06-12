import sqlite3
from tkinter import Tk, StringVar, messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
from PIL import Image, ImageTk
import io

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
        for F in (StartPage, AddUserPage, ViewUsersPage, AddPointsPage):
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
        
        self.tree = ttk.Treeview(self, columns=("ID", "First Name", "Last Name", "Username", "Rank", "Icon", "Points"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Icon", text="Icon")
        self.tree.heading("Points", text="Points")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.image_labels = {}
        
        refresh_button = ttk.Button(self, text="Refresh", command=self.view_users)
        refresh_button.pack(pady=10)
        
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack(pady=10)
    
    def view_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        conn = sqlite3.connect('typing.db')
        cursor = conn.execute("""
            SELECT User.ID, User.fname, User.lname, User.username, User.points, Rank.rankname, Rank.icon
            FROM User
            JOIN Rank ON User.rankID = Rank.ID
        """)
        
        for row in cursor:
            user_id, fname, lname, username, points, rankname, icon_blob = row
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(icon_blob)))
            self.image_labels[user_id] = image  # Keep a reference to avoid garbage collection
            self.tree.insert("", "end", values=(user_id, fname, lname, username, rankname, "Icon", points))
        
        conn.close()

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

def get_bronze_rank_id():
    conn = sqlite3.connect('typing.db')
    cursor = conn.execute("SELECT ID FROM Rank WHERE rankname = 'Bronze'")
    bronze_rank_id = cursor.fetchone()[0]
    conn.close()
    return bronze_rank_id

def retrieve_image(rank_id):
    conn = sqlite3.connect('typing.db')
    cursor = conn.execute("SELECT icon FROM Rank WHERE ID=?", (rank_id,))
    blob_data = cursor.fetchone()[0]
    conn.close()
    image = Image.open(io.BytesIO(blob_data))
    return ImageTk.PhotoImage(image)

if __name__ == "__main__":
    app = App()
    app.mainloop()
