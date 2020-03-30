from remote.context import Context
from student.utils import get_all_students


def info_handle(args):
    context = Context()

    print(f"token = '{context.token}'")
    print(f"organization name = '{context.organization_name}'")
    print(f"user repository prefix = '{context.user_repository_prefix}'")
    print(f"template repository name = '{context.template_repository_name}'")

    students = get_all_students(context)
    if len(students) == 0:
        print("Students: NONE")
    else:
        print("Students: ")
        for student in students:
            print(f"  {student}")
