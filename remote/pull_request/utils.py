import os
from typing import List, Optional, Any, Dict

from remote.context import Context
from core.config_loader import get_directory_path, get_local_config_path


def get_local_pull_requests(
    context: Context,
    students: Optional[List["Student"]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> List["PullRequest"]:
    from student.student import StudentFactory
    from core.config_loader import get_directory_path

    if students is None:
        students = [
            StudentFactory.get_student(context, student_name)
            for student_name in os.listdir(get_directory_path("pulls/"))
        ]

    pulls = []
    for student in students:
        for student_pull_file in os.listdir(student.pulls_directory_path()):
            pr = context.get_pull_request(student_pull_file, student)
            if pr.passes_filters(filters):
                pulls.append(pr)

    return pulls


def get_remote_pull_requests(
    context: Context,
    students: Optional[List["Student"]] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> List["PullRequest"]:
    from remote.repository.utils import get_student_repositories

    pulls = []
    all_repositories = get_student_repositories(context, students)
    for repository in all_repositories:
        for pr in repository.get_remote_pull_requests():
            if pr.passes_filters(filters):
                pulls.append(pr)

    return pulls


def create_student_pulls_directory(student) -> str:
    try:
        pulls_directory_path = get_directory_path("pulls/")
    except FileNotFoundError:
        pulls_directory_path = f"{get_local_config_path()}/pulls/"
        os.mkdir(pulls_directory_path)
    finally:
        student_pulls_directory_path = pulls_directory_path + student.file_name
        os.mkdir(student_pulls_directory_path)
        print(
            f"Creating pulls directory for {student.university_login} at {student_pulls_directory_path}"
        )
        return student_pulls_directory_path
