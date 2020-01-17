import os
from typing import List, Tuple, Optional, Any


def get_all_students() -> List[Any]:
    from student.student import Student
    from core.config_loader import directory_path
    students = []
    for student_file in os.listdir(directory_path("active/")):
        students.append(Student(university_login=student_file))

    return students
