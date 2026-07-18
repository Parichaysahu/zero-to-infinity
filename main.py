from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
Window.size = (1500, 800)
from kivy.uix.gridlayout import GridLayout
from database import (
    init_db, add_student, get_all_students, get_student_by_id, update_student, delete_student,
    init_batches_table, add_batch, get_all_batches, delete_batch,
    add_batch_id_column, assign_student_to_batch, get_students_by_batch, get_batch_name
)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        title = Label(text="Zero To Infinity", font_size=28)
        layout.add_widget(title)

        add_student_btn = Button(text="Add Student")
        add_student_btn.bind(on_press=self.go_to_add_student)
        layout.add_widget(add_student_btn)

        view_students_btn = Button(text="View Students")
        view_students_btn.bind(on_press=self.go_to_view_students)
        layout.add_widget(view_students_btn)

        add_batch_btn = Button(text="Add Batch")
        add_batch_btn.bind(on_press=self.go_to_add_batch)
        layout.add_widget(add_batch_btn)

        view_batches_btn = Button(text="View Batches")
        view_batches_btn.bind(on_press=self.go_to_view_batches)
        layout.add_widget(view_batches_btn)

        self.add_widget(layout)

    def go_to_add_student(self, instance):
        self.manager.current = "add_student"

    def go_to_view_students(self, instance):
        self.manager.current = "view_students"

    def go_to_add_batch(self, instance):
        self.manager.current = "add_batch"

    def go_to_view_batches(self, instance):
        self.manager.current = "view_batches"


class AddStudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.name_input = TextInput(hint_text="Student Name", multiline=False)
        self.layout.add_widget(self.name_input)

        self.class_input = TextInput(hint_text="Class (e.g. 10th)", multiline=False)
        self.layout.add_widget(self.class_input)

        self.joining_date_input = TextInput(hint_text="Joining Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.joining_date_input)

        self.contact_input = TextInput(hint_text="Contact Number", multiline=False)
        self.layout.add_widget(self.contact_input)

        self.status_input = TextInput(hint_text="Enrollment Status (Active/Inactive)", multiline=False)
        self.layout.add_widget(self.status_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Student")
        save_btn.bind(on_press=self.save_student)
        self.layout.add_widget(save_btn)

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

        self.name_input = TextInput(hint_text="Student Name", multiline=False)
        self.layout.add_widget(self.name_input)

        self.class_input = TextInput(hint_text="Class (e.g. 10th)", multiline=False)
        self.layout.add_widget(self.class_input)

        self.joining_date_input = TextInput(hint_text="Joining Date (YYYY-MM-DD)", multiline=False)
        self.layout.add_widget(self.joining_date_input)

        self.contact_input = TextInput(hint_text="Contact Number", multiline=False)
        self.layout.add_widget(self.contact_input)

        self.status_input = TextInput(hint_text="Enrollment Status (Active/Inactive)", multiline=False)
        self.layout.add_widget(self.status_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        update_btn = Button(text="Update Student")
        update_btn.bind(on_press=self.update_student_action)
        self.layout.add_widget(update_btn)

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

        self.batch_name_input = TextInput(hint_text="Batch Name (e.g. Class 10 Physics Evening)", multiline=False)
        self.layout.add_widget(self.batch_name_input)

        self.subject_input = TextInput(hint_text="Subject", multiline=False)
        self.layout.add_widget(self.subject_input)

        self.schedule_input = TextInput(hint_text="Schedule (e.g. Mon-Wed-Fri 5-6 PM)", multiline=False)
        self.layout.add_widget(self.schedule_input)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

        save_btn = Button(text="Save Batch")
        save_btn.bind(on_press=self.save_batch)
        self.layout.add_widget(save_btn)

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

        self.student_label = Label(text="Assign Batch for: ")
        self.layout.add_widget(self.student_label)

        self.batch_spinner = Spinner(text="Select a Batch", values=[])
        self.layout.add_widget(self.batch_spinner)

        self.message_label = Label(text="")
        self.layout.add_widget(self.message_label)

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


class ViewBatchesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.batches_grid = GridLayout(
            cols=4,
            size_hint_y=None,
            spacing=5,
            padding=5,
            cols_minimum={
                0: 200,  # Batch Name
                1: 130,  # Subject
                2: 200,  # Schedule
                3: 80,   # Delete
            }
        )
        self.batches_grid.bind(minimum_height=self.batches_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.batches_grid)
        self.layout.add_widget(scroll)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_batches()

    def load_batches(self):
        self.batches_grid.clear_widgets()

        for header in ["Batch Name", "Subject", "Schedule", ""]:
            self.batches_grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height=40))

        batches = get_all_batches()
        for batch in batches:
            batch_id, batch_name, subject, schedule = batch

            self.batches_grid.add_widget(Label(text=batch_name, size_hint_y=None, height=40))
            self.batches_grid.add_widget(Label(text=subject, size_hint_y=None, height=40))
            self.batches_grid.add_widget(Label(text=schedule, size_hint_y=None, height=40))

            delete_btn = Button(text="Delete", size_hint_y=None, height=40)
            delete_btn.bind(on_press=lambda instance, bid=batch_id: self.delete_batch_action(bid))
            self.batches_grid.add_widget(delete_btn)

    def delete_batch_action(self, batch_id):
        delete_batch(batch_id)
        self.load_batches()

    def go_back(self, instance):
        self.manager.current = "home"

class ViewStudentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        self.students_grid = GridLayout(
            cols=9,
            size_hint_y=None,
            spacing=5,
            padding=5,
            cols_minimum={
                0: 150,  # Name
                1: 80,   # Class
                2: 110,  # Joining Date
                3: 130,  # Contact
                4: 90,   # Status
                5: 100,  # Batch
                6: 70,   # Edit
                7: 130,  # Assign Batch
                8: 80,   # Delete
            }
        )
        self.students_grid.bind(minimum_height=self.students_grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.students_grid)
        self.layout.add_widget(scroll)

        refresh_btn = Button(text="Refresh List", size_hint_y=None, height=50)
        refresh_btn.bind(on_press=self.load_students)
        self.layout.add_widget(refresh_btn)

        back_btn = Button(text="Back to Home", size_hint_y=None, height=50)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_students()

    def load_students(self, instance=None):
        self.students_grid.clear_widgets()

        for header in ["Name", "Class", "Joining Date", "Contact", "Status", "Batch", "", "", ""]:
            self.students_grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height=40))

        students = get_all_students()
        for student in students:
            student_id, name, student_class, joining_date, contact, status, batch_id = student
            batch_name = get_batch_name(batch_id)

            self.students_grid.add_widget(Label(text=name, size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text=student_class, size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text=joining_date, size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text=contact, size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text=status, size_hint_y=None, height=40))
            self.students_grid.add_widget(Label(text=batch_name, size_hint_y=None, height=40))

            edit_btn = Button(text="Edit", size_hint_y=None, height=40)
            edit_btn.bind(on_press=lambda instance, sid=student_id: self.edit_student(sid))
            self.students_grid.add_widget(edit_btn)

            assign_btn = Button(text="Assign Batch", size_hint_y=None, height=40)
            assign_btn.bind(on_press=lambda instance, sid=student_id: self.assign_batch(sid))
            self.students_grid.add_widget(assign_btn)

            delete_btn = Button(text="Delete", size_hint_y=None, height=40)
            delete_btn.bind(on_press=lambda instance, sid=student_id: self.confirm_delete(sid))
            self.students_grid.add_widget(delete_btn)

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


class ZeroToInfinityApp(App):
    def build(self):
        self.title = "Zero To Infinity"
        init_db()
        init_batches_table()
        add_batch_id_column()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddStudentScreen(name="add_student"))
        sm.add_widget(ViewStudentsScreen(name="view_students"))
        sm.add_widget(EditStudentScreen(name="edit_student"))
        sm.add_widget(AddBatchScreen(name="add_batch"))
        sm.add_widget(ViewBatchesScreen(name="view_batches"))
        sm.add_widget(AssignBatchScreen(name="assign_batch"))

        return sm


if __name__ == "__main__":
    ZeroToInfinityApp().run()
    