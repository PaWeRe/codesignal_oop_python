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

## 6) Delete element(s) in dict or list (messagingapp.py, delete_user(), filehostingsystem.py)
    a) List comprehension filtering for deletion:
       user.wasblocked = [b for b in user.wasblocked if b.username != username]
       user.wantstoblock = [b for b in user.wantstoblock if b.username != username]
    b) Direct deletion with del:
       del self.children[name]  # from Directory class delete()
    c) Remove from list:
       self.users.remove(target)  # from messagingapp.py delete_user()
       pet.assigned.pets.remove(pet)  # from pethotel.py check_out()

## 7) Path and string manipulation (filehostingsystem.py)
    a) Path splitting:
       path_parts = path.split("/")  # split path into components
       file_name = path_parts[-1]    # get last component (file name)
       parent_path = path_parts[:-1]  # get all but last component
    b) String checks:
       value.name.startswith(prefix)  # check if string starts with prefix
    c) Path traversal:
       for part in path_parts[:-1]:   # iterate through all but last component
           current = current.get(part)

## 8) Deep copy for objects (filehostingsystem.py, _save_state())
    self.state_history[timestamp] = copy.deepcopy(self.root) # import copy necessary

## 9) List filtering with list comprehension (filehostingsystem.py, FILE_SEARCH_AT())
    not_dead = [f for f in prefix_list if not f.ttl or f.ttl > timestamp]

## 10) Multiple conditions in list comprehension (messagingapp.py, delete_user())
    user.wasblocked = [b for b in user.wasblocked if b.username != username]

## 11) Tuple returns for data structures (pethotel.py, list_pets())
    return [(pet.name, pet.species, pet.belongs_to.name) for pet in self.pets]

## 12) Dictionary as a timestamp-based storage (messagingapp.py)
    self.received = dict()  # key timestamp, value msg
    self.sent = dict()  # key timestamp, value msg

## 13) Finding max with condition (filehostingsystem.py, ROLLBACK())
    closest = max(valid_times)  # finds most recent valid timestamp

## 14) Recursive traversal with accumulator (filehostingsystem.py, _recursive_dfs())
    def _recursive_dfs(self, current_dir: Directory, prefix: str):
        all_files = []
        for key, value in current_dir.children.items():
            if isinstance(value, File) and value.name.startswith(prefix):
                all_files.append(value)
            if isinstance(value, Directory):
                all_files.extend(self._recursive_dfs(value, prefix))
        return all_files

## 15) Type hints and abstract base classes (messagingapp.py)
    from abc import ABC, abstractmethod
    class AppBase(ABC):
        @abstractmethod
        def create_user(self, username: str) -> bool:
            pass

## Advanced Algorithms and Patterns
Common patterns found in OOP coding assessments:

1) Recursive Tree/Graph Traversal (filehostingsystem.py, _recursive_dfs())
   ```python
   def _recursive_dfs(self, current_dir, prefix):
       all_files = []
       for key, value in current_dir.children.items():
           if isinstance(value, File) and value.name.startswith(prefix):
               all_files.append(value)
           if isinstance(value, Directory):
               all_files.extend(self._recursive_dfs(value, prefix))
       return all_files
   ```

2) Interval Overlap Detection (confscheduling.py, register_for_talk())
   ```python
   def overlaps(talk1, talk2):
       return not (talk1.end_time <= talk2.start_time or talk1.start_time >= talk2.end_time)
   ```

3) State Management with History (filehostingsystem.py)
   ```python
   def _save_state(self, timestamp):
       self.state_history[timestamp] = copy.deepcopy(self.root)
   ```

4) Bidirectional Reference Management (messagingapp.py, block_user())
   ```python
   if blocker_obj not in blockee_obj.wasblocked:
       blockee_obj.wasblocked.append(blocker_obj)
   if blockee_obj not in blocker_obj.wantstoblock:
       blocker_obj.wantstoblock.append(blockee_obj)
   ```

5) Resource Allocation with Constraints (studentscheduling.py)
   ```python
   # Check capacity
   if course.max_students <= len(course.enrolled_students):
       raise Exception("Max number of students in course reached.")
   # Check credit limit
   current_credits = sum(c.credits for c in student.enrolled_courses)
   if current_credits + course.credits > 18:
       raise Exception("Student has exceeded max number of credits.")
   ```

6) Conflict Detection in Scheduling (studentscheduling.py)
   ```python
   slots = set()
   for course in student.enrolled_courses:
       for slot in course.schedule:
           if slot in slots:
               return False
           slots.add(slot)
   ```

## Bonus: OOP Design Tips
- Use __init__ to initialize everything (e.g. self.schedule = [])
- Keep references in both objects if relationships are bidirectional
- Use dicts for quick lookup and mapping
- Add helper methods like has_schedule_conflict() or get_total_credits()