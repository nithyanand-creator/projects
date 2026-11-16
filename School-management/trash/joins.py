from store import load

def get_by_id(items, item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

def students_in_course(course_id):
    enrolls = load("enrollments")
    students = load("students")
    names = []
    for i in enrolls:
        if i["course_id"] == course_id:
            if not get_by_id(students, i["student_id"]):
                names.append(get_by_id(students, i["student_id"])["name"])
    return names

def courses_of_student(student_id):
    enrolls = load("enrollments")
    courses = load("courses")
    codes = []
    for i in enrolls:
        if i["student_id"] == student_id:
            if not get_by_id(courses, i["course_id"]):
                codes.append(get_by_id(courses, i["course_id"])["code"])
    return codes

def report():
    courses = load("courses")
    for i in courses:
        names = students_in_course(i["id"])
        print(f"{i["code"]}: {', '.join(names)}")

print(students_in_course(1))
print(courses_of_student(1))
print(get_by_id(load("students"), 99))
report()