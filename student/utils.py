import os
from typing import List, Tuple

from core.config_loader import get_root_directory


def get_all_students(context: "Context") -> List["Student"]:
    from student.student import Student
    from core.config_loader import directory_path, get_local_config, DirectoryNotFound

    student_directory = ""
    try:
        student_directory = directory_path("active/")
    except DirectoryNotFound:
        print("Creating active directory in localconfig")
        local_config_directory = get_local_config()
        os.mkdir(f"{local_config_directory}/active/")
        student_directory = f"{local_config_directory}/active/"

    students = []
    for student_file in os.listdir(directory_path("active/")):
        students.append(Student(context, university_login=student_file))

    return students


def delete_student(student: "Student") -> bool:
    # TODO: this uses the previous version of active, now you can have active directory in localconfig and in config so this will obviously not work
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


def generate_students(context, file_path: str) -> List["Student"]:
    from core.core import read_lines
    from student.student import Student

    students = get_all_students(context)

    active_students_university_login = set(
        student.university_login for student in students
    )

    for line in read_lines(file_path):
        university_login, remote_login, name, email = line.split(" ")
        if university_login in active_students_university_login:
            print(f"student with university login = {university_login} already exists, skipping")
        else:
            student = Student(context, university_login, remote_login, name, email)
            student.save()
            print(f"student ({student}) created and saved")
            students.append(student)

    return students


def active_students() -> List[Tuple[str, str]]:
    from core.core import read_line_file
    students = []
    root_directory = get_root_directory()
    for file_name in os.listdir(root_directory + "/active"):
        student = read_line_file(f"{root_directory}/active/{file_name}")
        students.append((file_name, student))
    return students
