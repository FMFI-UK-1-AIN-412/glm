from argparse import ArgumentParser
from typing import List

from remote.context import Context
from student.utils import get_students_from_university_logins
from remote.pull_request.pull_request import PullRequestState


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
    parser.add_argument(
        "--branch", "-b", help="Narrow pulls to specific branch", action="store",
    )

    parser.add_argument(
        "pr_status", help="Status of PR", choices=["open", "closed", "all"],
    )

    parsed_args = parser.parse_args(args)

    context = Context()

    students = None

    if parsed_args.students:
        students = get_students_from_university_logins(context, parsed_args.students)

    filters = {}

    if parsed_args.pr_status != "all":
        filters["status"] = PullRequestState(parsed_args.pr_status)

    if parsed_args.branch:
        filters["base_branch"] = parsed_args.branch

    pulls = []
    if parsed_args.cached:
        from remote.pull_request.utils import get_local_pull_requests

        pulls.extend(get_local_pull_requests(context, students, filters))
    else:
        from remote.pull_request.utils import get_remote_pull_requests

        pulls.extend(get_remote_pull_requests(context, students, filters))
        for pull in pulls:
            pull.save()

    if len(pulls) == 0:
        print("No pull requests")
    else:
        for pull in pulls:
            print(pull)
