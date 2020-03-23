from typing import Optional, List


def distribute_branch(
    context: "Context",
    branch_name: str,
    repositories: Optional[List["Repository"]] = None,
):
    from core.core import get_current_remotes, get_all_branches

    print(" -- generating -- ")
    if repositories is None:
        repositories = get_student_repositories(context)

    print(" -- getting remotes and branches -- ")
    # TODO: also check if you are in octopus directory
    current_remotes = get_current_remotes()
    all_branches = get_all_branches()

    print(" -- pushing branches -- ")
    for repository in repositories:
        print(" -- adding remote -- ")
        repository.check_or_add_remotes(current_remotes)
        print(" -- branch distribution -- ")
        repository.distribute_branch(
            branch_name,
            check_location=False,
            check_if_remote_added=False,
            should_fetch=True,
            all_branches=all_branches,
        )


def generate_report(
    context: "Context",
    report_command: str,
    repositories: Optional[List["Repository"]] = None,
):
    from core.core import get_current_remotes

    if repositories is None:
        repositories = get_student_repositories(context)

    current_remotes = get_current_remotes()

    for repository in repositories:
        print(" -- adding remote -- ")
        repository.check_or_add_remotes(current_remotes)
        repository.generate_and_push_report(report_command)


def get_student_repositories(
    context: "Context", students: Optional[List["Student"]] = None,
) -> List["Repository"]:
    from student.utils import get_all_students

    if students is None:
        students = get_all_students(context)

    return [context.get_repository(student) for student in students]
