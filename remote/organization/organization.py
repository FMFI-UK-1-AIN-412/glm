from typing import List, Optional
from github.GithubException import UnknownObjectException

from remote.context import Context
from errors import StudentDeleteException, RepositoryCreationException


class Organization:
    def __init__(self, context: Context):
        self.context = context
        self.remote_organization = None

    def create_repositories(self, students: List["Student"]):
        errors = []
        for student in students:
            try:
                self.create_repository(student)
            except RepositoryCreationException as error:
                if error.fatal:
                    print()
                    raise
                errors.append(error)

        if errors:
            print("Errors:")
            for error in errors:
                error.show()
            print(" --- ")

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

    def create_repository(self, student: "Student") -> Optional[str]:
        raise NotImplementedError()

    def does_remote_repository_exists(self, student) -> bool:
        raise NotImplementedError()()

    @property
    def name(self) -> str:
        if not hasattr(self, "__name") or self.__name is None:
            self.name = self.context.organization_name
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def remote_organization(self):
        if self.__remote_organization is None:
            self.__remote_organization = self.context.remote.get_organization(
                self.context.organization_name
            )
        return self.__remote_organization

    @remote_organization.setter
    def remote_organization(self, value):
        self.__remote_organization = value
