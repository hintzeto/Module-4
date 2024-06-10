import sqlite3

conn = sqlite3.connect("test.db")

print("Connected")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Paul', 32, 'California', 20000.00 )");

print("insert successful")