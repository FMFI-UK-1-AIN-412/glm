from typing import List
from argparse import ArgumentParser

from remote.context import Context
from remote.repository.utils import generate_report


def report_handler(args: List[str]):
    parser = ArgumentParser(
        prog="report", description="Generate and push report for students"
    )
    parser.add_argument(
        "report_path",
        action="store",
        type=str,
        help="Shell script file path that generates reports for students",
    )
    parser.add_argument(
        "--output-filename",
        action="store",
        metavar="filename",
        type=str,
        help="Name of the output file for the report. This will be pushed to students",
    )
    parsed_args = parser.parse_args(args)

    context = Context()

    output_filename = parsed_args.output_filename
    if output_filename is None:
        output_filename = context.report_file_name

    generate_report(
        context,
        report_command=parsed_args.report_command,
        output_filename=output_filename,
    )
