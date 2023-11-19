# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QMessageBox
from controllers import StudentController, ProfessorController, CourseController
from database import DatabaseManager

class LoginDialog(QDialog):
    def __init__(self):
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
        if self.username_input.text() == "admin" and self.password_input.text() == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Incorrect username or password.")

class EduMatrixApp(QMainWindow):
    def __init__(self, student_controller: StudentController, professor_controller: ProfessorController, course_controller: CourseController):
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

    def create_professors_tab(self):
        """
        Creates the Professors tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Professors tab.
        """
        professor_tab = QWidget()
        layout = QVBoxLayout()

        # Input fields for professor details
        self.professor_first_name_input = QLineEdit()
        self.professor_last_name_input = QLineEdit()
        self.professor_department_input = QLineEdit()
        self.professor_achievement_input = QLineEdit()

        # Buttons for operations
        add_button = QPushButton("Add Professor")
        add_button.clicked.connect(self.add_or_update_professor)
        delete_button = QPushButton("Delete Professor")
        delete_button.clicked.connect(self.delete_professor)

        # Table for displaying professors
        self.professors_table = QTableWidget()
        self.professors_table.setColumnCount(5)  # Number of fields
        self.professors_table.setHorizontalHeaderLabels(["ID","First Name", "Last Name", "Department", "Achievement"])
        self.professors_table.doubleClicked.connect(self.load_professor_for_editing)

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

        professor_tab.setLayout(layout)
        return professor_tab

    def load_professor_for_editing(self, index):
        """
        Loads the selected professor's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        professor_id = self.professors_table.item(index.row(), 0).text()  # Assuming professor ID is in the first column
        self.currently_editing_professor_id = int(professor_id)

        professor = self.professor_controller.get_professor(self.currently_editing_professor_id)
        if professor:
            self.professor_first_name_input.setText(professor.first_name)
            self.professor_last_name_input.setText(professor.last_name)
            self.professor_department_input.setText(professor.department)
            self.professor_achievement_input.setText(professor.academic_achievement)

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
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields.")
            return

        if hasattr(self, 'currently_editing_professor_id'):
            # Update existing professor
            self.professor_controller.update_professor(
                self.currently_editing_professor_id,
                first_name, last_name, department, academic_achievement
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
            QMessageBox.warning(self, "Selection Error", "Please select a professor to delete.")
            return

        # Assuming the first column in the table contains the professor ID
        professor_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this professor?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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

    def update_professors_table(self):
        """
        Updates the professors table with the latest data from the database.
        """
        professors = self.professor_controller.list_all_professors()

        self.professors_table.setRowCount(len(professors))

        for row, professor in enumerate(professors):
            self.professors_table.setItem(row, 0, QTableWidgetItem(str(professor.professor_id)))
            self.professors_table.setItem(row, 1, QTableWidgetItem(professor.first_name))
            self.professors_table.setItem(row, 2, QTableWidgetItem(professor.last_name))
            self.professors_table.setItem(row, 3, QTableWidgetItem(professor.department))
            self.professors_table.setItem(row, 4, QTableWidgetItem(professor.academic_achievement))

    def create_courses_tab(self):
        """
        Creates the Courses tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Courses tab.
        """
        course_tab = QWidget()
        layout = QVBoxLayout()

        # Input fields for course details
        self.course_name_input = QLineEdit()
        self.course_start_date_input = QLineEdit()
        self.course_end_date_input = QLineEdit()
        self.course_credits_input = QLineEdit()
        self.course_professor_id_input = QLineEdit()

        # Buttons for operations
        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_or_update_course)
        delete_button = QPushButton("Delete Course")
        delete_button.clicked.connect(self.delete_course)

        # Table for displaying courses
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(6)  # Number of fields
        self.courses_table.setHorizontalHeaderLabels(["ID", "Name", "Start Date", "End Date", "Credits", "Professor ID"])
        self.courses_table.doubleClicked.connect(self.load_course_for_editing)

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

        course_tab.setLayout(layout)
        return course_tab

    def load_student_for_editing(self, index):
        """
        Loads the selected student's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        # Fetch the student ID from the table
        student_id = self.students_table.item(index.row(), 0).text()  # Assuming student ID is in the first column
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

    def create_students_tab(self):
        """
        Creates the Students tab with necessary UI components.

        Returns
        -------
        QWidget
            The widget for the Students tab.
        """
        student_tab = QWidget()
        layout = QVBoxLayout()

        # Input fields for student details
        self.student_first_name_input = QLineEdit()
        self.student_last_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_degree_input = QLineEdit()
        self.student_credits_input = QLineEdit()
        self.student_gpa_input = QLineEdit()

        # Buttons for operations
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_or_update_student)

        # Add Delete Student Button
        delete_button = QPushButton("Delete Student")
        delete_button.clicked.connect(self.delete_student)

        # Connect double-click event on the table to load_student_for_editing
        self.students_table.doubleClicked.connect(self.load_student_for_editing)

        # Table for displaying students
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(7)  # Set the number of columns
        self.students_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Age", "Degree", "Credits", "GPA"])

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

        student_tab.setLayout(layout)
        return student_tab

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
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for age, credits, and GPA.")
            return

        degree_program = self.student_degree_input.text().strip()

        # Validate input data
        if not all([first_name, last_name, degree_program]) or age <= 0 or completed_credits < 0 or not 0 <= gpa <= 4.0:
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields.")
            return

        # Add the student using the student_controller
        self.student_controller.add_student(first_name, last_name, age, degree_program, completed_credits, gpa)

        # Update the students_table with new data
        self.update_students_table()

        # Clear input fields after adding
        self.clear_student_input_fields()

        # Show message box on success
        QMessageBox.information(self, "Success", "Student added successfully.")

        if hasattr(self, 'currently_editing_student_id'):
            # Update existing student
            self.student_controller.update_student(
                self.currently_editing_student_id,
                first_name, last_name, age, degree_program, completed_credits, gpa
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
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete.")
            return

        # Assuming the first column in the table contains the student ID
        student_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this student?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
            self.students_table.setItem(row, 0, QTableWidgetItem(str(student.student_id)))
            self.students_table.setItem(row, 1, QTableWidgetItem(student.first_name))
            self.students_table.setItem(row, 2, QTableWidgetItem(student.last_name))
            self.students_table.setItem(row, 3, QTableWidgetItem(str(student.age)))
            self.students_table.setItem(row, 4, QTableWidgetItem(student.degree_program))
            self.students_table.setItem(row, 5, QTableWidgetItem(str(student.completed_credits)))
            self.students_table.setItem(row, 6, QTableWidgetItem(str(student.gpa)))

    def add_or_update_course(self):
        """
        Adds a new course or updates an existing one based on the input fields.
        """
        # Collect data from input fields
        name = self.course_name_input.text().strip()
        start_date = self.course_start_date_input.text().strip()
        end_date = self.course_end_date_input.text().strip()
        credits = self.course_credits_input.text().strip()
        professor_id = self.course_professor_id_input.text().strip()

        # Validate input data
        if not all([name, start_date, end_date, credits, professor_id]):
            QMessageBox.warning(self, "Input Error", "Please enter valid data for all fields.")
            return

        try:
            credits = int(credits)
            professor_id = int(professor_id)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Credits and Professor ID must be numbers.")
            return

        if hasattr(self, 'currently_editing_course_id'):
            # Update existing course
            self.course_controller.update_course(
                self.currently_editing_course_id, start_date, end_date, name, credits, professor_id
            )
            QMessageBox.information(self, "Success", "Course updated successfully.")
            del self.currently_editing_course_id  # Clear the editing flag
        else:
            # Add new course
            self.course_controller.add_course(
                start_date, end_date, name, credits, professor_id
            )
            QMessageBox.information(self, "Success", "Course added successfully.")

        # Update the courses_table with new data and clear input fields
        self.update_courses_table()
        self.clear_course_input_fields()

    def clear_course_input_fields(self):
        """
        Clears all input fields in the course tab.
        """
        self.course_name_input.clear()
        self.course_start_date_input.clear()
        self.course_end_date_input.clear()
        self.course_credits_input.clear()
        self.course_professor_id_input.clear()

    def delete_course(self):
        """
        Deletes the selected course record from the database and updates the table.
        """
        selected_items = self.courses_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a course to delete.")
            return

        # Assuming the first column in the table contains the course ID
        course_id = int(selected_items[0].text())

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this course?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.course_controller.delete_course(course_id)
            self.update_courses_table()
            QMessageBox.information(self, "Success", "Course deleted successfully.")


    def update_courses_table(self):
        """
        Updates the courses table with the latest data from the database.
        """
        courses = self.course_controller.list_all_courses()

        self.courses_table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            self.courses_table.setItem(row, 0, QTableWidgetItem(str(course.course_id)))
            self.courses_table.setItem(row, 1, QTableWidgetItem(course.name))
            self.courses_table.setItem(row, 2, QTableWidgetItem(course.start_date))
            self.courses_table.setItem(row, 3, QTableWidgetItem(course.end_date))
            self.courses_table.setItem(row, 4, QTableWidgetItem(str(course.credit_hours)))
            self.courses_table.setItem(row, 5, QTableWidgetItem(str(course.professor_id)))

    def load_course_for_editing(self, index):
        """
        Loads the selected course's data into the input fields for editing.

        Parameters
        ----------
        index : QModelIndex
            The index of the selected item in the table.
        """
        course_id = self.courses_table.item(index.row(), 0).text()  # Assuming course ID is in the first column
        self.currently_editing_course_id = int(course_id)

        course = self.course_controller.get_course(self.currently_editing_course_id)
        if course:
            self.course_name_input.setText(course.name)
            self.course_start_date_input.setText(course.start_date)
            self.course_end_date_input.setText(course.end_date)
            self.course_credits_input.setText(str(course.credit_hours))
            self.course_professor_id_input.setText(str(course.professor_id))

def main():
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        db_manager = DatabaseManager("edumatrix.db")  # Assuming 'edumatrix.db' as the database file
        db_manager.initialize_database()
        student_controller = StudentController(db_manager)
        professor_controller = ProfessorController(db_manager)
        course_controller = CourseController(db_manager)

        main_window = EduMatrixApp(student_controller, professor_controller, course_controller)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
