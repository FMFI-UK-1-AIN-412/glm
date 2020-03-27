from remote.context import Context
from errors import WrongLocationException, GLMException
from student.utils import get_all_students
from core.config_loader import (
    is_in_octopus_directory,
    get_octopus_path,
    get_current_branch,
)


def pulls_handle(args):
    context = Context()

    if args.local:
        from remote.pull_request.utils import get_local_pull_requests

        pull_requests = get_local_pull_requests(context)
        for pull in pull_requests:
            print(pull)
    if args.remote:
        from remote.pull_request.utils import get_remote_pull_requests

        # TODO: you need to remove all the previous ones, or at least mark them as closed
        pull_requests = get_remote_pull_requests(context)
        for pull in pull_requests:
            print(pull)


def pulls_comment_handle(args):
    from student.student import Student

    context = Context()

    if not is_in_octopus_directory():
        raise WrongLocationException(
            "You are not in octopus directory", f"type: cd {get_octopus_path()}"
        )

    current_branch = get_current_branch()
    if current_branch is None or "#" not in current_branch:
        raise GLMException(
            "The current branch needs to be a PR student branch in format (university_login#number)"
        )

    student_university_login, number = current_branch.split("#")
    number = int(number)

    student = Student(context, student_university_login)
    student.load_properties()
    pull_request = context.get_pull_request(number, student)

    pull_request.create_issue_comment(args.message)


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
