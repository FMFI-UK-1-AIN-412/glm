from typing import List
from plumbum.colors import fatal
from argparse import ArgumentParser

from core.core import get_exit_code
from errors import WrongLocationException
from remote.context import Context
from remote.repository.utils import get_student_repositories
from student.utils import get_students_from_university_logins
from core.core import get_current_remotes, get_all_branches
from core.config_loader import is_in_octopus_directory, get_octopus_path


def distribute_handler(args: List[str]):
    parser = ArgumentParser(prog="distribute", description="Distribute branches")
    parser.add_argument("branch_name", type=str, action="store")
    parser.add_argument(
        "--students",
        "-s",
        type=str,
        action="store",
        default="",
        help="Comma separated university logins",
    )
    parsed_args = parser.parse_args(args)

    context = Context()

    distribute_branch(context, parsed_args.branch_name, parsed_args.students)


def distribute_branch(
    context: "Context", branch_name: str, students: str,
):
    if not is_in_octopus_directory():
        raise WrongLocationException(
            "You are not in octopus directory", f"type: cd {get_octopus_path()}"
        )

    if not does_remote_branch_exist("origin", branch_name):
        print(fatal | f"{branch_name} doesn't exist on origin, nothing to push")
        return

    if len(students) == 0:
        students = []
    else:
        students = students.split(",")

    students_list = get_students_from_university_logins(context, students)

    if len(students) != 0 and len(students_list) == 0:
        return

    repositories = get_student_repositories(context, students_list)

    current_remotes = get_current_remotes()
    all_branches = get_all_branches()

    for repository in repositories:
        repository.check_or_add_remotes(current_remotes)
        repository.distribute_branch(branch_name, all_branches=all_branches)


def does_remote_branch_exist(remote: str, branch_name: str) -> bool:
    code = get_exit_code(f"git fetch {remote} {branch_name}", True, True)
    return code == 0
