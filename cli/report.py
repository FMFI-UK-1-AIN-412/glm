from remote.context import Context


def handle_args(args):
    from remote.repository.utils import generate_report

    context = Context()

    generate_report(context, report_command=args.report_command)
