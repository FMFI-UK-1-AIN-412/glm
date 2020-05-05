from typing import Tuple, List
from argparse import ArgumentParser

from remote.context import Context
from errors import WrongLocationException, GLMException
from student.student import Student, StudentFactory
from remote.pull_request.pull_request import PullRequest
from core.config_loader import (
    is_in_review_directory,
    get_review_path,
    get_current_branch,
)


def pull_handler(args: List[str]):
    parser = ArgumentParser(prog="pull", description="Pull request manipulation")
    parser.add_argument(
        "--comments", "-c", help="Load comments made on PR", action="store_true"
    )

    # Sub-parser: comment
    pull_sub_parsers = parser.add_subparsers()
    pull_sub_parsers_comment = pull_sub_parsers.add_parser(
        "comment", help="Comment on checked out pull request"
    )
    pull_sub_parsers_comment.add_argument("message", action="store", type=str)
    pull_sub_parsers_comment.set_defaults(func=pull_comment_handle)
    # Sub-parser: close
    pull_sub_parsers_comment = pull_sub_parsers.add_parser(
        "merge", help="Comment on checked out pull request"
    )
    pull_sub_parsers_comment.add_argument("message", action="store", type=str)
    pull_sub_parsers_comment.set_defaults(func=pull_merge_handle)

    parser_args = parser.parse_args(args)

    if hasattr(parser_args, "func"):
        parser_args.func(parser_args)
    else:
        context = Context()

        student, pull_request = get_checked_out_student_and_pull_request(context)

        if parser_args.comments:
            for issue in pull_request.get_issue_comments():
                print(issue)
        else:
            print(f"Currently checked out student = '{student}'")
            print(f"Currently checked out PR = '{pull_request}'")
            print(f"Can merge = {pull_request.mergeable}")


def pull_comment_handle(args):
    context = Context()

    _, pull_request = get_checked_out_student_and_pull_request(context)

    pull_request.create_issue_comment(args.message)


def pull_merge_handle(args):
    context = Context()

    _, pull_request = get_checked_out_student_and_pull_request(context)

    pull_request.merge_pull_request(args.message)


def get_checked_out_student_and_pull_request(
    context: "Context",
) -> Tuple[Student, PullRequest]:
    if not is_in_review_directory():
        raise WrongLocationException(
            "You are not in review directory", f"type: cd {get_review_path()}"
        )

    current_branch = get_current_branch()
    if current_branch is None or "#" not in current_branch:
        raise GLMException(
            "The current branch needs to be a PR student branch in format (university_login#number)"
        )

    student_university_login, number = current_branch.split("#")
    number = int(number)

    student = StudentFactory.get_student(context, student_university_login)
    student.load_properties()
    pull_request = context.get_pull_request(number, student)

    return student, pull_request
