import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully")

conn.execute('DROP TABLE IF EXISTS COMPANY')

conn.execute('''CREATE TABLE COMPANY
             (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
             NAME       TEXT    NOT NULL,
             AGE        INT     NOT NULL,
             ADDRESS    CHAR(50),
             SALARY     REAL);''')
print("Table created successfully")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Paul', 32, 'California', 20000.00 ) \
      VALUES ('Talon', 22, '460 S. 2nd West', 70000.00)");


print("insert successful")