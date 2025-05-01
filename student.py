import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# Create the STUDENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME TEXT,
    CLASS TEXT,
    SECTION TEXT,
    MARKS INTEGER
);
""")

# Insert sample records
students = [
    ('Krish', 'Data Science', 'A', 90),
    ('Sudhanshu', 'Data Science', 'B', 100),
    ('Darius', 'Data Science', 'A', 86),
    ('Vikash', 'DEVOPS', 'A', 50),
    ('Dipesh', 'DEVOPS', 'A', 35),
]

cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?);", students)

# Commit and close connection
connection.commit()
connection.close()

print("✅ student.db created with sample data.")
