import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect("typing.db")
print("Connected")

# Create a cursor object
cursor = conn.cursor()

# Execute the query to select all records from the User table
cursor.execute("SELECT * FROM User")

# Fetch all results from the executed query
rows = cursor.fetchall()

# Fetch column names
column_names = [description[0] for description in cursor.description]

# Print column names
print("Columns:", column_names)

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
