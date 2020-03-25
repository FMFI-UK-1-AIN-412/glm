from remote.context import Context
from student.utils import generate_students


def handle_args(args):
    context = Context()

    file_path = args.file_path
    students = generate_students(context, file_path)
    context.organization.create_repositories(students)
