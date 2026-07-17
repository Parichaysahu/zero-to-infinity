import sqlite3

DB_NAME = "zero_to_infinity.db"

def init_db():
    """Creates the students table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            joining_date TEXT NOT NULL,
            contact TEXT NOT NULL,
            enrollment_status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_student(name, student_class, joining_date, contact, enrollment_status):
    """Inserts a new student record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, student_class, joining_date, contact, enrollment_status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, student_class, joining_date, contact, enrollment_status))
    conn.commit()
    conn.close()

def get_all_students():
    """Fetches all student records from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows
def get_student_by_id(student_id):
    """Fetches a single student record by its id."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_student(student_id, name, student_class, joining_date, contact, enrollment_status):
    """Updates an existing student record."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET name = ?, student_class = ?, joining_date = ?, contact = ?, enrollment_status = ?
        WHERE id = ?
    """, (name, student_class, joining_date, contact, enrollment_status, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    """Deletes a student record by its id."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()