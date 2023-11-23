"""
This module contains the controllers for the application.
"""
from typing import List
from database import DatabaseManager
from models import Professor, Student, Course


class StudentController:
    """
    Controller for handling student-related operations.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Controller for handling student-related operations.

        Parameters
        ----------
        db_manager : DatabaseManager
            The database manager instance to handle database operations.
        """
        self.db_manager = db_manager

    def add_student(
        self,
        first_name: str,
        last_name: str,
        age: int,
        degree_program: str,
        completed_credits: int,
        gpa: float,
    ):
        """
        Adds a new student to the database.

        Parameters
        ----------
        first_name : str
            Student's first name.
        last_name : str
            Student's last name.
        age : int
            Student's age.
        degree_program : str
            The degree program in which the student is enrolled.
        completed_credits : int
            Number of credits completed by the student.
        gpa : float
            Student's Grade Point Average.
        """
        self.db_manager.create_student(
            first_name, last_name, age, degree_program, completed_credits, gpa
        )

    def get_student(self, student_id: int) -> Student:
        """
        Retrieves a student from the database by their ID.

        Parameters
        ----------
        student_id : int
            The unique identifier of the student.

        Returns
        -------
        Student
            The student object with the specified ID.
        """
        student_data = self.db_manager.read_student(student_id)
        if student_data:
            return Student(*student_data)
        return None

    def update_student(
        self,
        student_id: int,
        first_name: str,
        last_name: str,
        age: int,
        degree_program: str,
        completed_credits: int,
        gpa: float,
    ):
        """
        Updates an existing student's information in the database.

        Parameters
        ----------
        student_id : int
            The unique identifier of the student to update.
        first_name : str
            Updated first name.
        last_name : str
            Updated last name.
        age : int
            Updated age.
        degree_program : str
            Updated degree program.
        completed_credits : int
            Updated number of completed credits.
        gpa : float
            Updated GPA.
        """
        self.db_manager.update_student(
            student_id,
            first_name,
            last_name,
            age,
            degree_program,
            completed_credits,
            gpa,
        )

    def delete_student(self, student_id: int):
        """
        Deletes a student from the database.

        Parameters
        ----------
        student_id : int
            The unique identifier of the student to be deleted.
        """
        self.db_manager.delete_student(student_id)

    def list_all_students(self) -> List[Student]:
        """
        Retrieves all students from the database.

        Returns
        -------
        List[Student]
            A list of all student objects.
        """
        students_data = self.db_manager.list_all_students()
        return [Student(*data) for data in students_data] if students_data else []

    def get_students_for_course(self, course_id: int):
        """
        Retrieves students enrolled in a given course.

        Parameters
        ----------
        course_id : int
            The ID of the course.

        Returns
        -------
        list
            A list of students enrolled in the course.
        """
        return self.db_manager.get_students_for_course(course_id)


class ProfessorController:
    """
    Controller for handling professor-related operations.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Controller for handling professor-related operations.

        Parameters
        ----------
        db_manager : DatabaseManager
            The database manager instance to handle database operations.
        """
        self.db_manager = db_manager

    def add_professor(
        self,
        first_name: str,
        last_name: str,
        department: str,
        academic_achievement: str,
    ):
        """
        Adds a new professor to the database.

        Parameters
        ----------
        first_name : str
            Professor's first name.
        last_name : str
            Professor's last name.
        department : str
            The department to which the professor belongs.
        academic_achievement : str
            The highest academic achievement of the professor (e.g., PhD in Mathematics).
        """
        self.db_manager.create_professor(
            first_name, last_name, department, academic_achievement
        )

    def get_professor(self, professor_id: int) -> Professor:
        """
        Retrieves a professor from the database by their ID.

        Parameters
        ----------
        professor_id : int
            The unique identifier of the professor.

        Returns
        -------
        Professor
            The professor object with the specified ID.
        """
        professor_data = self.db_manager.read_professor(professor_id)
        if professor_data:
            return Professor(*professor_data)
        return None

    def update_professor(
        self,
        professor_id: int,
        first_name: str,
        last_name: str,
        department: str,
        academic_achievement: str,
    ):
        """
        Updates an existing professor's information in the database.

        Parameters
        ----------
        professor_id : int
            The unique identifier of the professor to update.
        first_name : str
            Updated first name.
        last_name : str
            Updated last name.
        department : str
            Updated department.
        academic_achievement : str
            Updated academic achievement.
        """
        self.db_manager.update_professor(
            professor_id, first_name, last_name, department, academic_achievement
        )

    def delete_professor(self, professor_id: int):
        """
        Deletes a professor from the database.

        Parameters
        ----------
        professor_id : int
            The unique identifier of the professor to be deleted.
        """
        self.db_manager.delete_professor(professor_id)

    def list_all_professors(self) -> List[Professor]:
        """
        Retrieves all professors from the database.

        Returns
        -------
        List[Professor]
            A list of all professor objects.
        """
        professors_data = self.db_manager.list_all_professors()
        return [Professor(*data) for data in professors_data] if professors_data else []


