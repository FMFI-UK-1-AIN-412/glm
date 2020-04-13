from typing import List
from argparse import ArgumentParser

from remote.context import Context


def test_handler(args: List[str]):
    parser = ArgumentParser(prog="test", description="Test if glm is setup correctly")
    parser.parse_args(args)

    context = Context()
    test = context.get_test()
    test.do_tests()
