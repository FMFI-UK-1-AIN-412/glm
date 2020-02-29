from typing import List, Optional
from github.GithubException import UnknownObjectException

from remote.context import Context


class Organization:
    def __init__(self, context: Context):
        self.context = context
        self.name = None

    def create_repositories(self, students: List["Student"]):
        errors = []
        for student in students:
            error = self.create_repository(student)
            if error:
                errors.append(error)

        if errors:
            print("Errors:")
            print("\n".join(errors))
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
        except:
            print(f"Cannot delete student {student.name}")

    def get_student_git_ssh_remote_url(self, student: "Student"):
        return f"{self.context.git_remote_url_prefix}{self.name}/{student.remote_login}.git"

    def create_repository(self, student: "Student") -> Optional[str]:
        """Return error that occured during generating."""
        raise NotImplementedError()

    def get_repository(self, student: "Student") -> "Repository":
        raise NotImplementedError()

    def get_all_pull_requests(self):
        raise NotImplementedError()

    def does_repository_exists(self, student) -> bool:
        raise NotImplementedError()()

    @property
    def name(self) -> str:
        if self.__name is None:
            self.name = self.context.organization_name
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
