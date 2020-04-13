import argparse
from typing import List

from remote.context import Context
from student.utils import generate_students as utils_generate_students


def generate_handler(args: List[str]):
    parser = argparse.ArgumentParser(
        prog="generate", description="Command for generating students",
    )
    parser.add_argument(
        "file_path", action="store", type=str, help="file for generating students",
    )
    parsed_args = parser.parse_args(args)

    generate_students(parsed_args.file_path)


def generate_students(file_path: str):
    context = Context()

    students = utils_generate_students(context, file_path)
    context.organization.setup_student_repositories(students)
