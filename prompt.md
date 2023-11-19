I am building a software application for my senior project for my bachelors degree in computer science.

The application that I will be building is called EduMatrix.

This application will be a university management system.

It will contain data on:

- Students (To include First Name, Last name, Age, Degree program, Completed credits, GPA, currently enrolled courses, and grade in each course)
- Professors (To include First Name, Last name, Teaching department, Level of academic achievment and subject i.e. PHD in mathematics, and courses currently teaching)
- Courses (To include start date, end date, name, number of credit hours, professor teaching the course, and students enrolled in the course)

Relationships and Junction Tables:
- Students-Courses Relationship (Many-to-Many):
  - Junction Table: Perhaps named Enrollments.
  - Attributes: StudentID, CourseID, Grade.
  - This table represents which students are enrolled in which courses and their grades in those courses.
 - Professors-Courses Relationship (One-to-Many):
  - The Courses table should have a ProfessorID foreign key.
  - This indicates which professor is teaching a particular course.
  - A professor can teach multiple courses, but each course is taught by only one professor.


The application should be able to create, read, update, and delete students, professors, and courses

The application should prompt for a username and password when launched. The username should be'admin' and the password should be 'admin'. These credentialed should be set in the python code.

Implementation details:

- The application should be written in python
- The application GUI should be created with PyQT5
- The data should be stored in SQLite3 database files (1 file or several. I will leave that decision to you)
- I would like the application to check for a database file on startup, and if one exists, it will read from and write to the existing database. If the database doesn't exist, it will create one with the appropriate schema.
- I would like the GUI to have a tabbed layout, i.e. a tab for students, a tab for courses, and a tab for professors.

I would like this application to be a python package, so it will need a pyproj.toml and a setup.py

I would like you to walk me through how you would architect this application before you begin generating any code. By that I mean I would like you to specify the entire file/directory structure. Additionally, I would like you to list and briefly describe every single class, method, and function.

When you are generating code, I want you generate all of the code in it's entirety. If a section of code will be large, generate it in smaller pieces.

I would like all code to by type-hinted and to have numpy-style docstrings.

When generating python, I would like you to put a comment line at the top of each code block indicating which file it belongs in. i.e.:
# HelloWorld.py

Do you have any questions, or require any clarification before you begin?


EduMatrix/
│
├── edumatrix/               # Main application package
│   ├── __init__.py
│   ├── main.py              # Entry point of the application
│   ├── database.py          # Database interactions
│   ├── models.py            # Data models (Students, Professors, Courses)
│   ├── views.py             # GUI components
│   ├── controllers.py       # Business logic
│   └── utils.py             # Utility functions
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_models.py
│
├── setup.py                 # Setup script for package installation
└── pyproject.toml           # Package metadata and dependencies


Detailed Architecture Plan
1. Main Application Structure
main.py:
MainApplication: Initializes and starts the PyQt5 application. Handles the login process.
2. Database Management
database.py:
DatabaseManager: Manages SQLite database connections, creation, and schema initialization. Methods will include initialize_database, create_tables, and CRUD operations for each entity.
3. Data Models
models.py:
Student: Attributes include name, age, degree program, credits, GPA, etc.
Professor: Attributes include name, department, academic achievement, etc.
Course: Attributes include dates, credit hours, professor, enrolled students, etc.
4. Graphical User Interface
views.py:
BaseView: A common base for all views.
StudentView, ProfessorView, CourseView: Specific classes for each tab in the GUI.
5. Business Logic
controllers.py:
Functions that integrate the views with the models, handling the logic for creating, reading, updating, and deleting data.
6. Utility Functions
utils.py:
Includes helper functions for the application, such as data validation.
7. Testing
tests/:
Contains unit tests for different components of the application.
8. Packaging
setup.py and pyproject.toml:
For packaging the application as a Python package.
Implementation Strategy
Start with Database Setup:
Initialize the SQLite database and define the schema.
Develop Data Models:
Implement Student, Professor, and Course classes.
Implement Business Logic:
Develop the functionality to manipulate the data models (CRUD operations).
Build the GUI:
Design and implement the GUI using PyQt5.
Integrate All Components:
Ensure all parts of the application work seamlessly together.
Testing and Documentation:
Write tests for each component and document the code thoroughly.