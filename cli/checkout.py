from typing import List
from argparse import ArgumentParser

from remote.context import Context
from student.utils import get_all_students


def checkout_handler(args: List[str]):
    parser = ArgumentParser(prog="checkout", description="Checkout student PR")
    parser.add_argument("university_login", action="store", type=str)
    parser.add_argument("pr_number", action="store", type=int)

    parsed_args = parser.parse_args(args)

    checkout(parsed_args)


def checkout(args):
    context = Context()
    university_login = args.university_login
    student = list(
        filter(
            lambda x: x.university_login == university_login, get_all_students(context),
        )
    )

    if len(student) != 1:
        print(
            f"No student with university login=({university_login}) found in active students"
        )
    else:
        student = student[0]
        student_repository = context.get_repository(student)
        pull_number = args.pr_number

        pulls = list(
            filter(
                lambda x: x.number == pull_number,
                student_repository.get_local_pull_requests(),
            )
        )

        if len(pulls) != 1:
            print(
                f"Pull request for {student} with number = ({pull_number}) was not found fetching new pull requests"
            )
            pulls = list(
                filter(
                    lambda x: x.number == pull_number,
                    student_repository.get_remote_pull_requests(),
                )
            )

            if len(pulls) != 1:
                print("Pull request does not exists")
                return

        pull_request = pulls[0]
        pull_request.save()
        pull_request.checkout_pull_request()
