from remote.context import Context
from student.utils import get_all_students, get_students_from_university_logins


def pulls_handle(args):
    context = Context()

    students = None

    if args.students:
        students = get_students_from_university_logins(
            context, args.students.split(",")
        )

    if args.local:
        from remote.pull_request.utils import get_local_pull_requests

        pull_requests = get_local_pull_requests(context, students)
        if len(pull_requests) == 0:
            print("No pull requests")
        else:
            for pull in pull_requests:
                print(pull)
    if args.remote:
        from remote.pull_request.utils import get_remote_pull_requests

        # TODO: you need to remove all the previous ones, or at least mark them as closed
        pull_requests = get_remote_pull_requests(context, students)
        if len(pull_requests) == 0:
            print("No pull requests")
        else:
            for pull in pull_requests:
                print(pull)


def pulls_checkout_handle(args):
    context = Context()
    university_login = args.checkout[0]
    student = list(
        filter(
            lambda x: x.university_login == university_login, get_all_students(context),
        )
    )

    if len(student) != 1:
        print(
            f"No student with university login=({university_login}) found in active students"
        )
    else:
        student = student[0]
        student_repository = context.get_repository(student)
        try:
            pull_id = int(args.checkout[1])
        except ValueError:
            print("Pull id needs to be integer")
            return

        pulls = list(
            filter(
                lambda x: x.id == pull_id, student_repository.get_local_pull_requests(),
            )
        )

        if len(pulls) != 1:
            print(
                f"Pull request for {student} with id = ({pull_id}) was not found fetching new pull requests"
            )
            pulls = list(
                filter(
                    lambda x: x.id == pull_id,
                    student_repository.get_remote_pull_requests(),
                )
            )

            if len(pulls) != 1:
                print("Pull request does not exists")
                return

        pull_request = pulls[0]
        pull_request.save()
        pull_request.checkout_pull_request()
