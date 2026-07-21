from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import platform

if platform not in ('android', 'ios'):
    Window.size = (1500, 800)
from kivy.uix.gridlayout import GridLayout
from database import (
    init_db, add_student, get_all_students, get_student_by_id, update_student, delete_student,
    init_batches_table, add_batch, get_all_batches, delete_batch,
    add_batch_id_column, assign_student_to_batch, get_students_by_batch, get_batch_name,
    init_attendance_table, mark_attendance, get_attendance_for_batch_on_date,
    get_attendance_history, get_attendance_percentage,
    init_fees_table, add_fee_record, get_fees_for_student, record_payment, get_total_pending_dues,
    init_exams_table, add_exam, get_all_exams, get_exam_by_id,
    init_marks_table, record_marks, get_marks_for_exam, get_progress_for_student,
    get_total_students_count, get_total_batches_count, get_total_fees_collected, get_total_pending_dues_all, get_today_attendance_summary, get_average_marks_percentage,
    init_expenses_table, add_expense, get_all_expenses, delete_expense, get_total_expenses
)

# ---- COLOR THEME ----
BG_COLOR = (0.07, 0.07, 0.1, 1)        # dark navy background
PRIMARY_COLOR = (0.95, 0.5, 0.15, 1)   # orange (matches your logo)
ACCENT_COLOR = (0.2, 0.5, 0.85, 1)     # blue (matches your logo)
CARD_COLOR = (0.15, 0.15, 0.22, 1)     # lighter navy for card panels

Window.clearcolor = BG_COLOR


def styled_button(text, color=None, **kwargs):
    """Creates a Button with consistent app styling."""
    btn = Button(
        text=text,
        background_normal="",
        background_color=color if color else PRIMARY_COLOR,
        color=(1, 1, 1, 1),
        **kwargs
    )
    return btn


def title_label(text, **kwargs):
    """Creates a large, bold title Label that doesn't stretch to fill space."""
    kwargs.setdefault("size_hint_y", None)
    kwargs.setdefault("height", 40)
    return Label(text=text, font_size=22, bold=True, color=(1, 1, 1, 1), **kwargs)

def section_label(text):
    """Small uppercase section header, like 'Overview' or 'Actions'."""
    return Label(
        text=text.upper(),
        font_size=17,
        bold=True,
        color=(0.75, 0.75, 0.8, 1),
        size_hint_y=None,
        height=30,
        halign="left",
        valign="middle"
    )

def styled_input(hint_text, **kwargs):
    """Creates a TextInput with consistent app styling."""
    return TextInput(
        hint_text=hint_text,
        multiline=False,
        background_color=(0.15, 0.15, 0.22, 1),
        foreground_color=(1, 1, 1, 1),
        hint_text_color=(0.6, 0.6, 0.65, 1),
        cursor_color=(1, 1, 1, 1),
        padding=[10, 10, 10, 10],
        **kwargs
    )

def add_card_background(widget, color=CARD_COLOR, radius=12):
    """Draws a rounded rectangle behind a widget without changing its type."""
    with widget.canvas.before:
        Color(*color)
        widget._bg_rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[radius])
    widget.bind(pos=lambda w, *a: setattr(w._bg_rect, 'pos', w.pos))
    widget.bind(size=lambda w, *a: setattr(w._bg_rect, 'size', w.size))

