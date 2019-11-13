from remote.remote import Remote
from typing import List, Tuple

_remote = None

def add_student_repos(students: List[Tuple[str]], private: bool = True):
    global _remote
    _remote = _remote or Remote()
    remote = _remote
    for student in students:
        university_login, remote_login = student
        remote.create_repository(university_login, remote_login, private=private)

def delete_repo(university_login: str):
    global _remote
    _remote = _remote or Remote()
    remote = _remote
    remote.delete_repo(university_login)
