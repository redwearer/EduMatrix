# database.py

import sqlite3
from sqlite3 import Connection

class DatabaseManager:
    def __init__(self, db_path: str):
        """
        Initialize the database manager with the path to the SQLite database.

        Parameters
        ----------
        db_path : str
            Path to the SQLite database file.
        """
        self.db_path = db_path

    def get_connection(self) -> Connection:
        """
        Create and return a connection to the SQLite database.

        Returns
        -------
        Connection
            A SQLite3 connection object.
        """
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        """
        Initialize the database by creating tables if they do not exist.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Age INTEGER,
                DegreeProgram TEXT,
                CompletedCredits INTEGER,
                GPA REAL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Professors (
                ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Department TEXT,
                AcademicAchievement TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses (
                CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
                StartDate TEXT,
                EndDate TEXT,
                Name TEXT NOT NULL,
                CreditHours INTEGER,
                ProfessorID INTEGER,
                FOREIGN KEY (ProfessorID) REFERENCES Professors(ProfessorID)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enrollments (
                StudentID INTEGER,
                CourseID INTEGER,
                Grade TEXT,
                PRIMARY KEY (StudentID, CourseID),
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
            );
        """)

        conn.commit()
        conn.close()

    # CRUD Operations for Students
    def create_student(self, first_name: str, last_name: str, age: int, degree_program: str, completed_credits: int, gpa: float):
        """
        Create a new student record in the database.

        Parameters
        ----------
        first_name : str
        last_name : str
        age : int
        degree_program : str
        completed_credits : int
        gpa : float
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Students (FirstName, LastName, Age, DegreeProgram, CompletedCredits, GPA)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, age, degree_program, completed_credits, gpa))

        conn.commit()
        conn.close()

    def read_student(self, student_id: int):
        """
        Read a student record from the database.

        Parameters
        ----------
        student_id : int

        Returns
        -------
        dict
            A dictionary containing the student's data.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
        student = cursor.fetchone()

        conn.close()
        return student

    def update_student(self, student_id: int, first_name: str, last_name: str, age: int, degree_program: str, completed_credits: int, gpa: float):
        """
        Update a student record in the database.

        Parameters
        ----------
        student_id : int
        first_name : str
        last_name : str
        age : int
        degree_program : str
        completed_credits : int
        gpa : float
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Students
            SET FirstName = ?, LastName = ?, Age = ?, DegreeProgram = ?, CompletedCredits = ?, GPA = ?
            WHERE StudentID = ?
        """, (first_name, last_name, age, degree_program, completed_credits, gpa, student_id))

        conn.commit()
        conn.close()

    def delete_student(self, student_id: int):
        """
        Delete a student record from the database.

        Parameters
        ----------
        student_id : int
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Students WHERE StudentID = ?", (student_id,))

        conn.commit()
        conn.close()

    def list_all_students(self):
        """
        Retrieves all student records from the database.

        Returns
        -------
        list
            A list of tuples, each representing a student record.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Students")
        students_data = cursor.fetchall()

        conn.close()
        return students_data

    # CRUD Operations for Professors
    def create_professor(self, first_name: str, last_name: str, department: str, academic_achievement: str):
        """
        Create a new professor record in the database.

        Parameters
        ----------
        first_name : str
        last_name : str
        department : str
        academic_achievement : str
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Professors (FirstName, LastName, Department, AcademicAchievement)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, department, academic_achievement))

        conn.commit()
        conn.close()

    def read_professor(self, professor_id: int):
        """
        Read a professor record from the database.

        Parameters
        ----------
        professor_id : int

        Returns
        -------
        dict
            A dictionary containing the professor's data.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Professors WHERE ProfessorID = ?", (professor_id,))
        professor = cursor.fetchone()

        conn.close()
        return professor

    def update_professor(self, professor_id: int, first_name: str, last_name: str, department: str, academic_achievement: str):
        """
        Update a professor record in the database.

        Parameters
        ----------
        professor_id : int
        first_name : str
        last_name : str
        department : str
        academic_achievement : str
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Professors
            SET FirstName = ?, LastName = ?, Department = ?, AcademicAchievement = ?
            WHERE ProfessorID = ?
        """, (first_name, last_name, department, academic_achievement, professor_id))

        conn.commit()
        conn.close()

    def delete_professor(self, professor_id: int):
        """
        Delete a professor record from the database.

        Parameters
        ----------
        professor_id : int
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Professors WHERE ProfessorID = ?", (professor_id,))

        conn.commit()
        conn.close()

    def list_all_professors(self):
        """
        Retrieves all professor records from the database.

        Returns
        -------
        list
            A list of tuples, each representing a professor record.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Professors")
        professors_data = cursor.fetchall()

        conn.close()
        return professors_data

    # CRUD Operations for Courses
    def create_course(self, start_date: str, end_date: str, name: str, credit_hours: int, professor_id: int):
        """
        Create a new course record in the database.

        Parameters
        ----------
        start_date : str
        end_date : str
        name : str
        credit_hours : int
        professor_id : int
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Courses (StartDate, EndDate, Name, CreditHours, ProfessorID)
            VALUES (?, ?, ?, ?, ?)
        """, (start_date, end_date, name, credit_hours, professor_id))

        conn.commit()
        conn.close()

    def read_course(self, course_id: int):
        """
        Read a course record from the database.

        Parameters
        ----------
        course_id : int

        Returns
        -------
        dict
            A dictionary containing the course's data.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Courses WHERE CourseID = ?", (course_id,))
        course = cursor.fetchone()

        conn.close()
        return course

    def update_course(self, course_id: int, start_date: str, end_date: str, name: str, credit_hours: int, professor_id: int):
        """
        Update a course record in the database.

        Parameters
        ----------
        course_id : int
        start_date : str
        end_date : str
        name : str
        credit_hours : int
        professor_id : int
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Courses
            SET StartDate = ?, EndDate = ?, Name = ?, CreditHours = ?, ProfessorID = ?
            WHERE CourseID = ?
        """, (start_date, end_date, name, credit_hours, professor_id, course_id))

        conn.commit()
        conn.close()

    def delete_course(self, course_id: int):
        """
        Delete a course record from the database.

        Parameters
        ----------
        course_id : int
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Courses WHERE CourseID = ?", (course_id,))

        conn.commit()
        conn.close()

    def list_all_courses(self):
        """
        Retrieves all course records from the database.

        Returns
        -------
        list
            A list of tuples, each representing a course record.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Courses")
        courses_data = cursor.fetchall()

        conn.close()
        return courses_data

    def get_courses_for_student(self, student_id: int):
        """
        Retrieves courses for a given student from the database, including credit hours and professor name.

        Parameters
        ----------
        student_id : int

        Returns
        -------
        list
            A list of courses the student is enrolled in, including additional details.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Adjust the SQL query based on your database schema
        cursor.execute("""
            SELECT c.Name, c.StartDate, c.EndDate, c.CreditHours, p.FirstName || ' ' || p.LastName as ProfessorName
            FROM Courses c
            JOIN Enrollments e ON c.CourseID = e.CourseID
            LEFT JOIN Professors p ON c.ProfessorID = p.ProfessorID
            WHERE e.StudentID = ?
        """, (student_id,))

        courses_data = cursor.fetchall()

        conn.close()
        return courses_data

    def get_courses_for_professor(self, professor_id: int):
        """
        Retrieves courses taught by a given professor from the database.

        Parameters
        ----------
        professor_id : int

        Returns
        -------
        list
            A list of courses taught by the professor.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.Name, c.StartDate, c.EndDate, c.CreditHours
            FROM Courses c
            WHERE c.ProfessorID = ?
        """, (professor_id,))

        courses_data = cursor.fetchall()

        conn.close()
        return courses_data