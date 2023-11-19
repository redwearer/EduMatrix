from faker import Faker
import random
import sqlite3

# Initialize the Faker library
fake = Faker()

# Number of entries to generate
num_students = 1000
num_professors = 100
num_courses = 75

# Generating lists for random selections
departments = ["Computer Science", "Biology", "Physics", "History", "Economics",
               "Mathematics", "Chemistry", "Engineering", "Psychology", "Political Science"]
academic_achievements = ["MBA", "BS", "BA", "PHD"]
degree_programs = ["Computer Science", "Biology", "Physics", "History", "Economics",
                   "Mathematics", "Chemistry", "Engineering", "Psychology", "Political Science",
                   "Art", "Music", "Philosophy", "Sociology", "Environmental Science",
                   "Law", "Medicine", "Business", "Literature", "Anthropology"]
course_names = ["Intro to Computer Science", "Advanced Biology", "Quantum Physics", "World History",
                "Microeconomics", "Calculus", "Organic Chemistry", "Mechanical Engineering",
                "Cognitive Psychology", "Political Theory", "Painting 101", "Music Theory",
                "Ethics", "Social Theory", "Climate Change", "Constitutional Law",
                "Medical Ethics", "Business Management", "Shakespearean Literature", "Cultural Anthropology",
                "Astronomy", "Neuroscience", "Creative Writing", "Urban Studies", "Film Studies"]

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('edumatrix.db')
cursor = conn.cursor()

# Inserting data into Professors table
for _ in range(num_professors):
    cursor.execute("INSERT INTO Professors (FirstName, LastName, Department, AcademicAchievement) VALUES (?, ?, ?, ?)",
                   (fake.first_name(), fake.last_name(), random.choice(departments), random.choice(academic_achievements)))

# Inserting data into Students table
for _ in range(num_students):
    cursor.execute("INSERT INTO Students (FirstName, LastName, Age, DegreeProgram, CompletedCredits, GPA) VALUES (?, ?, ?, ?, ?, ?)",
                   (fake.first_name(), fake.last_name(), random.randint(18, 25), random.choice(degree_programs),
                    random.randint(0, 120), round(random.uniform(2.0, 4.0), 2)))

# Inserting data into Courses table
for _ in range(num_courses):
    start_date = fake.date_between(start_date="-2y", end_date="-1y")
    end_date = fake.date_between(start_date=start_date, end_date="today")
    cursor.execute("INSERT INTO Courses (StartDate, EndDate, Name, CreditHours, ProfessorID) VALUES (?, ?, ?, ?, ?)",
                   (start_date, end_date, random.choice(course_names), random.randint(1, 4), random.randint(1, num_professors)))

# Commit the changes
conn.commit()

# Inserting data into Enrollments table
# For simplicity, each student is enrolled in a random number of courses
for student_id in range(1, num_students + 1):
    num_enrollments = random.randint(1, 5)  # Each student enrolls in 1 to 5 courses
    enrolled_courses = random.sample(range(1, num_courses + 1), num_enrollments)
    for course_id in enrolled_courses:
        grade = random.choice(['A', 'B', 'C', 'D', 'F', 'P', 'NP'])
        cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, Grade) VALUES (?, ?, ?)",
                       (student_id, course_id, grade))

# Commit the changes and close the connection
conn.commit()
conn.close()
