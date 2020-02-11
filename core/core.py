import os
from subprocess import check_output, DEVNULL

from core.config_loader import get_root_directory
from typing import List, Tuple, Optional

def get_organization_name() -> str:
    return "glm-testing"

def user_repository_prefix() -> str:
    return "osprog18-"

def get_template_name() -> str:
    return "osprog18"

def get_repo_name(university_login: str) -> str:
    return user_repository_prefix() + university_login

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
            print(f"Student {student.university_login} removed from active students")
            return True
        except:
            print(f"Failed removing {student.university_login} from active students")
    else:
        print(f"Student {student.university_login} is an active student")
    return False

def active_students() -> List[Tuple[str, str]]:
    students = []
    root_directory = get_root_directory()
    for file_name in os.listdir(root_directory + "/active"):
        student = read_line_file(f"{root_directory}/active/{file_name}")
        students.append((file_name, student))
    return students

def get_token() -> Optional[str]:
    root_directory = get_root_directory()
    return read_line_file(root_directory + "/token")

def read_line_file(filename) -> Optional[str]:
    try:
        with open(filename) as f:
            line = f.readline()
            if line[-1] == "\n":
                line = line[:-1]
            return line
    except:
        return None

def shell_command(command: str) -> Optional[str]:
    try:
        command_list = [command]
        if " " in command:
            command_list = command.split(" ")
        output = check_output(command_list).decode("utf-8")[:-1]
        if output:
            return output
        if output != "":
            print(f"Wrong formatted $GLM_PATH, current value = {output}")
    except:
        return None

def stats(short=False):
    if not short:
        print("Printing database summary")
    print(f"user repo prefix = {user_repository_prefix()}")
    print(f"organization name = {get_organization_name()}")
    if not short:
        students = "".join(map(lambda x: "\t" + x[0] + " -> " + x[1] + "\n", active_students()))
        print(f"active stundets = \n {students}")

if __name__ == "__main__":
    stats()
