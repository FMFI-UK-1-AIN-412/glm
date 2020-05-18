from typing import List, Dict
from plumbum.colors import success, fatal
from github.GithubException import UnknownObjectException

from remote.context import Context
from errors import StudentDeleteException, RepositorySetupException, GLMException


class Organization:
    def __init__(self, context: Context):
        self.context = context

    def setup_student_repositories(self, students: List["Student"]):
        errors = []
        for student in students:
            try:
                self.setup_student_repository(student)
            except RepositorySetupException as error:
                if error.fatal:
                    print()
                    raise
                errors.append(error)

        if errors:
            print("Errors:")
            for error in errors:
                error.show()
            print(" --- ")

    def setup_student_repository(self, student):
        if not self.does_remote_repository_exists(student):
            print(
                f"Creating repository '{student.repository_name}' for '{student.name}'",
                end="",
            )
            try:
                self.create_remote_repository(student)
                print(" ...", success | "OK")
            except GLMException:
                print(" ...", fatal | "FAIL")
                raise

        repository = self.context.get_repository(student)

        if not repository.has_student_in_collaborators():
            print(
                f"Inviting '{student.name}' to collaborate on '{repository.name}'",
                end="",
            )
            try:
                repository.invite_student_to_collaborators()
                print(" ...", success | "OK")
            except RepositorySetupException:
                print(" ...", fatal | "FAIL")
                raise

    def delete_student_and_student_repository(self, student: "Student"):
        repository = self.get_repository(student)

        try:
            repository.delete()
        except UnknownObjectException:
            print(f"Cannot delete repository {repository.name} for {student.name}")
            return

        try:
            from student.utils import delete_student

            delete_student(student)
        except StudentDeleteException as error:
            error.show()

    def get_all_pull_requests(self) -> List["PullRequest"]:
        from student.utils import get_all_students

        pulls = []
        for student in get_all_students(self.context):
            pulls.extend(
                self.context.get_repository(student).get_remote_pull_requests()
            )

        return pulls

    def create_remote_repository(self, student: "Student"):
        raise NotImplementedError()

    def does_remote_repository_exists(self, student) -> bool:
        raise NotImplementedError()()

    def get_student_pull_requests(self, students: List["Student"]) -> Dict["Student", "PullRequest"]:
        raise NotImplementedError()()

    @property
    def name(self) -> str:
        if not hasattr(self, "__name") or self.__name is None:
            self.name = self.context.organization_name
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
