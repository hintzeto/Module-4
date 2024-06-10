import sqlite3

conn = sqlite3.connect('typing.db')

print("Opened database successfully")

conn.execute('DROP TABLE IF EXISTS User')

conn.execute('''CREATE TABLE User
             (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
             fname       TEXT    NOT NULL,
             lname       TEXT    NOT NULL,
             username    TEXT    NOT NULL,
             rankID      INTEGER,
             FOREIGN KEY(rankID) REFERENCES Rank(ID))''')
print("User table created successfully")

conn.execute('DROP TABLE IF EXISTS Rank')

conn.execute('''CREATE TABLE Rank
             (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             rankname   TEXT    NOT NULL,
             points     INT     NOT NULL,
             icon       TEXT    NOT NULL)''')
print("Rank table created successfully")

conn.execute("INSERT INTO User (fname,lname,username,rankID) \
      VALUES ('Talon', 'Hintze', 'Bungus', 1)");

cursor = conn.execute("SELECT fname, lname FROM User")

for row in cursor:
    fname, lname = row

print(f"User: {fname} {lname} has been added successfully")

ranks = [
    ('Bronze', 100, 'icons\\Bronze_Rank_Icon.png'),
    ('Silver', 200, 'icons\\silver_Rank_Icon.png'),
    ('Gold', 400, 'icons\\gold_Rank_Icon.png'),
    ('Platinum', 800, 'icons\\platinum_Rank_Icon.png'),
]

conn.executemany("INSERT INTO Rank (rankname, points, icon) VALUES (?, ?, ?)", ranks)
conn.commit()

cursor = conn.execute("SELECT rankname FROM Rank")

for row in cursor:
    rankname = row[0]
    print(f"{rankname} successfully added to Rank table")