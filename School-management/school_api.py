import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE = Path(__file__).parent
app = FastAPI()

class EnrollmentIn(BaseModel):
    student_id: int
    course_id : int

class Student(BaseModel):
    name: str
    email: str
    year: int

class Course(BaseModel):
    code: str
    title: str
    credits: int
    capacity: int

@app.get("/students")
def list_students(year: int | None = None, search: str = ""):
    result = []
    with open(BASE/"students.json", encoding="utf-8") as f:
        students = json.load(f)
        for student in students:
            if search != "":
                if year != None:
                    if student["year"] == year and search.lower() in student["name"].lower():
                        result.append(student)
                else:
                    if search.lower() in student["name"].lower():
                        result.append(student)
            else:
                if year != None:
                    if student["year"] == year:
                        result.append(student)
        if year == None and search == "":
            return students
    return result

@app.get("/enrollments")
def list_enrollments():
    with open(BASE/"enrollments.json", encoding="utf-8") as f:
        return json.load(f)

@app.get("/courses")
def list_courses(min_credits: int = 0, search: str = ""):
    result = []
    with open(BASE/"courses.json", encoding="utf-8") as f:
        courses = json.load(f)
        for course in courses:
            if search == "":
                if course["credits"] >= min_credits:
                    result.append(course)
            else:
                if search.lower() in course["title"].lower() and course["credits"] >= min_credits:
                    result.append(course)
        if min_credits == 0 and search == "":
            return courses
    return result

@app.get("/students/{student_id}")
def one_student(student_id: int):
    count = 0
    with open(BASE/"students.json", encoding="utf-8") as f:
        students = json.load(f)
        for student in students:
            if student["id"] == student_id:
                result = student
                count = 1
    if count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

@app.get("/courses/{course_id}")
def one_course(course_id: int):
    count = 0
    with open(BASE/"courses.json", encoding="utf-8") as f:
        courses = json.load(f)
        for course in courses:
            if course["id"] == course_id:
                count = 1
                result = course
    if count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return result

@app.get("/courses/{course_id}/students")
def student_in_course(course_id: int):
    result = []
    with open(BASE/"courses.json", encoding="utf-8") as f:
        courses = json.load(f)
        for course in courses:
            result.append(course["id"])
    if course_id not in result:
        raise HTTPException(status_code=404, detail="Course not found")
    result = []
    with open(BASE/"enrollments.json", encoding="utf-8") as f:
        enrollments = json.load(f)
        with open(BASE/"students.json", encoding="utf-8") as g:
            students = json.load(g)
            for enrollment in enrollments:
                if enrollment["course_id"] == course_id:
                    for student in students:
                        if student["id"] == enrollment["student_id"]:
                            result.append(student)
    return result

@app.get("/students/{student_id}/courses")
def course_with_students(student_id: int):
    result = []
    with open(BASE/"students.json", encoding="utf-8") as f:
        students = json.load(f)
        for student in students:
            result.append(student["id"])
    if student_id not in result:
        raise HTTPException(status_code=404, detail="Student not found")
    result = []
    with open(BASE/"enrollments.json", encoding="utf-8") as f:
        enrollments = json.load(f)
        with open(BASE/"courses.json", encoding="utf-8") as g:
            courses = json.load(g)
            for enrollment in enrollments:
                if enrollment["student_id"] == student_id:
                    for course in courses:
                        if course["id"] == enrollment["course_id"]:
                            result.append(course)
    return result

@app.post("/enrollments", status_code=201)
def enroll(body: EnrollmentIn):
    result = []
    with open(BASE/"students.json", encoding="utf-8") as f:
        students = json.load(f)
        with open(BASE/"courses.json", encoding="utf-8") as g:
            courses = json.load(g)
            with open(BASE/"enrollments.json", encoding="utf-8") as h:
                enrollments = json.load(h)
                for student in students:
                    result.append(student["id"])
                if body.student_id not in result:
                    raise HTTPException(status_code=404, detail="Student not found")
                result = []
                for course in courses:
                    result.append(course["id"])
                if body.course_id not in result:
                    raise HTTPException(status_code=404, detail="Course not found")
                result = []
                count = 0
                enrolled = 0
                for enrollment in enrollments:
                    if enrollment["course_id"] == body.course_id and enrollment["student_id"] == body.student_id:
                        count += 1
                    if enrollment["course_id"] == body.course_id:
                        enrolled += 1
                if count != 0:
                    raise HTTPException(status_code=400, detail="Already enrolled")
                for course in courses:
                    if course["id"] == body.course_id:
                        if course["capacity"] == enrolled:
                            raise HTTPException(status_code=400, detail="Course is full")
                        break
                new_id = 1
                result = []
                for enrollment in enrollments:
                    result.append(enrollment["id"])
                while new_id in result:
                    new_id += 1
                new_enroll = {"id": new_id, "student_id": body.student_id, "course_id": body.course_id, "grade": None}
                enrollments.append(new_enroll)
    with open(BASE/"enrollments.json", "w", encoding="utf-8") as i:
        json.dump(enrollments, i, indent=2)
    return new_enroll

