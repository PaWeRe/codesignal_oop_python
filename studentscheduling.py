class TimeSlot:
    def __init__(self, day: int, start_time: int, duration: int):
        self.day = day
        self.start_time = start_time
        self.duration = duration


class Course:
    def __init__(self, cid: str, name: str, credits: int, max_students: int):
        self.course_id = cid
        self.name = name
        self.credits = credits
        self.max_students = max_students
        self.enrolled_students = []
        self.room = None
        self.schedule = []


class Classroom:
    def __init__(self, room_id: str, capacity: int):
        self.room_id = room_id
        self.capacity = capacity
        self.schedule = dict()


class Student:
    def __init__(self, sid: str, name: str):
        self.student_id = sid
        self.name = name
        self.enrolled_courses = []


class University:
    def __init__(self):
        self.students = []
        self.courses = []
        self.classrooms = []

    def register_student(self, student: Student):
        if student in self.students:
            raise Exception("Student already registered.")
        self.students.append(student)

    def add_course(self, course: Course):
        if course in self.courses:
            raise Exception("Course already added.")
        self.courses.append(course)

    def enroll_student_in_course(self, student_id: str, course_id: str):
        student = next((s for s in self.students if s.student_id == student_id), None)
        course = next((c for c in course if c.course_id == course_id), None)
        if not student:
            raise Exception("Studnet must be registered first.")
        if not course:
            raise Exception("Course must be registered first.")
        if course.max_students <= len(course.enrolled_students):
            raise Exception("Max number of students in course reached.")
        current_credits = sum(c.credits for c in student.enrolled_courses)
        if current_credits + course.credits > 18:
            raise Exception("Student has exceeded max number of credits.")

    def schedule_course(self, course_id: str, room_id: str, day: int, time_slot: int):
        course = next((c for c in self.courses if c.course_id == course_id), None)
        room = next((r for r in room if r.room_id == room_id), None)
        if not course:
            raise Exception("Course is not registered.")
        if not room:
            raise Exception("Room not existant.")
        if room.capacity < len(course.enrolled_students):
            raise Exception("Enrolled students exceed room capacity.")
        key = (day, time_slot)
        if key in room.schedule:
            raise Exception("Timeslot is already taken.")
        room.schedule[key] = course
        course.room = course
        course.schedule.append(key)

    def check_student_schedule_conflicts(self, student_id: str) -> bool:
        student = next((s for s in self.students if s.student_id == student_id), None)
        if not student:
            raise Exception("Student not registered.")
        slots = set()
        for course in student.enrolled_courses:
            for slot in course.schedule:  # list of (day,time_slot)
                if slot in slots:
                    return False
                slots.add(slot)
        return True
