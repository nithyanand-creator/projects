from store import save, load

students = [
    {"id": 1, "name": "Asha Rao", "email": "asha@school.test", "year": 1},
    {"id": 2, "name": "Ravi Kumar", "email": "ravi@school.test", "year": 2},
    {"id": 3, "name": "Meera Nair", "email": "meera@school.test", "year": 1},
    {"id": 4, "name": "Arjun Singh", "email": "arjun@school.test", "year": 3},
    {"id": 5, "name": "Divya Iyer", "email": "divya@school.test", "year": 2},
]
courses = [
    {"id": 1, "code": "CS101", "title": "Intro to Python", "credits": 4, "capacity": 3},
    {"id": 2, "code": "MA101", "title": "Calculus", "credits": 3, "capacity": 2},
    {"id": 3, "code": "PH101", "title": "Physics", "credits": 4, "capacity": 3},
    {"id": 4, "code": "EN101", "title": "English", "credits": 2, "capacity": 2},
]
enrollments = [
    {"id": 1, "student_id": 1, "course_id": 1, "grade": None},
    {"id": 2, "student_id": 2, "course_id": 1, "grade": None},
    {"id": 3, "student_id": 3, "course_id": 1, "grade": None},
    {"id": 4, "student_id": 1, "course_id": 2, "grade": None},
    {"id": 5, "student_id": 4, "course_id": 3, "grade": None},
    {"id": 6, "student_id": 5, "course_id": 4, "grade": None},
]
save("students", students)
save("courses", courses)
save("enrollments", enrollments)

print("students", len(students))
print("courses", len(courses))
print("enrollments", len(enrollments))

print(load("courses")[0]["code"])
print(load("enrollments")[0])