def metric_card(label_text, value_text):
    """Small stat card: label on top, big bold value below."""
    card = BoxLayout(orientation="vertical", size_hint_y=None, height=112, padding=[14, 12], spacing=6)
    add_card_background(card, color=(0.13, 0.13, 0.19, 1))

    label = Label(text=label_text, font_size=20, color=(0.75, 0.75, 0.8, 1),
                  size_hint_y=None, height=26, halign="left", valign="middle")
    label.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], None)))
    card.add_widget(label)

    value = Label(text=value_text, font_size=32, bold=True, color=(1, 1, 1, 1),
                  size_hint_y=None, height=42, halign="left", valign="middle")
    value.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], None)))
    card.add_widget(value)

    return card

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        top_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=56, padding=[16, 0])
        add_card_background(top_bar, color=(0.09, 0.09, 0.14, 1), radius=0)
        top_bar.add_widget(title_label("Zero To Infinity", size_hint_y=None, height=56))
        self.layout.add_widget(top_bar)

        body = BoxLayout(orientation="vertical", size_hint_y=1, spacing=10, padding=16)
        self.layout.add_widget(body)

        overview_label = section_label("Overview")
        overview_label.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], None)))
        body.add_widget(overview_label)

        self.stats_grid = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        self.stats_grid.bind(minimum_height=self.stats_grid.setter("height"))
        body.add_widget(self.stats_grid)

        actions_label = section_label("Actions")
        actions_label.bind(size=lambda w, s: setattr(w, 'text_size', (s[0], None)))
        body.add_widget(actions_label)

        nav_buttons = [
        ("Add Student", "add_student"),
        ("View Students", "view_students"),
        ("Add Batch", "add_batch"),
        ("View Batches", "view_batches"),
        ("Take Attendance", "take_attendance"),
        ("Add Fee Record", "add_fee"),
        ("View Fees", "view_fees"),
        ("Add Exam", "add_exam"),
        ("Record Marks", "record_marks"),
        ("Monthly Report", "monthly_report"),
        ("Add Expense", "add_expense"),
        ("View Expenses", "view_expenses"),
        ("Timetable", "timetable"),
    ]
        
        buttons_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        buttons_box.bind(minimum_height=buttons_box.setter("height"))
        for label_text, screen_name in nav_buttons:
            btn = styled_button(label_text, size_hint_y=None, height=56)
            btn.bind(on_press=lambda instance, sn=screen_name: self.go_to_screen(sn))
            buttons_box.add_widget(btn)

        scroll = ScrollView(size_hint_y=1)
        scroll.add_widget(buttons_box)
        body.add_widget(scroll)

        footer = Label(
            text="Zero To Infinity  •  by Prateek Sir",
            font_size=12,
            color=(0.4, 0.4, 0.45, 1),
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(footer)

        self.add_widget(self.layout)
        

    def on_pre_enter(self):
        self.load_dashboard_stats()

    def load_dashboard_stats(self):
        self.stats_grid.clear_widgets()

        total_students = get_total_students_count()
        total_batches = get_total_batches_count()
        total_collected = get_total_fees_collected()
        total_pending = get_total_pending_dues_all()
        present, absent = get_today_attendance_summary()

        metrics = [
            ("Students", str(total_students)),
            ("Collected", f"₹{total_collected:.0f}"),
            ("Batches", str(total_batches)),
            ("Pending", f"₹{total_pending:.0f}"),
            ("Present today", str(present)),
            ("Absent today", str(absent)),
        ]

        for label_text, value_text in metrics:
            self.stats_grid.add_widget(metric_card(label_text, value_text))
    def go_to_screen(self, screen_name):
        self.manager.current = screen_name

class AddStudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.layout.add_widget(title_label("Add Student"))

        self.name_input = styled_input("Student Name")
        self.layout.add_widget(self.name_input)

        self.class_input = styled_input(hint_text="Class (e.g. 10th)")
        self.layout.add_widget(self.class_input)

        self.joining_date_input = styled_input(hint_text="Joining Date (YYYY-MM-DD)")
        self.layout.add_widget(self.joining_date_input)

        self.contact_input = styled_input(hint_text="Contact Number")
        self.layout.add_widget(self.contact_input)

        self.status_input = styled_input(hint_text="Enrollment Status (Active/Inactive)")
        self.layout.add_widget(self.status_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Student")
        save_btn.bind(on_press=self.save_student)
        self.layout.add_widget(save_btn)

        save_btn = styled_button("Save Student")
        back_btn = styled_button("Back to Home", color=ACCENT_COLOR)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def save_student(self, instance):
        name = self.name_input.text.strip()
        student_class = self.class_input.text.strip()
        joining_date = self.joining_date_input.text.strip()
        contact = self.contact_input.text.strip()
        status = self.status_input.text.strip()

        if not name or not student_class:
            self.message_label.text = "Name and Class are required!"
            return

        add_student(name, student_class, joining_date, contact, status)
        self.message_label.text = f"Saved: {name}"

        self.name_input.text = ""
        self.class_input.text = ""
        self.joining_date_input.text = ""
        self.contact_input.text = ""
        self.status_input.text = ""

    def go_back(self, instance):
        self.manager.current = "home"

class EditStudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_id = None
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.layout.add_widget(title_label("Edit Student"))

        self.name_input = styled_input("Student Name")
        self.layout.add_widget(self.name_input)

        self.class_input = styled_input("Class (e.g. 10th)")
        self.layout.add_widget(self.class_input)

        self.joining_date_input = styled_input("Joining Date (YYYY-MM-DD)")
        self.layout.add_widget(self.joining_date_input)

        self.contact_input = styled_input("Contact Number")
        self.layout.add_widget(self.contact_input)

        self.status_input = styled_input("Enrollment Status (Active/Inactive)")
        self.layout.add_widget(self.status_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        update_btn = Button(text="Update Student")
        update_btn.bind(on_press=self.update_student_action)
        self.layout.add_widget(update_btn)

        update_btn = styled_button("Update Student")
        back_btn = styled_button("Cancel", color=ACCENT_COLOR)

        back_btn = Button(text="Cancel")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_student(self, student_id):
        """Pre-fills the form with this student's existing data."""
        self.student_id = student_id
        student = get_student_by_id(student_id)
        _, name, student_class, joining_date, contact, status, batch_id = student

        self.name_input.text = name
        self.class_input.text = student_class
        self.joining_date_input.text = joining_date
        self.contact_input.text = contact
        self.status_input.text = status
        self.message_label.text = ""

    def update_student_action(self, instance):
        name = self.name_input.text.strip()
        student_class = self.class_input.text.strip()
        joining_date = self.joining_date_input.text.strip()
        contact = self.contact_input.text.strip()
        status = self.status_input.text.strip()

        if not name or not student_class:
            self.message_label.text = "Name and Class are required!"
            return

        update_student(self.student_id, name, student_class, joining_date, contact, status)
        self.manager.current = "view_students"

    def go_back(self, instance):
        self.manager.current = "view_students"

class AddBatchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.layout.add_widget(title_label("Add Batch"))

        self.batch_name_input = styled_input("Batch Name (e.g. Class 10 Physics Evening)")
        self.layout.add_widget(self.batch_name_input)

        self.subject_input = styled_input("Subject")
        self.layout.add_widget(self.subject_input)

        self.schedule_input = styled_input("Schedule (e.g. Mon-Wed-Fri 5-6 PM)")
        self.layout.add_widget(self.schedule_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Batch")
        save_btn.bind(on_press=self.save_batch)
        self.layout.add_widget(save_btn)

        save_btn = styled_button("Save Batch")
        back_btn = styled_button("Back to Home", color=ACCENT_COLOR)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def save_batch(self, instance):
        batch_name = self.batch_name_input.text.strip()
        subject = self.subject_input.text.strip()
        schedule = self.schedule_input.text.strip()

        if not batch_name or not subject:
            self.message_label.text = "Batch Name and Subject are required!"
            return

        add_batch(batch_name, subject, schedule)
        self.message_label.text = f"Saved: {batch_name}"

        self.batch_name_input.text = ""
        self.subject_input.text = ""
        self.schedule_input.text = ""

    def go_back(self, instance):
        self.manager.current = "home"


class AssignBatchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_id = None
        self.batch_name_to_id = {}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_label = Label(text="Assign Batch for: ", font_size=18, bold=True, color=(1, 1, 1, 1))
        self.layout.add_widget(self.student_label)

        self.batch_spinner = Spinner(
    text="Select a Batch",
    values=[],
    background_color=ACCENT_COLOR,
    color=(1, 1, 1, 1)
)
        self.layout.add_widget(self.batch_spinner)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        assign_btn = styled_button("Assign Batch")
        back_btn = styled_button("Back to View Students", color=ACCENT_COLOR)

        assign_btn = Button(text="Assign Batch")
        assign_btn.bind(on_press=self.assign_batch_action)
        self.layout.add_widget(assign_btn)

        back_btn = Button(text="Back to View Students")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_student_for_assignment(self, student_id):
        self.student_id = student_id
        student = get_student_by_id(student_id)
        _, name, student_class, joining_date, contact, status, batch_id = student
        self.student_label.text = f"Assign Batch for: {name} ({student_class})"

        batches = get_all_batches()
        self.batch_name_to_id = {batch[1]: batch[0] for batch in batches}
        self.batch_spinner.values = list(self.batch_name_to_id.keys())

        current_batch_name = get_batch_name(batch_id)
        self.batch_spinner.text = current_batch_name if current_batch_name != "Not Assigned" else "Select a Batch"

        self.message_label.text = ""

    def assign_batch_action(self, instance):
        selected_batch_name = self.batch_spinner.text
        if selected_batch_name not in self.batch_name_to_id:
            self.message_label.text = "Please select a valid batch!"
            return

        batch_id = self.batch_name_to_id[selected_batch_name]
        assign_student_to_batch(self.student_id, batch_id)
        self.manager.current = "view_students"

    def go_back(self, instance):
        self.manager.current = "view_students"

from datetime import date

class TakeAttendanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_name_to_id = {}
        self.selected_batch_id = None
        self.attendance_status = {}  # {student_id: "Present"/"Absent"}
        self.status_buttons = {}     # {student_id: button widget}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.batch_spinner = Spinner(text="Select a Batch", values=[])
        self.layout.add_widget(self.batch_spinner)

        self.date_input = TextInput(text=str(date.today()), hint_text="Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.date_input)

        load_btn = Button(text="Load Students", size_hint_y=None, height=50)
        load_btn.bind(on_press=self.load_students_for_batch)
        self.layout.add_widget(load_btn)

        self.students_grid = GridLayout(cols=2, size_hint_y=None, spacing=5, padding=5)
        self.students_grid.bind(minimum_height=self.students_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.students_grid)
        self.layout.add_widget(scroll)

        self.message_label = Label(text="", size_hint_y=None, height=30)
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Attendance", size_hint_y=None, height=50)
        save_btn.bind(on_press=self.save_attendance)
        self.layout.add_widget(save_btn)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        batches = get_all_batches()
        self.batch_name_to_id = {batch[1]: batch[0] for batch in batches}
        self.batch_spinner.values = list(self.batch_name_to_id.keys())
        self.message_label.text = ""

    def load_students_for_batch(self, instance):
        selected_batch_name = self.batch_spinner.text
        if selected_batch_name not in self.batch_name_to_id:
            self.message_label.text = "Please select a valid batch first!"
            return

        self.selected_batch_id = self.batch_name_to_id[selected_batch_name]
        selected_date = self.date_input.text.strip()

        students = get_students_by_batch(self.selected_batch_id)
        existing_attendance = get_attendance_for_batch_on_date(self.selected_batch_id, selected_date)

        self.students_grid.clear_widgets()
        self.attendance_status = {}
        self.status_buttons = {}

        if not students:
            self.students_grid.add_widget(Label(text="No students in this batch.", size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            return

        for student in students:
            student_id = student[0]
            student_name = student[1]

            self.students_grid.add_widget(Label(text=student_name, size_hint_y=None, height=40))

            current_status = existing_attendance.get(student_id, "Present")
            self.attendance_status[student_id] = current_status

            status_btn = Button(text=current_status, size_hint_y=None, height=40)
            status_btn.bind(on_press=lambda instance, sid=student_id: self.toggle_status(sid))
            self.status_buttons[student_id] = status_btn
            self.students_grid.add_widget(status_btn)

        self.message_label.text = f"Loaded {len(students)} student(s). Tap a status to toggle."

    def toggle_status(self, student_id):
        current = self.attendance_status[student_id]
        new_status = "Absent" if current == "Present" else "Present"
        self.attendance_status[student_id] = new_status
        self.status_buttons[student_id].text = new_status

    def save_attendance(self, instance):
        if not self.selected_batch_id or not self.attendance_status:
            self.message_label.text = "Load a batch's students first!"
            return

        selected_date = self.date_input.text.strip()
        for student_id, status in self.attendance_status.items():
            mark_attendance(student_id, self.selected_batch_id, selected_date, status)

        self.message_label.text = f"Attendance saved for {selected_date}!"

    def go_back(self, instance):
        self.manager.current = "home"

class AttendanceHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_label = Label(text="Attendance History for: ", size_hint_y=None, height=40)
        self.layout.add_widget(self.student_label)

        self.percentage_label = Label(text="", size_hint_y=None, height=40, bold=True)
        self.layout.add_widget(self.percentage_label)

        self.history_grid = GridLayout(cols=2, size_hint_y=None, spacing=5, padding=5)
        self.history_grid.bind(minimum_height=self.history_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.history_grid)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to View Students", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_history(self, student_id):
        student = get_student_by_id(student_id)
        _, name, student_class, joining_date, contact, status, batch_id = student
        self.student_label.text = f"Attendance History for: {name} ({student_class})"

        percentage = get_attendance_percentage(student_id)
        self.percentage_label.text = f"Overall Attendance: {percentage}%"

        self.history_grid.clear_widgets()
        self.history_grid.add_widget(Label(text="Date", bold=True, size_hint_y=None, height=40))
        self.history_grid.add_widget(Label(text="Status", bold=True, size_hint_y=None, height=40))

        history = get_attendance_history(student_id)
        if not history:
            self.history_grid.add_widget(Label(text="No records yet.", size_hint_y=None, height=40))
            self.history_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            return

        for record_date, record_status in history:
            self.history_grid.add_widget(Label(text=record_date, size_hint_y=None, height=40))
            self.history_grid.add_widget(Label(text=record_status, size_hint_y=None, height=40))

    def go_back(self, instance):
        self.manager.current = "view_students"

class AddFeeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_name_to_id = {}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_spinner = Spinner(text="Select a Student", values=[])
        self.layout.add_widget(self.student_spinner)

        self.description_input = TextInput(hint_text="Description (e.g. July 2026 Tuition)", multiline=False)
        self.layout.add_widget(self.description_input)

        self.amount_input = TextInput(hint_text="Amount Due", multiline=False, input_filter="float")
        self.layout.add_widget(self.amount_input)

        self.due_date_input = TextInput(hint_text="Due Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.due_date_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Fee Record")
        save_btn.bind(on_press=self.save_fee)
        self.layout.add_widget(save_btn)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        students = get_all_students()
        self.student_name_to_id = {student[1]: student[0] for student in students}
        self.student_spinner.values = list(self.student_name_to_id.keys())
        self.message_label.text = ""

    def save_fee(self, instance):
        selected_student_name = self.student_spinner.text
        description = self.description_input.text.strip()
        amount_text = self.amount_input.text.strip()
        due_date = self.due_date_input.text.strip()

        if selected_student_name not in self.student_name_to_id:
            self.message_label.text = "Please select a valid student!"
            return

        if not description or not amount_text or not due_date:
            self.message_label.text = "All fields are required!"
            return

        student_id = self.student_name_to_id[selected_student_name]
        amount_due = float(amount_text)

        add_fee_record(student_id, description, amount_due, due_date)
        self.message_label.text = f"Fee record saved for {selected_student_name}"

        self.description_input.text = ""
        self.amount_input.text = ""
        self.due_date_input.text = ""

    def go_back(self, instance):
        self.manager.current = "home"

class ViewFeesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_name_to_id = {}
        self.selected_student_id = None
        self.fee_id_for_payment = None

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_spinner = Spinner(text="Select a Student", values=[], size_hint_y=None, height=50)
        self.layout.add_widget(self.student_spinner)

        load_btn = Button(text="Load Fees", size_hint_y=None, height=50)
        load_btn.bind(on_press=self.load_fees)
        self.layout.add_widget(load_btn)

        self.pending_label = Label(text="", size_hint_y=None, height=40, bold=True)
        self.layout.add_widget(self.pending_label)

        self.fees_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.fees_list.bind(minimum_height=self.fees_list.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.fees_list)
        self.layout.add_widget(scroll)

        payment_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)
        self.payment_amount_input = TextInput(hint_text="Payment Amount", multiline=False, input_filter="float")
        payment_row.add_widget(self.payment_amount_input)
        record_payment_btn = Button(text="Record Payment")
        record_payment_btn.bind(on_press=self.record_payment_action)
        payment_row.add_widget(record_payment_btn)
        self.layout.add_widget(payment_row)

        self.message_label = Label(text="", size_hint_y=None, height=30)
        self.layout.add_widget(self.message_label)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        students = get_all_students()
        self.student_name_to_id = {student[1]: student[0] for student in students}
        self.student_spinner.values = list(self.student_name_to_id.keys())

    def load_fees(self, instance):
        selected_student_name = self.student_spinner.text
        if selected_student_name not in self.student_name_to_id:
            self.message_label.text = "Please select a valid student first!"
            return

        self.selected_student_id = self.student_name_to_id[selected_student_name]
        fees = get_fees_for_student(self.selected_student_id)

        self.fees_list.clear_widgets()

        for fee_id, description, amount_due, amount_paid, due_date in fees:
            pending = amount_due - amount_paid

            card = BoxLayout(orientation="vertical", size_hint_y=None, height=140, padding=10, spacing=4)
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(0.15, 0.15, 0.2, 1)
                card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
            card.bind(pos=lambda inst, val: setattr(inst.bg_rect, 'pos', val))
            card.bind(size=lambda inst, val: setattr(inst.bg_rect, 'size', val))

            card.add_widget(Label(text=f"[b]{description}[/b]", markup=True, font_size=20, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"Due: ₹{amount_due}  |  Paid: ₹{amount_paid}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Pending: ₹{pending}  |  Due Date: {due_date}", size_hint_y=None, height=25))

            self.fees_list.add_widget(card)

            if pending > 0:
                self.fee_id_for_payment = fee_id

        total_pending = get_total_pending_dues(self.selected_student_id)
        self.pending_label.text = f"Total Pending Dues: {total_pending}"
        self.message_label.text = "Payments apply to the oldest unpaid fee record."

    def record_payment_action(self, instance):
        if not self.selected_student_id:
            self.message_label.text = "Load a student's fees first!"
            return

        payment_text = self.payment_amount_input.text.strip()
        if not payment_text:
            self.message_label.text = "Enter a payment amount!"
            return

        if not self.fee_id_for_payment:
            self.message_label.text = "No pending fee record to apply payment to!"
            return

        payment_amount = float(payment_text)
        record_payment(self.fee_id_for_payment, payment_amount)
        self.payment_amount_input.text = ""
        self.message_label.text = "Payment recorded!"
        self.load_fees(None)

    def go_back(self, instance):
        self.manager.current = "home"


class ViewBatchesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.batches_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.batches_list.bind(minimum_height=self.batches_list.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.batches_list)
        self.layout.add_widget(scroll)

        back_btn = styled_button("Back to Home", color=ACCENT_COLOR, size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_batches()

    def load_batches(self):
        self.batches_list.clear_widgets()

        batches = get_all_batches()
        for batch_id, batch_name, subject, schedule in batches:
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=140, padding=10, spacing=4)
            add_card_background(card)

            card.add_widget(Label(text=f"[b]{batch_name}[/b]", markup=True, font_size=20, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"Subject: {subject}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Schedule: {schedule}", size_hint_y=None, height=25))

            delete_btn = styled_button("Delete", color=ACCENT_COLOR, size_hint_y=None, height=45)
            delete_btn.bind(on_press=lambda instance, bid=batch_id: self.delete_batch_action(bid))
            card.add_widget(delete_btn)

            self.batches_list.add_widget(card)

    def delete_batch_action(self, batch_id):
        delete_batch(batch_id)
        self.load_batches()

    def go_back(self, instance):
        self.manager.current = "home"

class AddExpenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.description_input = TextInput(hint_text="Description (e.g. Rent, Stationery)", multiline=False)
        self.layout.add_widget(self.description_input)

        self.amount_input = TextInput(hint_text="Amount", multiline=False, input_filter="float")
        self.layout.add_widget(self.amount_input)

        self.date_input = TextInput(text=str(date.today()), hint_text="Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.date_input)

        self.category_input = TextInput(hint_text="Category (e.g. Rent, Utilities, Supplies)", multiline=False)
        self.layout.add_widget(self.category_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Expense")
        save_btn.bind(on_press=self.save_expense)
        self.layout.add_widget(save_btn)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def save_expense(self, instance):
        description = self.description_input.text.strip()
        amount_text = self.amount_input.text.strip()
        expense_date = self.date_input.text.strip()
        category = self.category_input.text.strip()

        if not description or not amount_text or not category:
            self.message_label.text = "All fields are required!"
            return

        add_expense(description, float(amount_text), expense_date, category)
        self.message_label.text = f"Saved: {description}"

        self.description_input.text = ""
        self.amount_input.text = ""
        self.category_input.text = ""

    def go_back(self, instance):
        self.manager.current = "home"

class ViewExpensesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.summary_label = Label(text="", size_hint_y=None, height=40, bold=True)
        self.layout.add_widget(self.summary_label)

        self.expenses_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.expenses_list.bind(minimum_height=self.expenses_list.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.expenses_list)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_expenses()

    def load_expenses(self):
        self.expenses_list.clear_widgets()

        expenses = get_all_expenses()
        for expense_id, description, amount, expense_date, category in expenses:
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=160, padding=10, spacing=4)
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(0.15, 0.15, 0.2, 1)
                card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
            card.bind(pos=lambda inst, val: setattr(inst.bg_rect, 'pos', val))
            card.bind(size=lambda inst, val: setattr(inst.bg_rect, 'size', val))

            card.add_widget(Label(text=f"[b]{description}[/b]", markup=True, font_size=20, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"Amount: ₹{amount}  |  Category: {category}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Date: {expense_date}", size_hint_y=None, height=25))

            delete_btn = Button(text="Delete", size_hint_y=None, height=45)
            delete_btn.bind(on_press=lambda instance, eid=expense_id: self.delete_expense_action(eid))
            card.add_widget(delete_btn)

            self.expenses_list.add_widget(card)

        total_expenses = get_total_expenses()
        total_fees = get_total_fees_collected()
        profit = round(total_fees - total_expenses, 2)
        self.summary_label.text = f"Fees: ₹{total_fees}  |  Expenses: ₹{total_expenses}  |  Profit: ₹{profit}"

    def delete_expense_action(self, expense_id):
        delete_expense(expense_id)
        self.load_expenses()

    def go_back(self, instance):
        self.manager.current = "home"

class ViewStudentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.students_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.students_list.bind(minimum_height=self.students_list.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.students_list)
        self.layout.add_widget(scroll)

        refresh_btn = styled_button(text="Refresh List", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.load_students)
        self.layout.add_widget(refresh_btn)

        back_btn = styled_button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_students()

    def load_students(self, instance=None):
        self.students_list.clear_widgets()

        students = get_all_students()
        for student in students:
            student_id, name, student_class, joining_date, contact, status, batch_id = student
            batch_name = get_batch_name(batch_id)

            card = BoxLayout(orientation="vertical", size_hint_y=None, height=220, padding=10, spacing=4)
            add_card_background(card)

            card.add_widget(Label(text=f"[b]{name}[/b]", markup=True, font_size=20, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"Class: {student_class}  |  Batch: {batch_name}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Joined: {joining_date}  |  Status: {status}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Contact: {contact}", size_hint_y=None, height=25))

            button_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, spacing=5)

            edit_btn = styled_button("Edit", color=ACCENT_COLOR)
            edit_btn.bind(on_press=lambda instance, sid=student_id: self.edit_student(sid))
            button_row.add_widget(edit_btn)

            assign_btn = styled_button("Batch", color=ACCENT_COLOR)
            assign_btn.bind(on_press=lambda instance, sid=student_id: self.assign_batch(sid))
            button_row.add_widget(assign_btn)

            history_btn = styled_button("History", color=ACCENT_COLOR)
            history_btn.bind(on_press=lambda instance, sid=student_id: self.view_history(sid))
            button_row.add_widget(history_btn)

            progress_btn = styled_button("Progress", color=ACCENT_COLOR)
            progress_btn.bind(on_press=lambda instance, sid=student_id: self.view_progress(sid))
            button_row.add_widget(progress_btn)

            delete_btn = styled_button("Delete", color=ACCENT_COLOR)
            delete_btn.bind(on_press=lambda instance, sid=student_id: self.confirm_delete(sid))
            button_row.add_widget(delete_btn)

            card.add_widget(button_row)
            self.students_list.add_widget(card)

    def edit_student(self, student_id):
        edit_screen = self.manager.get_screen("edit_student")
        edit_screen.load_student(student_id)
        self.manager.current = "edit_student"

    def confirm_delete(self, student_id):
        delete_student(student_id)
        self.load_students()

    def go_back(self, instance):
        self.manager.current = "home"

    def assign_batch(self, student_id):
        assign_screen = self.manager.get_screen("assign_batch")
        assign_screen.load_student_for_assignment(student_id)
        self.manager.current = "assign_batch"

    def view_history(self, student_id):
        history_screen = self.manager.get_screen("attendance_history")
        history_screen.load_history(student_id)
        self.manager.current = "attendance_history"

    def view_progress(self, student_id):
        progress_screen = self.manager.get_screen("student_progress")
        progress_screen.load_progress(student_id)
        self.manager.current = "student_progress"

class MonthlyReportScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_name_to_id = {}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_spinner = Spinner(text="Select a Student", values=[])
        self.layout.add_widget(self.student_spinner)

        load_btn = Button(text="Generate Report", size_hint_y=None, height=50)
        load_btn.bind(on_press=self.generate_report)
        self.layout.add_widget(load_btn)

        self.report_grid = GridLayout(cols=2, size_hint_y=None, spacing=8, padding=10)
        self.report_grid.bind(minimum_height=self.report_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.report_grid)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        students = get_all_students()
        self.student_name_to_id = {student[1]: student[0] for student in students}
        self.student_spinner.values = list(self.student_name_to_id.keys())

    def generate_report(self, instance):
        selected_name = self.student_spinner.text
        if selected_name not in self.student_name_to_id:
            return

        student_id = self.student_name_to_id[selected_name]
        student = get_student_by_id(student_id)
        _, name, student_class, joining_date, contact, status, batch_id = student
        batch_name = get_batch_name(batch_id)

        attendance_pct = get_attendance_percentage(student_id)
        total_pending = get_total_pending_dues(student_id)
        avg_marks_pct = get_average_marks_percentage(student_id)

        self.report_grid.clear_widgets()

        rows = [
            ("Name", name),
            ("Class", student_class),
            ("Batch", batch_name),
            ("Status", status),
            ("Attendance %", f"{attendance_pct}%"),
            ("Pending Dues", f"₹{total_pending}"),
            ("Average Exam Score", f"{avg_marks_pct}%"),
        ]

        for label_text, value_text in rows:
            self.report_grid.add_widget(Label(text=label_text, bold=True, size_hint_y=None, height=40))
            self.report_grid.add_widget(Label(text=value_text, size_hint_y=None, height=40))

    def go_back(self, instance):
        self.manager.current = "home"

class AddExamScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batch_name_to_id = {}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.exam_name_input = TextInput(hint_text="Exam Name (e.g. Unit Test 1)", multiline=False)
        self.layout.add_widget(self.exam_name_input)

        self.subject_input = TextInput(hint_text="Subject", multiline=False)
        self.layout.add_widget(self.subject_input)

        self.batch_spinner = Spinner(text="Select a Batch", values=[])
        self.layout.add_widget(self.batch_spinner)

        self.date_input = TextInput(text=str(date.today()), hint_text="Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.date_input)

        self.max_marks_input = TextInput(hint_text="Max Marks (e.g. 100)", multiline=False, input_filter="float")
        self.layout.add_widget(self.max_marks_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Exam")
        save_btn.bind(on_press=self.save_exam)
        self.layout.add_widget(save_btn)

        back_btn = Button(text="Back to Home")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        batches = get_all_batches()
        self.batch_name_to_id = {batch[1]: batch[0] for batch in batches}
        self.batch_spinner.values = list(self.batch_name_to_id.keys())
        self.message_label.text = ""

    def save_exam(self, instance):
        exam_name = self.exam_name_input.text.strip()
        subject = self.subject_input.text.strip()
        selected_batch_name = self.batch_spinner.text
        exam_date = self.date_input.text.strip()
        max_marks_text = self.max_marks_input.text.strip()

        if selected_batch_name not in self.batch_name_to_id:
            self.message_label.text = "Please select a valid batch!"
            return

        if not exam_name or not subject or not max_marks_text:
            self.message_label.text = "All fields are required!"
            return

        batch_id = self.batch_name_to_id[selected_batch_name]
        max_marks = float(max_marks_text)

        add_exam(exam_name, subject, batch_id, exam_date, max_marks)
        self.message_label.text = f"Exam saved: {exam_name}"

        self.exam_name_input.text = ""
        self.subject_input.text = ""
        self.max_marks_input.text = ""

    def go_back(self, instance):
        self.manager.current = "home"

class TimetableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.timetable_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10, padding=10)
        self.timetable_list.bind(minimum_height=self.timetable_list.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.timetable_list)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_timetable()

    def load_timetable(self):
        self.timetable_list.clear_widgets()

        batches = get_all_batches()
        for batch_id, batch_name, subject, schedule in batches:
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=110, padding=10, spacing=4)
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(0.15, 0.15, 0.2, 1)
                card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
            card.bind(pos=lambda inst, val: setattr(inst.bg_rect, 'pos', val))
            card.bind(size=lambda inst, val: setattr(inst.bg_rect, 'size', val))

            card.add_widget(Label(text=f"[b]{batch_name}[/b]", markup=True, font_size=20, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"Subject: {subject}", size_hint_y=None, height=25))
            card.add_widget(Label(text=f"Schedule: {schedule}", size_hint_y=None, height=25))

            self.timetable_list.add_widget(card)

    def go_back(self, instance):
        self.manager.current = "home"

class RecordMarksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exam_display_to_id = {}
        self.selected_exam_id = None
        self.marks_inputs = {}  # {student_id: TextInput}

        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.exam_spinner = Spinner(text="Select an Exam", values=[])
        self.layout.add_widget(self.exam_spinner)

        load_btn = Button(text="Load Students", size_hint_y=None, height=50)
        load_btn.bind(on_press=self.load_students_for_exam)
        self.layout.add_widget(load_btn)

        self.marks_grid = GridLayout(cols=2, size_hint_y=None, spacing=5, padding=5)
        self.marks_grid.bind(minimum_height=self.marks_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.marks_grid)
        self.layout.add_widget(scroll)

        self.message_label = Label(text="", size_hint_y=None, height=30)
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save All Marks", size_hint_y=None, height=50)
        save_btn.bind(on_press=self.save_all_marks)
        self.layout.add_widget(save_btn)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        exams = get_all_exams()
        self.exam_display_to_id = {}
        for exam in exams:
            exam_id, exam_name, subject, batch_id, exam_date, max_marks = exam
            display = f"{exam_name} - {subject} ({exam_date})"
            self.exam_display_to_id[display] = (exam_id, batch_id)
        self.exam_spinner.values = list(self.exam_display_to_id.keys())
        self.message_label.text = ""

    def load_students_for_exam(self, instance):
        selected_display = self.exam_spinner.text
        if selected_display not in self.exam_display_to_id:
            self.message_label.text = "Please select a valid exam first!"
            return

        exam_id, batch_id = self.exam_display_to_id[selected_display]
        self.selected_exam_id = exam_id

        students = get_students_by_batch(batch_id)
        existing_marks = get_marks_for_exam(exam_id)

        self.marks_grid.clear_widgets()
        self.marks_inputs = {}

        if not students:
            self.marks_grid.add_widget(Label(text="No students in this batch.", size_hint_y=None, height=40))
            self.marks_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            return

        for student in students:
            student_id = student[0]
            student_name = student[1]

            self.marks_grid.add_widget(Label(text=student_name, size_hint_y=None, height=40))

            marks_input = TextInput(
                text=str(existing_marks.get(student_id, "")),
                multiline=False,
                input_filter="float",
                size_hint_y=None,
                height=40
            )
            self.marks_inputs[student_id] = marks_input
            self.marks_grid.add_widget(marks_input)

        self.message_label.text = f"Loaded {len(students)} student(s). Enter marks and save."

    def save_all_marks(self, instance):
        if not self.selected_exam_id or not self.marks_inputs:
            self.message_label.text = "Load an exam's students first!"
            return

        saved_count = 0
        for student_id, marks_input in self.marks_inputs.items():
            marks_text = marks_input.text.strip()
            if marks_text:
                record_marks(self.selected_exam_id, student_id, float(marks_text))
                saved_count += 1

        self.message_label.text = f"Saved marks for {saved_count} student(s)!"

    def go_back(self, instance):
        self.manager.current = "home"

class StudentProgressScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.student_label = Label(text="Progress for: ", size_hint_y=None, height=40)
        self.layout.add_widget(self.student_label)

        self.progress_grid = GridLayout(cols=4, size_hint_y=None, spacing=5, padding=5)
        self.progress_grid.bind(minimum_height=self.progress_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.progress_grid)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to View Students", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_progress(self, student_id):
        student = get_student_by_id(student_id)
        _, name, student_class, joining_date, contact, status, batch_id = student
        self.student_label.text = f"Progress for: {name} ({student_class})"

        self.progress_grid.clear_widgets()
        for header in ["Exam", "Subject", "Date", "Marks"]:
            self.progress_grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height=40))

        progress = get_progress_for_student(student_id)
        if not progress:
            self.progress_grid.add_widget(Label(text="No exam records yet.", size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text="", size_hint_y=None, height=40))
            return

        for exam_name, subject, exam_date, marks_obtained, max_marks in progress:
            self.progress_grid.add_widget(Label(text=exam_name, size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text=subject, size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text=exam_date, size_hint_y=None, height=40))
            self.progress_grid.add_widget(Label(text=f"{marks_obtained}/{max_marks}", size_hint_y=None, height=40))

    def go_back(self, instance):
        self.manager.current = "view_students"


class ZeroToInfinityApp(App):
    def build(self):
        self.title = "Zero To Infinity"
        init_db()
        init_batches_table()
        add_batch_id_column()
        init_attendance_table()
        init_fees_table()
        init_exams_table()
        init_expenses_table()
        init_marks_table()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddStudentScreen(name="add_student"))
        sm.add_widget(ViewStudentsScreen(name="view_students"))
        sm.add_widget(EditStudentScreen(name="edit_student"))
        sm.add_widget(AddBatchScreen(name="add_batch"))
        sm.add_widget(ViewBatchesScreen(name="view_batches"))
        sm.add_widget(AssignBatchScreen(name="assign_batch"))
        sm.add_widget(TakeAttendanceScreen(name="take_attendance"))
        sm.add_widget(AttendanceHistoryScreen(name="attendance_history"))
        sm.add_widget(AddFeeScreen(name="add_fee"))
        sm.add_widget(ViewFeesScreen(name="view_fees"))
        sm.add_widget(AddExamScreen(name="add_exam"))
        sm.add_widget(RecordMarksScreen(name="record_marks"))
        sm.add_widget(StudentProgressScreen(name="student_progress"))
        sm.add_widget(MonthlyReportScreen(name="monthly_report"))
        sm.add_widget(AddExpenseScreen(name="add_expense"))
        sm.add_widget(ViewExpensesScreen(name="view_expenses"))
        sm.add_widget(TimetableScreen(name="timetable"))

        return sm


if __name__ == "__main__":
    ZeroToInfinityApp().run()
    