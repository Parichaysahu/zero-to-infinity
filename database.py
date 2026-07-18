import sqlite3
from datetime import date

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
def init_batches_table():
    """Creates the batches table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            schedule TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_batch(batch_name, subject, schedule):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO batches (batch_name, subject, schedule)
        VALUES (?, ?, ?)
    """, (batch_name, subject, schedule))
    conn.commit()
    conn.close()

def get_all_batches():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM batches")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_batch(batch_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM batches WHERE id = ?", (batch_id,))
    conn.commit()
    conn.close()

def add_batch_id_column():
    """Adds a batch_id column to students table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN batch_id INTEGER")
    except sqlite3.OperationalError:
        # Column already exists, ignore
        pass
    conn.commit()
    conn.close()

def assign_student_to_batch(student_id, batch_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET batch_id = ? WHERE id = ?", (batch_id, student_id))
    conn.commit()
    conn.close()

def get_students_by_batch(batch_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE batch_id = ?", (batch_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_batch_name(batch_id):
    if batch_id is None:
        return "Not Assigned"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT batch_name FROM batches WHERE id = ?", (batch_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "Not Assigned"

def init_attendance_table():
    """Creates the attendance table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            batch_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(student_id, batch_id, date, status):
    """Saves or updates a student's attendance for a specific date."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Check if attendance for this student on this date already exists
    cursor.execute("""
        SELECT id FROM attendance WHERE student_id = ? AND date = ?
    """, (student_id, date))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE attendance SET status = ?, batch_id = ? WHERE id = ?
        """, (status, batch_id, existing[0]))
    else:
        cursor.execute("""
            INSERT INTO attendance (student_id, batch_id, date, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, batch_id, date, status))

    conn.commit()
    conn.close()

def get_attendance_for_batch_on_date(batch_id, date):
    """Returns a dict of {student_id: status} for a batch on a specific date."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_id, status FROM attendance WHERE batch_id = ? AND date = ?
    """, (batch_id, date))
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_attendance_history(student_id):
    """Returns all attendance records for a student, most recent first."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_attendance_percentage(student_id):
    """Calculates the percentage of days marked Present for a student."""
    history = get_attendance_history(student_id)
    if not history:
        return 0
    present_count = sum(1 for date, status in history if status == "Present")
    return round((present_count / len(history)) * 100, 1)

def init_fees_table():
    """Creates the fees table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount_due REAL NOT NULL,
            amount_paid REAL NOT NULL DEFAULT 0,
            due_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_fee_record(student_id, description, amount_due, due_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fees (student_id, description, amount_due, amount_paid, due_date)
        VALUES (?, ?, ?, 0, ?)
    """, (student_id, description, amount_due, due_date))
    conn.commit()
    conn.close()

def get_fees_for_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, description, amount_due, amount_paid, due_date
        FROM fees WHERE student_id = ? ORDER BY due_date DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def record_payment(fee_id, payment_amount):
    """Adds a payment to an existing fee record's amount_paid."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount_paid FROM fees WHERE id = ?", (fee_id,))
    row = cursor.fetchone()
    if row:
        new_amount_paid = row[0] + payment_amount
        cursor.execute("UPDATE fees SET amount_paid = ? WHERE id = ?", (new_amount_paid, fee_id))
        conn.commit()
    conn.close()

def get_total_pending_dues(student_id):
    """Returns total pending amount (due - paid) across all fee records for a student."""
    fees = get_fees_for_student(student_id)
    total_pending = sum(amount_due - amount_paid for _, _, amount_due, amount_paid, _ in fees)
    return round(total_pending, 2)

def init_exams_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            batch_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            max_marks REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_exam(exam_name, subject, batch_id, date, max_marks):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exams (exam_name, subject, batch_id, date, max_marks)
        VALUES (?, ?, ?, ?, ?)
    """, (exam_name, subject, batch_id, date, max_marks))
    conn.commit()
    conn.close()

def get_all_exams():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_exam_by_id(exam_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def init_marks_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            marks_obtained REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def record_marks(exam_id, student_id, marks_obtained):
    """Saves or updates a student's marks for a specific exam."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM marks WHERE exam_id = ? AND student_id = ?
    """, (exam_id, student_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE marks SET marks_obtained = ? WHERE id = ?", (marks_obtained, existing[0]))
    else:
        cursor.execute("""
            INSERT INTO marks (exam_id, student_id, marks_obtained)
            VALUES (?, ?, ?)
        """, (exam_id, student_id, marks_obtained))

    conn.commit()
    conn.close()

def get_marks_for_exam(exam_id):
    """Returns a dict of {student_id: marks_obtained} for a given exam."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, marks_obtained FROM marks WHERE exam_id = ?", (exam_id,))
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_progress_for_student(student_id):
    """Returns a list of (exam_name, subject, date, marks_obtained, max_marks) for a student."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT exams.exam_name, exams.subject, exams.date, marks.marks_obtained, exams.max_marks
        FROM marks
        JOIN exams ON marks.exam_id = exams.id
        WHERE marks.student_id = ?
        ORDER BY exams.date DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_students_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_batches_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM batches")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_fees_collected():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_paid) FROM fees")
    total = cursor.fetchone()[0]
    conn.close()
    return round(total, 2) if total else 0

def get_total_pending_dues_all():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_due - amount_paid) FROM fees")
    total = cursor.fetchone()[0]
    conn.close()
    return round(total, 2) if total else 0

def get_today_attendance_summary():
    """Returns (present_count, absent_count) for today's date."""
    today_str = str(date.today())
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Present'", (today_str,))
    present = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Absent'", (today_str,))
    absent = cursor.fetchone()[0]
    conn.close()
    return present, absent

def get_average_marks_percentage(student_id):
    """Returns the average percentage score across all exams for a student."""
    progress = get_progress_for_student(student_id)
    if not progress:
        return 0
    percentages = [(marks / max_marks) * 100 for _, _, _, marks, max_marks in progress if max_marks > 0]
    if not percentages:
        return 0
    return round(sum(percentages) / len(percentages), 1)