@app.post("/students", status_code=201)
def add_student(student: Student):
    if student.name.strip() == "" :
        raise HTTPException(status_code=400, detail="Name is required")
    if "@" not in  student.email :
        raise HTTPException(status_code=400, detail="Invalid email")
    if not 1 <= student.year <= 4 :
        raise HTTPException(status_code=400, detail="Year must be between 1 and 4")
    with open(BASE/"students.json", encoding="utf-8") as f :
        students = json.load(f)
        for s in students:
            if s["email"].lower() == student.email.lower():
                raise HTTPException(status_code=400, detail="Email already exists")
        new_id = 1
        result = []
        for s in students:
            result.append(s["id"])
        while new_id in result:
            new_id += 1
        result = {"id": new_id, "name": student.name, "email": student.email, "year": student.year}
        students.append(result)
        with open(BASE/ "students.json", "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2)
        return result

@app.post("/courses", status_code=201)
def add_course(course: Course):
    if course.code == "":
        raise HTTPException(status_code=400, detail="Code is required")
    if course.title == "":
        raise HTTPException(status_code=400, detail="Title is required")
    if not 1 <= course.credits <= 6:
        raise HTTPException(status_code=400, detail="Credits must be between 1 and 6")
    if not course.capacity >= 1:
        raise HTTPException(status_code=400, detail="Capacity must be atleast 1")
    with open(BASE/ "courses.json", encoding="utf-8") as f:
        courses = json.load(f)
        for c in courses:
            if c["code"].lower() == course.code.lower():
                raise HTTPException(status_code=400, detail="Course code already exists")
        new_id = 1
        result = [c["id"] for c in courses]
        while new_id in result:
            new_id = new_id + 1
        result = {"id": new_id, "code": course.code, "title": course.title, "credits": course.credits, "capacity": course.capacity}
        courses.append(result)
        with open(BASE/ "courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2)
    return result

@app.put("/students/{student_id}", status_code=200)
def update_student(student: Student, student_id: int):
    with open("students.json", encoding="utf-8") as f:
        students = json.load(f)
        id = 0
        for s in students:
            if s["id"] == student_id:
                id = student_id
        if not id:
            raise HTTPException(status_code=404, detail="Student not found")
        if student.name.strip() == "" :
                raise HTTPException(status_code=400, detail="Name is required")
        if "@" not in  student.email :
            raise HTTPException(status_code=400, detail="Invalid email")
        if not 1 <= student.year <= 4 :
            raise HTTPException(status_code=400, detail="Year must be between 1 and 4")
        for s in students:
            if not s["id"] == student_id:
                if s["email"] == student.email:
                    raise HTTPException(status_code=400, detail="Email already exists")
        for s in students:
            if s["id"] == student_id:
                s["name"] = student.name
                s["email"] = student.email
                s["year"] = student.year
                result = s
                break
        with open(BASE/ "students.json", "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2)
        return f"updated {result}"

@app.put("/enrollments/{id}/grade", status_code=200)
def update_enrollment(id: int, grade: int):
    with open(BASE/ "enrollments.json", encoding="utf-8") as f:
        enrollments = json.load(f)
        result = []
        for e in enrollments:
            result.append(e["id"])
        if id not in result:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        if not 0 <= grade <= 100:
            raise HTTPException(status_code=400, detail="Grade must be between 0 and 100")
        for e in enrollments:
            if e["id"] == id:
                e["grade"] = grade
        with open(BASE/ "enrollments.json", "w", encoding="utf-8") as f:
            json.dump(enrollments, f, indent=2)
        return [dict(e) for e in enrollments if e["id"] == id]

@app.delete("/enrollments/{id}")
def delete_enrollment(id: int):
    with open(BASE/ "enrollments.json", encoding="utf-8") as f:
        enrollments = json.load(f)
        result = []
        for e in enrollments:
            result.append(e["id"])
        if id not in result:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        index = 0
        for x, y in enumerate(enrollments):
            if y["id"] == id:
                index = x
                break
        del enrollments[index]
        with open(BASE/ "enrollments.json", "w", encoding="utf-8") as f:
            json.dump(enrollments, f, indent=2)
    return {"message": f"Enrollment {id} deleted"}

@app.delete("/courses/{id}")
def delete_course(id: int):
    with open("courses.json", encoding="utf-8") as f:
        courses = json.load(f)
        ids = []
        for course in courses:
            ids.append(course["id"])
        if id not in ids:
            raise HTTPException(status_code=404, detail="Course not found")
        index = 0
        for x, y in enumerate(courses):
            if y["id"] == id:
                index = x
        del courses[index]
        with open(BASE/ "courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2)
    return {"message": f"Course {id} deleted"}

@app.delete("/students/{id}")
def delete_student(id: int):
    with open(BASE/ "students.json", encoding="utf-8") as f:
        students = json.load(f)
        ids = []
        for s in students:
            ids.append(s["id"])
        if id not in ids:
            raise HTTPException(status_code=404, detail="Student not found")
        index = 0
        for x, y in enumerate(students):
            if y["id"] == id:
                index = x
        del students[index]
        with open(BASE/ "students.json", "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2)
    return {"message": f"Student {id} deleted"}

