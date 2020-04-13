from argparse import ArgumentParser
from typing import List

from remote.context import Context
from student.utils import get_students_from_university_logins


def pulls_handler(args: List[str]):
    parser = ArgumentParser(prog="pulls", description="pull requests manipulation")
    parser.add_argument("--students", "-s", action="store")
    local_pulls_parser_group = parser.add_argument_group(
        "local", "arguments for manipulation of local pull requests"
    )
    local_pulls_parser_group.add_argument("--local", "-l", action="store_true")
    remote_pulls_parser_group = parser.add_argument_group(
        "remote", "arguments for manipulation of remote pull requests"
    )
    remote_pulls_parser_group.add_argument("--remote", "-r", action="store_true")
    remote_pulls_parser_group.add_argument(
        "--combine", choices=["replace", "merge"], action="store"
    )

    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        context = Context()

        students = None

        if parsed_args.students:
            students = get_students_from_university_logins(
                context, parsed_args.students.split(",")
            )

        if parsed_args.local:
            from remote.pull_request.utils import get_local_pull_requests

            pull_requests = get_local_pull_requests(context, students)
            if len(pull_requests) == 0:
                print("No pull requests")
            else:
                for pull in pull_requests:
                    print(pull)
        if parsed_args.remote:
            from remote.pull_request.utils import get_remote_pull_requests

            # TODO: you need to remove all the previous ones, or at least mark them as closed
            pull_requests = get_remote_pull_requests(context, students)
            if len(pull_requests) == 0:
                print("No pull requests")
            else:
                for pull in pull_requests:
                    print(pull)
                    pull.save()
