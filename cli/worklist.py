import argparse
import yaml
from plumbum.colors import fatal, warn, success
from typing import List, Tuple, Optional

from errors import GLMException
from core.config_loader import get_file_path, get_current_branch
from remote.context import Context
from student.student import Student, StudentFactory
from remote.pull_request.pull_request import PullRequest

Worklist = Tuple[Student, PullRequest]


def worklist_handler(args: List[str]):
    parser = argparse.ArgumentParser(
        prog="worklist", description="Worklist related functionality",
    )
    parser.add_argument("action", action="store", choices=["next", "prev", "list"])
    parsed_args = parser.parse_args(args)

    context = Context()

    worklist = get_worklist(context)
    current_worklist_index = get_current_worklist_index(worklist)

    if parsed_args.action == "list":
        list_worklist(worklist, current_worklist_index)
    elif parsed_args.action == "next":
        if current_worklist_index is None:
            worklist[0][1].checkout_pull_request()
        elif len(worklist) > current_worklist_index + 1:
            worklist[current_worklist_index + 1][1].checkout_pull_request()
        else:
            print("End of worklist")
    elif parsed_args.action == "prev":
        if current_worklist_index is None:
            worklist[-1][1].checkout_pull_request()
        elif current_worklist_index > 0:
            worklist[current_worklist_index - 1][1].checkout_pull_request()
        else:
            print("Start of worklist")


def get_worklist(context: Context) -> List[Worklist]:
    try:
        worklist_filepath = get_file_path("worklist.yaml")
    except FileNotFoundError:
        raise GLMException(
            "worklist.yaml doesn't exists", "You first need to create worklist"
        )

    with open(worklist_filepath) as file:
        parsed_worklist = yaml.safe_load(file)

    worklist = list()

    parsed_worklist_lines = set()

    for line in parsed_worklist:
        if line in parsed_worklist_lines:
            print(warn | f"Duplicity found, {line} has already been parsed")
            continue
        else:
            parsed_worklist_lines.add(line)

        worklist_line = parse_worklist_line(context, line)
        if worklist_line is not None:
            worklist.append(worklist_line)

    return worklist


def parse_worklist_line(context: Context, line: str) -> Optional[Worklist]:
    try:
        university_login, pr_number = line.split("#")
        pr_number = int(pr_number)
    except ValueError:
        print(warn | f"Error parsing ({line})")
        return

    student = StudentFactory.get_student(context, university_login)
    try:
        student.load_properties()
    except FileNotFoundError:
        print(fatal | f"Student ({university_login}) doesn't exist")
        return

    pull_request = context.get_pull_request(pr_number, student)
    try:
        pull_request.load_properties()
    except FileNotFoundError:
        print(
            fatal
            | f"Pull request with number = ({pr_number}) for student ({university_login}) doesn't exist locally"
        )
        return

    return student, pull_request


def get_current_worklist_index(worklist: Worklist) -> Optional[int]:
    current_branch = get_current_branch()
    if current_branch is None or "#" not in current_branch:
        return None

    university_login, pr_number = "", 0
    try:
        university_login, pr_number = current_branch.split("#")
        pr_number = int(pr_number)
    except ValueError:
        return None

    for index, worklist_item in enumerate(worklist):
        student, pr = worklist_item
        if student.university_login == university_login and pr.number == pr_number:
            return index

    return None


def list_worklist(worklist: Worklist, current_worklist_index: int):
    for index, worklist_item in enumerate(worklist):
        if index == current_worklist_index:
            print(success | "-> ", end="")
        else:
            print("   ", end="")

        print(worklist_item[1])
