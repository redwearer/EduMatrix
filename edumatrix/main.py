#!/usr/bin/python3
"""
This file contains the main application code for the EduMatrix application.
"""

import sys

from edumatrix.controllers import (
    CourseController,
    ProfessorController,
    StudentController,
)
from edumatrix.database import DatabaseManager

from PyQt5.QtCore import Qt, QDate

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QSplitter,
    QHeaderView,
    QDateEdit,
)


class LoginDialog(QDialog):
    """_summary_

    Parameters
    ----------
    QDialog : PyQt5.QtWidgets.QDialog
        A PyQt5 QDialog object.
    """

    def __init__(self):
        """
        Initialize the LoginDialog class.

        This class represents a dialog window for user login. It sets up the UI elements
        such as labels, input fields, and buttons. It also connects the login button
        to the check_credentials method.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()

        username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def check_credentials(self):
        """
        Check the entered username and password against the expected values.

        If the username and password match the expected values ("admin" and "admin" respectively),
        the method accepts the credentials. Otherwise, it displays an error message.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        if (
            self.username_input.text() == "admin"
            and self.password_input.text() == "admin"
        ):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Incorrect username or password.")


class EduMatrixApp(QMainWindow):
    """
    Main window for the EduMatrix application.

    Parameters
    ----------
    QMainWindow : PyQt5.QtWidgets.QMainWindow
        A PyQt5 QMainWindow object.
    """

    def __init__(
        self,
        student_controller: StudentController,
        professor_controller: ProfessorController,
        course_controller: CourseController,
    ):
        """
        Main window for the EduMatrix application.

        Parameters
        ----------
        student_controller : StudentController
            Controller for student operations.
        professor_controller : ProfessorController
            Controller for professor operations.
        course_controller : CourseController
            Controller for course operations.
        """
        super().__init__()

        self.student_controller = student_controller
        self.professor_controller = professor_controller
        self.course_controller = course_controller

        self.student_courses_table = QTableWidget()

        self.currently_editing_student_id = None

        # Input fields for professor details
        self.professor_first_name_input = QLineEdit()
        self.professor_last_name_input = QLineEdit()
        self.professor_department_input = QLineEdit()
        self.professor_achievement_input = QLineEdit()

        # Input fields for student details
        self.student_first_name_input = QLineEdit()
        self.student_last_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_degree_input = QLineEdit()
        self.student_credits_input = QLineEdit()
        self.student_gpa_input = QLineEdit()

        # Table for displaying professors
        self.professors_table = QTableWidget()

        # Second table for displaying courses taught by the selected professor
        self.professor_courses_table = QTableWidget()

        self.currently_editing_professor_id = None

        # Input fields for course details
        self.course_name_input = QLineEdit()
        self.course_start_date_input = QDateEdit()
        self.course_start_date_input.setCalendarPopup(True)
        self.course_start_date_input.setDate(QDate.currentDate())
        self.course_end_date_input = QDateEdit()
        self.course_end_date_input.setCalendarPopup(True)
        self.course_end_date_input.setDate(QDate.currentDate())
        self.course_credits_input = QLineEdit()
        self.course_professor_id_input = QLineEdit()

        # Table for displaying courses
        self.courses_table = QTableWidget()

        # Second table for displaying students enrolled in the selected course
        self.course_students_table = QTableWidget()

        self.currently_editing_course_id = None

        self.setWindowTitle("EduMatrix University Management System")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Initialize the students_table
        self.students_table = QTableWidget()

        self.initialize_ui()

    def initialize_ui(self):
        """
        Initializes the user interface components.
        """
        # Create tabs
        self.tab_widget.addTab(self.create_students_tab(), "Students")
        self.tab_widget.addTab(self.create_professors_tab(), "Professors")
        self.tab_widget.addTab(self.create_courses_tab(), "Courses")

        # Update tables with existing data
        self.update_students_table()
        self.update_professors_table()
        self.update_courses_table()

    def create_students_tab(self):
        """
        Creates the Students tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Students tab.
        """
        student_tab = QWidget()
        layout = QVBoxLayout(student_tab)

        # Create the splitter and set orientation
        splitter = QSplitter(Qt.Vertical)

        # Buttons for operations
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_or_update_student)

        # Add Delete Student Button
        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete_student)

        # Table for displaying students
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(7)  # Set the number of columns
        self.students_table.setHorizontalHeaderLabels(
            ["ID", "First Name", "Last Name", "Age", "Degree", "Credits", "GPA"]
        )
        student_table_header = self.students_table.horizontalHeader()
        student_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )
        student_table_header.setSectionResizeMode(
            6, QHeaderView.ResizeMode.ResizeToContents
        )

        # Connect double-click event on the table to load_student_for_editing
        self.students_table.doubleClicked.connect(self.load_student_for_editing)

        # Layout setup
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("First Name:"))
        form_layout.addWidget(self.student_first_name_input)
        form_layout.addWidget(QLabel("Last Name:"))
        form_layout.addWidget(self.student_last_name_input)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.student_age_input)
        form_layout.addWidget(QLabel("Degree:"))
        form_layout.addWidget(self.student_degree_input)
        form_layout.addWidget(QLabel("Credits:"))
        form_layout.addWidget(self.student_credits_input)
        form_layout.addWidget(QLabel("GPA:"))
        form_layout.addWidget(self.student_gpa_input)
        form_layout.addWidget(add_button)
        form_layout.addWidget(delete_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.students_table)

        # Container widget for the second table and its label
        student_courses_container = QWidget()
        student_courses_layout = QVBoxLayout(student_courses_container)
        student_courses_label = QLabel("Courses Enrolled:")
        student_courses_layout.addWidget(student_courses_label)
        student_courses_layout.addWidget(self.student_courses_table)

        # Second table for displaying courses for the selected student
        self.student_courses_table.setColumnCount(
            5
        )  # For example, Course Name, Start Date, End Date
        self.student_courses_table.setHorizontalHeaderLabels(
            ["Course Name", "Start Date", "End Date", "Credit Hours", "Professor"]
        )
        student_courses_table_header = self.student_courses_table.horizontalHeader()
        student_courses_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        student_courses_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        student_courses_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        student_courses_table_header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        student_courses_table_header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )

        # Layout setup
        # layout.addWidget(self.students_table)
        # layout.addWidget(QLabel("Courses Enrolled:"))  # Label for the second table
        # layout.addWidget(self.student_courses_table)

        # Connect row selection to update the courses table
        self.students_table.selectionModel().selectionChanged.connect(
            self.on_student_selected
        )
        splitter.addWidget(self.students_table)
        splitter.addWidget(student_courses_container)

        # Set the splitter as the central widget
        layout.addWidget(splitter)

        student_tab.setLayout(layout)
        return student_tab

    def update_students_table(self):
        """
        Updates the students table with the latest data from the database.
        """
        # Fetch all students from the database
        students = self.student_controller.list_all_students()

        # Set the number of rows in the table
        self.students_table.setRowCount(len(students))

        # Populate the table with student data
        for row, student in enumerate(students):
            self.students_table.setItem(
                row, 0, QTableWidgetItem(str(student.student_id))
            )
            self.students_table.setItem(row, 1, QTableWidgetItem(student.first_name))
            self.students_table.setItem(row, 2, QTableWidgetItem(student.last_name))
            self.students_table.setItem(row, 3, QTableWidgetItem(str(student.age)))
            self.students_table.setItem(
                row, 4, QTableWidgetItem(student.degree_program)
            )
            self.students_table.setItem(
                row, 5, QTableWidgetItem(str(student.completed_credits))
            )
            self.students_table.setItem(row, 6, QTableWidgetItem(str(student.gpa)))

    def add_or_update_student(self):
        """
        Adds a new student record to the database and updates the table.
        """
        # Collect data from input fields
        first_name = self.student_first_name_input.text().strip()
        last_name = self.student_last_name_input.text().strip()
        try:
            age = int(self.student_age_input.text().strip())
            completed_credits = int(self.student_credits_input.text().strip())
            gpa = float(self.student_gpa_input.text().strip())
        except ValueError:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid numbers for age, credits, and GPA.",
            )
            return

        degree_program = self.student_degree_input.text().strip()

        # Validate input data
        if (
            not all([first_name, last_name, degree_program])
            or age <= 0
            or completed_credits < 0
            or not 0 <= gpa <= 4.0
        ):
            QMessageBox.warning(
                self, "Input Error", "Please enter valid data for all fields."
            )
            return

        if hasattr(self, "currently_editing_student_id"):
            # Update existing student
            self.student_controller.update_student(
                self.currently_editing_student_id,
                first_name,
                last_name,
                age,
                degree_program,
                completed_credits,
                gpa,
            )
            QMessageBox.information(self, "Success", "Student updated successfully.")
            del self.currently_editing_student_id  # Clear the editing flag
        else:
            # Add new student
            self.student_controller.add_student(
                first_name, last_name, age, degree_program, completed_credits, gpa
            )
            QMessageBox.information(self, "Success", "Student added successfully.")

        # Update the students_table with new data and clear input fields
        self.update_students_table()
        self.clear_student_input_fields()

    def delete_student(self):
        """
        Deletes the selected student record from the database and updates the table.
        """
        selected_items = self.students_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Selection Error", "Please select a student to delete."
            )
            return

        # Assuming the first column in the table contains the student ID
        student_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this student?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.student_controller.delete_student(student_id)
            self.update_students_table()
            QMessageBox.information(self, "Success", "Student deleted successfully.")

    def clear_student_input_fields(self):
        """
        Clears all input fields in the student tab.
        """
        self.student_first_name_input.clear()
        self.student_last_name_input.clear()
        self.student_age_input.clear()
        self.student_degree_input.clear()
        self.student_credits_input.clear()
        self.student_gpa_input.clear()

    def load_student_for_editing(self, index):
        """
        Loads the selected student's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        # Fetch the student ID from the table
        student_id = self.students_table.item(
            index.row(), 0
        ).text()
        # Assuming student ID is in the first column
        self.currently_editing_student_id = int(student_id)

        # Load the student data into the input fields
        student = self.student_controller.get_student(self.currently_editing_student_id)
        if student:
            self.student_first_name_input.setText(student.first_name)
            self.student_last_name_input.setText(student.last_name)
            self.student_age_input.setText(str(student.age))
            self.student_degree_input.setText(student.degree_program)
            self.student_credits_input.setText(str(student.completed_credits))
            self.student_gpa_input.setText(str(student.gpa))

    def on_student_selected(self, selected):
        """
        Handle the event when a student is selected in the table.

        Args:
            selected: The selected item(s) in the table.
        """
        if selected.indexes():
            selected_row = selected.indexes()[0].row()
            student_id = self.students_table.item(
                selected_row, 0
            ).text()  # Assuming student ID is in the first column
            self.populate_student_courses(int(student_id))

    def populate_student_courses(self, student_id):
        """
        Populates the student_courses_table with courses the selected student is enrolled in.

        Parameters
        ----------
        student_id : int
            The ID of the selected student.
        """
        courses = self.course_controller.get_courses_for_student(student_id)

        self.student_courses_table.setColumnCount(5)  # Adjust the column count
        self.student_courses_table.setHorizontalHeaderLabels(
            ["Course Name", "Start Date", "End Date", "Credit Hours", "Professor"]
        )

        self.student_courses_table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            # Update these lines to match the order and content of your SQL query
            self.student_courses_table.setItem(
                row, 0, QTableWidgetItem(course[0])
            )  # Course Name
            self.student_courses_table.setItem(
                row, 1, QTableWidgetItem(course[1])
            )  # Start Date
            self.student_courses_table.setItem(
                row, 2, QTableWidgetItem(course[2])
            )  # End Date
            self.student_courses_table.setItem(
                row, 3, QTableWidgetItem(str(course[3]))
            )  # Credit Hours
            self.student_courses_table.setItem(
                row, 4, QTableWidgetItem(course[4])
            )  # Professor Name

    def create_professors_tab(self):
        """
        Creates the Professors tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Professors tab.
        """
        professor_tab = QWidget()
        layout = QVBoxLayout(professor_tab)

        # Create the splitter and set orientation
        splitter = QSplitter(Qt.Vertical)

        # Buttons for operations
        add_button = QPushButton("Add Professor")
        add_button.clicked.connect(self.add_or_update_professor)
        delete_button = QPushButton("Delete Professor")
        delete_button.clicked.connect(self.delete_professor)

        # Table for displaying professors
        self.professors_table.setColumnCount(5)  # Number of fields
        self.professors_table.setHorizontalHeaderLabels(
            ["ID", "First Name", "Last Name", "Department", "Achievement"]
        )

        professor_table_header = self.professors_table.horizontalHeader()
        professor_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_table_header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_table_header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        self.professors_table.doubleClicked.connect(self.load_professor_for_editing)

        # Connect row selection to update the courses table
        self.professors_table.selectionModel().selectionChanged.connect(
            self.on_professor_selected
        )

        # Layout setup
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("First Name:"))
        form_layout.addWidget(self.professor_first_name_input)
        form_layout.addWidget(QLabel("Last Name:"))
        form_layout.addWidget(self.professor_last_name_input)
        form_layout.addWidget(QLabel("Department:"))
        form_layout.addWidget(self.professor_department_input)
        form_layout.addWidget(QLabel("Achievement:"))
        form_layout.addWidget(self.professor_achievement_input)
        form_layout.addWidget(add_button)
        form_layout.addWidget(delete_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.professors_table)

        # Container widget for the second table and its label
        professor_courses_container = QWidget()
        professor_courses_layout = QVBoxLayout(professor_courses_container)
        professor_courses_label = QLabel("Courses Taught:")
        professor_courses_layout.addWidget(professor_courses_label)
        professor_courses_layout.addWidget(self.professor_courses_table)

        # Second table for displaying courses taught by the selected professor
        self.professor_courses_table.setColumnCount(
            4
        )  # Example: Course Name, Start Date, End Date, Credit Hours
        self.professor_courses_table.setHorizontalHeaderLabels(
            ["Course Name", "Start Date", "End Date", "Credit Hours"]
        )

        professor_courses_table_header = self.professor_courses_table.horizontalHeader()
        professor_courses_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_courses_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_courses_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        professor_courses_table_header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )

        # Layout setup
        # layout.addWidget(self.professors_table)
        # layout.addWidget(QLabel("Courses Taught:"))  # Label for the second table
        # layout.addWidget(self.professor_courses_table)

        splitter.addWidget(self.professors_table)
        splitter.addWidget(professor_courses_container)

        # Set the splitter as the central widget
        layout.addWidget(splitter)

        professor_tab.setLayout(layout)
        return professor_tab

    def update_professors_table(self):
        """
        Updates the professors table with the latest data from the database.
        """
        professors = self.professor_controller.list_all_professors()

        self.professors_table.setRowCount(len(professors))

        for row, professor in enumerate(professors):
            self.professors_table.setItem(
                row, 0, QTableWidgetItem(str(professor.professor_id))
            )
            self.professors_table.setItem(
                row, 1, QTableWidgetItem(professor.first_name)
            )
            self.professors_table.setItem(row, 2, QTableWidgetItem(professor.last_name))
            self.professors_table.setItem(
                row, 3, QTableWidgetItem(professor.department)
            )
            self.professors_table.setItem(
                row, 4, QTableWidgetItem(professor.academic_achievement)
            )

    def add_or_update_professor(self):
        """
        Adds a new professor or updates an existing one based on the input fields.
        """
        # Collect data from input fields
        first_name = self.professor_first_name_input.text().strip()
        last_name = self.professor_last_name_input.text().strip()
        department = self.professor_department_input.text().strip()
        academic_achievement = self.professor_achievement_input.text().strip()

        # Validate input data
        if not all([first_name, last_name, department, academic_achievement]):
            QMessageBox.warning(
                self, "Input Error", "Please enter valid data for all fields."
            )
            return

        if hasattr(self, "currently_editing_professor_id"):
            # Update existing professor
            self.professor_controller.update_professor(
                self.currently_editing_professor_id,
                first_name,
                last_name,
                department,
                academic_achievement,
            )
            QMessageBox.information(self, "Success", "Professor updated successfully.")
            del self.currently_editing_professor_id  # Clear the editing flag
        else:
            # Add new professor
            self.professor_controller.add_professor(
                first_name, last_name, department, academic_achievement
            )
            QMessageBox.information(self, "Success", "Professor added successfully.")

        # Update the professors_table with new data and clear input fields
        self.update_professors_table()
        self.clear_professor_input_fields()

    def delete_professor(self):
        """
        Deletes the selected professor record from the database and updates the table.
        """
        selected_items = self.professors_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Selection Error", "Please select a professor to delete."
            )
            return

        # Assuming the first column in the table contains the professor ID
        professor_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this professor?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.professor_controller.delete_professor(professor_id)
            self.update_professors_table()
            QMessageBox.information(self, "Success", "Professor deleted successfully.")

    def clear_professor_input_fields(self):
        """
        Clears all input fields in the professor tab.
        """
        self.professor_first_name_input.clear()
        self.professor_last_name_input.clear()
        self.professor_department_input.clear()
        self.professor_achievement_input.clear()

    def load_professor_for_editing(self, index):
        """
        Loads the selected professor's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        professor_id = self.professors_table.item(
            index.row(), 0
        ).text()  # Assuming professor ID is in the first column
        self.currently_editing_professor_id = int(professor_id)

        professor = self.professor_controller.get_professor(
            self.currently_editing_professor_id
        )
        if professor:
            self.professor_first_name_input.setText(professor.first_name)
            self.professor_last_name_input.setText(professor.last_name)
            self.professor_department_input.setText(professor.department)
            self.professor_achievement_input.setText(professor.academic_achievement)

    def on_professor_selected(self, selected):
        """
        Handle the event when a professor is selected in the UI.

        Args:
            selected: The selected item in the UI.

        Returns:
            None
        """
        if selected.indexes():
            selected_row = selected.indexes()[0].row()
            professor_id = self.professors_table.item(
                selected_row, 0
            ).text()  # Assuming professor ID is in the first column
            self.populate_professor_courses(int(professor_id))

    def populate_professor_courses(self, professor_id):
        """
        Populates the professor_courses_table with courses taught by the selected professor.

        Parameters
        ----------
        professor_id : int
            The ID of the selected professor.
        """
        courses = self.course_controller.get_courses_for_professor(professor_id)

        self.professor_courses_table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            # Assuming course data is a tuple like (course_name, start_date, end_date, credit_hours)
            self.professor_courses_table.setItem(
                row, 0, QTableWidgetItem(course[0])
            )  # Course Name
            self.professor_courses_table.setItem(
                row, 1, QTableWidgetItem(course[1])
            )  # Start Date
            self.professor_courses_table.setItem(
                row, 2, QTableWidgetItem(course[2])
            )  # End Date
            self.professor_courses_table.setItem(
                row, 3, QTableWidgetItem(str(course[3]))
            )  # Credit Hours

    def create_courses_tab(self):
        """
        Creates the Courses tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Courses tab.
        """
        course_tab = QWidget()
        layout = QVBoxLayout(course_tab)

        # Create the splitter and set orientation
        splitter = QSplitter(Qt.Vertical)

        # Buttons for operations
        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_or_update_course)
        delete_button = QPushButton("Delete Course")
        delete_button.clicked.connect(self.delete_course)

        # Table for displaying courses
        self.courses_table.setColumnCount(7)  # Number of fields
        self.courses_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Start Date",
                "End Date",
                "Credits",
                "Professor ID",
                "Professor Name",
            ]
        )

        course_table_header = self.courses_table.horizontalHeader()
        course_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )   # ID
        course_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )   # Name
        course_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        course_table_header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        course_table_header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        course_table_header.setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )
        course_table_header.setSectionResizeMode(
            6, QHeaderView.ResizeMode.ResizeToContents
        )

        self.courses_table.doubleClicked.connect(self.load_course_for_editing)

        # Connect row selection to update the students table
        self.courses_table.selectionModel().selectionChanged.connect(
            self.on_course_selected
        )

        # Layout setup
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.course_name_input)
        form_layout.addWidget(QLabel("Start Date:"))
        form_layout.addWidget(self.course_start_date_input)
        form_layout.addWidget(QLabel("End Date:"))
        form_layout.addWidget(self.course_end_date_input)
        form_layout.addWidget(QLabel("Credits:"))
        form_layout.addWidget(self.course_credits_input)
        form_layout.addWidget(QLabel("Professor ID:"))
        form_layout.addWidget(self.course_professor_id_input)
        form_layout.addWidget(add_button)
        form_layout.addWidget(delete_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.courses_table)

        # Container widget for the second table and its label
        course_students_container = QWidget()
        course_students_layout = QVBoxLayout(course_students_container)
        course_students_label = QLabel("Students Enrolled:")
        course_students_layout.addWidget(course_students_label)
        course_students_layout.addWidget(self.course_students_table)


        # Second table for displaying students enrolled in the selected course
        self.course_students_table.setColumnCount(
            3
        )  # Example: Student ID, First Name, Last Name
        self.course_students_table.setHorizontalHeaderLabels(
            ["Student ID", "First Name", "Last Name"]
        )

        course_students_table_header = self.course_students_table.horizontalHeader()
        course_students_table_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        course_students_table_header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        course_students_table_header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )

        # Layout setup
        # layout.addWidget(self.courses_table)
        # layout.addWidget(QLabel("Enrolled Students:"))  # Label for the second table
        # layout.addWidget(self.course_students_table)

        splitter.addWidget(self.courses_table)
        splitter.addWidget(course_students_container)

        # Set the splitter as the central widget
        layout.addWidget(splitter)

        course_tab.setLayout(layout)
        return course_tab

    def update_courses_table(self):
        """
        Updates the courses table with the latest data from the database.
        """
        courses = self.course_controller.list_all_courses()

        self.courses_table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            self.courses_table.setItem(
                row, 0, QTableWidgetItem(str(course.course_id))
            )  # Course ID
            self.courses_table.setItem(
                row, 1, QTableWidgetItem(course.name)
            )  # Course Name
            self.courses_table.setItem(
                row, 2, QTableWidgetItem(course.start_date)
            )  # Start Date
            self.courses_table.setItem(
                row, 3, QTableWidgetItem(course.end_date)
            )  # End Date
            self.courses_table.setItem(
                row, 4, QTableWidgetItem(str(course.credit_hours))
            )  # Credit Hours
            self.courses_table.setItem(
                row, 5, QTableWidgetItem(str(course.professor_id))
            )  # Professor Name
            self.courses_table.setItem(
                row, 6, QTableWidgetItem(course.professor_name)
            )  # Professor Name

    def add_or_update_course(self):
        """
        Adds a new course or updates an existing one based on the input fields.
        """
        # Collect data from input fields
        name = self.course_name_input.text().strip()
        start_date = self.course_start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.course_end_date_input.date().toString("yyyy-MM-dd")
        course_credits = self.course_credits_input.text().strip()
        professor_id = self.course_professor_id_input.text().strip()

        # Validate input data
        if not all([name, start_date, end_date, course_credits, professor_id]):
            QMessageBox.warning(
                self, "Input Error", "Please enter valid data for all fields."
            )
            return

        try:
            course_credits = int(credits)
            professor_id = int(professor_id)
        except ValueError:
            QMessageBox.warning(
                self, "Input Error", "Credits and Professor ID must be numbers."
            )
            return

        if hasattr(self, "currently_editing_course_id"):
            # Update existing course
            self.course_controller.update_course(
                self.currently_editing_course_id,
                start_date,
                end_date,
                name,
                course_credits,
                professor_id,
            )
            QMessageBox.information(self, "Success", "Course updated successfully.")
            del self.currently_editing_course_id  # Clear the editing flag
        else:
            # Add new course
            self.course_controller.add_course(
                start_date, end_date, name, course_credits, professor_id
            )
            QMessageBox.information(self, "Success", "Course added successfully.")

        # Update the courses_table with new data and clear input fields
        self.update_courses_table()
        self.clear_course_input_fields()

    def delete_course(self):
        """
        Deletes the selected course record from the database and updates the table.
        """
        selected_items = self.courses_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(
                self, "Selection Error", "Please select a course to delete."
            )
            return

        # Assuming the first column in the table contains the course ID
        course_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this course?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.course_controller.delete_course(course_id)
            self.update_courses_table()
            QMessageBox.information(self, "Success", "Course deleted successfully.")

    def clear_course_input_fields(self):
        """
        Clears all input fields in the course tab.
        """
        self.course_name_input.clear()
        self.course_start_date_input.clear()
        self.course_end_date_input.clear()
        self.course_credits_input.clear()
        self.course_professor_id_input.clear()

    def load_course_for_editing(self, index):
        """
        Loads the selected course's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        course_id = self.courses_table.item(
            index.row(), 0
        ).text()  # Assuming course ID is in the first column
        self.currently_editing_course_id = int(course_id)

        course = self.course_controller.get_course(self.currently_editing_course_id)
        if course:
            self.course_name_input.setText(course.name)
            self.course_start_date_input.setText(course.start_date)
            self.course_end_date_input.setText(course.end_date)
            self.course_credits_input.setText(str(course.credit_hours))
            self.course_professor_id_input.setText(str(course.professor_id))

    def on_course_selected(self, selected):
        """
        Handle the event when a course is selected in the UI.

        Args:
            selected: The selected item in the UI.

        Returns:
            None
        """
        if selected.indexes():
            selected_row = selected.indexes()[0].row()
            course_id = self.courses_table.item(
                selected_row, 0
            ).text()  # Assuming course ID is in the first column
            self.populate_course_students(int(course_id))

    def populate_course_students(self, course_id):
        """
        Populates the course_students_table with students enrolled in the selected course.

        Parameters
        ----------
        course_id : int
            The ID of the selected course.
        """
        students = self.student_controller.get_students_for_course(course_id)

        self.course_students_table.setRowCount(len(students))

        for row, student in enumerate(students):
            # Assuming student data is a tuple like (student_id, first_name, last_name)
            self.course_students_table.setItem(
                row, 0, QTableWidgetItem(str(student[0]))
            )  # Student ID
            self.course_students_table.setItem(
                row, 1, QTableWidgetItem(student[1])
            )  # First Name
            self.course_students_table.setItem(
                row, 2, QTableWidgetItem(student[2])
            )  # Last Name


def main():
    """
    Entry point of the application.
    Initializes the QApplication and creates the main window.
    """
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        db_manager = DatabaseManager(
            "/home/curranz/dev/py/git/EduMatrix/edumatrix/edumatrix.db"
        )  # Assuming 'edumatrix.db' as the database file
        db_manager.initialize_database()
        student_controller = StudentController(db_manager)
        professor_controller = ProfessorController(db_manager)
        course_controller = CourseController(db_manager)

        main_window = EduMatrixApp(
            student_controller, professor_controller, course_controller
        )
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()


if __name__ == "__main__":
    main()
