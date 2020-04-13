from typing import List
from argparse import ArgumentParser

from remote.context import Context
from remote.repository.utils import distribute_branch


def distribute_handler(args: List[str]):
    parser = ArgumentParser(prog="distribute", description="Distribute branches")
    parser.add_argument("branch_name", type=str, action="store")
    parsed_args = parser.parse_args(args)

    context = Context()

    distribute_branch(context, parsed_args.branch_name)
