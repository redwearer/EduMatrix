#!/usr/bin/python3
"""
This module contains the models for the database.
"""
from typing import Optional


class Student:
    """
    Represents a student.
    """

    def __init__(
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
        Represents a student.

        Parameters
        ----------
        student_id : int
            Unique identifier for the student.
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
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.degree_program = degree_program
        self.completed_credits = completed_credits
        self.gpa = gpa


class Professor:
    """
    Represents a professor.
    """
    def __init__(
        self,
        professor_id: int,
        first_name: str,
        last_name: str,
        department: str,
        academic_achievement: str,
    ):
        """
        Represents a professor.

        Parameters
        ----------
        professor_id : int
            Unique identifier for the professor.
        first_name : str
            Professor's first name.
        last_name : str
            Professor's last name.
        department : str
            The department to which the professor belongs.
        academic_achievement : str
            The highest academic achievement of the professor (e.g., PhD in Mathematics).
        """
        self.professor_id = professor_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.academic_achievement = academic_achievement


class Course:
    """
    Represents a course.
    """
    def __init__(
        self,
        course_id: int,
        name: str,
        start_date: str,
        end_date: str,
        credit_hours: int,
        professor_id: Optional[int] = None,
        professor_name: Optional[str] = None,
    ):
        """
        Represents a course.

        Parameters
        ----------
        course_id : int
            Unique identifier for the course.
        start_date : str
            The start date of the course.
        end_date : str
            The end date of the course.
        name : str
            The name of the course.
        credit_hours : int
            The number of credit hours for the course.
        professor_id : Optional[int]
            The identifier of the professor teaching the course. Default is None.
            c.CourseID, c.Name, c.StartDate, c.EndDate, c.CreditHours, p.FirstName || ' ' || p.LastName as ProfessorName
        """
        self.course_id = course_id
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.credit_hours = credit_hours
        self.professor_id = professor_id
        self.professor_name = professor_name