class CourseController:
    """
    Controller for handling course-related operations.
    """
    def __init__(self, db_manager: DatabaseManager):
        """
        Controller for handling course-related operations.

        Parameters
        ----------
        db_manager : DatabaseManager
            The database manager instance to handle database operations.
        """
        self.db_manager = db_manager

    def add_course(
        self,
        start_date: str,
        end_date: str,
        name: str,
        credit_hours: int,
        professor_id: int,
    ):
        """
        Adds a new course to the database.

        Parameters
        ----------
        start_date : str
            The start date of the course.
        end_date : str
            The end date of the course.
        name : str
            The name of the course.
        credit_hours : int
            The number of credit hours for the course.
        professor_id : int
            The identifier of the professor teaching the course.
        """
        self.db_manager.create_course(
            start_date, end_date, name, credit_hours, professor_id
        )

    def get_course(self, course_id: int) -> Course:
        """
        Retrieves a course from the database by its ID.

        Parameters
        ----------
        course_id : int
            The unique identifier of the course.

        Returns
        -------
        Course
            The course object with the specified ID.
        """
        course_data = self.db_manager.read_course(course_id)
        if course_data:
            return Course(*course_data)
        return None

    def update_course(
        self,
        course_id: int,
        start_date: str,
        end_date: str,
        name: str,
        credit_hours: int,
        professor_id: int,
    ):
        """
        Updates an existing course's information in the database.

        Parameters
        ----------
        course_id : int
            The unique identifier of the course to update.
        start_date : str
            Updated start date.
        end_date : str
            Updated end date.
        name : str
            Updated name.
        credit_hours : int
            Updated credit hours.
        professor_id : int
            Updated professor ID.
        """
        self.db_manager.update_course(
            course_id, start_date, end_date, name, credit_hours, professor_id
        )

    def delete_course(self, course_id: int):
        """
        Deletes a course from the database.

        Parameters
        ----------
        course_id : int
            The unique identifier of the course to be deleted.
        """
        self.db_manager.delete_course(course_id)

    def list_all_courses(self) -> List[Course]:
        """
        Retrieves all courses from the database.

        Returns
        -------
        List[Course]
            A list of all course objects.
        """
        courses_data = self.db_manager.list_all_courses()
        return [Course(*data) for data in courses_data] if courses_data else []

    def get_courses_for_student(self, student_id: int):
        """
        Retrieves courses for a given student.

        Parameters
        ----------
        student_id : int
            The ID of the student.

        Returns
        -------
        list
            A list of courses the student is enrolled in.
        """
        return self.db_manager.get_courses_for_student(student_id)

    def get_courses_for_professor(self, professor_id: int):
        """
        Retrieves courses taught by a given professor.

        Parameters
        ----------
        professor_id : int
            The ID of the professor.

        Returns
        -------
        list
            A list of courses taught by the professor.
        """
        return self.db_manager.get_courses_for_professor(professor_id)
