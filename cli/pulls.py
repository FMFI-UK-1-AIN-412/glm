from argparse import ArgumentParser
from typing import List

from remote.context import Context
from student.utils import get_students_from_university_logins


def pulls_handler(args: List[str]):
    parser = ArgumentParser(prog="pulls", description="pull requests manipulation")
    parser.add_argument(
        "--students",
        "-s",
        nargs="+",
        action="store",
        metavar="students",
        help="List of students",
    )
    parser.add_argument(
        "--cached", "-c", help="Load PR from localconfig", action="store_true"
    )

    parsed_args = parser.parse_args(args)

    context = Context()

    students = None

    if parsed_args.students:
        students = get_students_from_university_logins(context, parsed_args.students)

    pulls = []
    if parsed_args.cached:
        from remote.pull_request.utils import get_local_pull_requests

        pulls.extend(get_local_pull_requests(context, students))
    else:
        from remote.pull_request.utils import get_remote_pull_requests

        pulls.extend(get_remote_pull_requests(context, students))
        for pull in pulls:
            pull.save()

    if len(pulls) == 0:
        print("No pull requests")
    else:
        for pull in pulls:
            print(pull)
