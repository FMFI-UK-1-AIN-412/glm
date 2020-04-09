from remote.context import Context
from remote.repository.utils import distribute_branch


def distribute_handle(args):
    context = Context()

    distribute_branch(context, args.branch_name)
