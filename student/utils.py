import os
from typing import List, Tuple

from core.config_loader import get_root_directory


def get_all_students() -> List["Student"]:
    from student.student import Student
    from core.config_loader import directory_path
    students = []
    for student_file in os.listdir(directory_path("active/")):
        students.append(Student(university_login=student_file))

    return students


def save_student(university_login: str, remote_login: str):
    root_directory = get_root_directory()
    path = root_directory + "/active/"
    if os.path.exists(path + university_login):
        print(f"File for {university_login} already exists")
    else:
        try:
            f = open(root_directory + "/active/" + university_login, "w")
            f.write(remote_login + "\n")
            f.close()
        except:
            print(f"Error while writing file {university_login}")


def delete_student(student: "Student") -> bool:
    if os.path.exists("./active/" + student.university_login):
        try:
            os.remove("./active/" + student.university_login)
            print(
                f"Student {student.university_login} removed from active students"
            )
            return True
        except:
            print(
                f"Failed removing {student.university_login} from active students"
            )
    else:
        print(f"Student {student.university_login} is an active student")
    return False


def active_students() -> List[Tuple[str, str]]:
    from core.core import read_line_file
    students = []
    root_directory = get_root_directory()
    for file_name in os.listdir(root_directory + "/active"):
        student = read_line_file(f"{root_directory}/active/{file_name}")
        students.append((file_name, student))
    return students
