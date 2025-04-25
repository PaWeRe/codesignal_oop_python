# Cheatsheet - useful python functions

## 1) Object look up in list (in studentscheduling.py, enroll_student_in_course())
    student = next((s for s in self.students if s.student_id == student_id), None)
    course = next((c for c in course if c.course_id == course_id), None)
    if not student:
        raise Exception("Studnet must be registered first.")
    if not course:
        raise Exception("Course must be registered first.")

## 2) Membership checking (in studentscheduling.py, check_student_schedule_conflicts())
    slots = set()
    for course in student.enrolled_courses:
        for slot in course.schedule: # list of (day,time_slot) elements
            if slot in slots:
                return False
            slots.add(slot)
    return True

## 3) Sum with comprehensions (in studentscheduling.py, enroll_student_in_course())
    current_credits = sum(c.credits for c in student.enrolled_courses)

## 4) Sorting with custom keys (messagingapp.py, get_messages(), filehostingsystem.py)
    a) return [receiver.received[t] for t in sorted(receiver.received, reverse=False)] # key - timestamp, value - msg (for values of dict use ".value()")
    b) prefix_list.sort(key = lambda f: (-f.size, f.name))

## 5) Checking overlap with start and end time (confscheduling.py, register_for_talk())
    def overlaps(talk1, talk2):
        return not (talk1.end_time <= talk2.start_time or talk1.start_time >= talk2.end_time)

## 6) Delete element(s) in dict or list (messagingapp.py, delete_user(), filehostingsystem.py, Directory class delete())
    a) list comprehension 
    b) Del keyword

## 7) basic string manipulation (...)
     path.split("/")
     path.strip("hola")
     path_parts[-1]
     path_parts[:-1]
     value.name.startswith(prefix), prefix="holabuenas"

## 8) basic algorithms (leetcode easy)


## Bonus: OOP Design Tips
- Use __init__ to initialize everything (e.g. self.schedule = [])
- Keep references in both objects if relationships are bidirectional
- Use dicts for quick lookup and mapping
- Add helper methods like has_schedule_conflict() or get_total_credits()