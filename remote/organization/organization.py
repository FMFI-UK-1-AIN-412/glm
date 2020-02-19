from typing import List

from remote.context import Context


class Organization:
    def __init__(self, context: Context):
        self.context = context
        self.name = None

    def create_repositories(self, students: List["Student"]) -> List["Repository"]:
        repositories = []
        for student in students:
            repositories.append(self.create_repository(student))

        return repositories

    def delete_student_and_student_repository(self, student: "Student"):
        repository = self.context.get_repository(student)

        try:
            repository.delete()
        except:
            print(f"Cannot delete repo {repository.name}")
            return

        try:
            from student.utils import delete_student
            delete_student(student)
        except:
            print(f"Cannot student {student.name}")

    def get_student_git_ssh_remote_url(self, student: "Student"):
        return self.context.git_remote_url_prefix + self.name + "/" + student.remote_login + ".git"

    # def push_branch(self, branch_name: str, university_login: Optional[str]=None):
    #     import subprocess
    #     import core.core as Core
    #     subprocess.run(["git", "checkout", branch_name])
    #     remotes = []
    # 
    #     if university_login == None:
    #         students = Core.active_students()
    #         for student in students:
    #             subprocess.run(["git", "remote", "add", "-t", branch_name, student[0], self.generate_remote_url_for_remote_student(student[1])])
    #             remotes.append(self.generate_remote_url_for_remote_student(student[1]))
    #     else:
    #         subprocess.run(["git", "remote", "add", "-t", branch_name, university_login, self.generate_remote_url_for_student(university_login)])
    #         remotes.append(self.generate_remote_url_for_remote_student(university_login))
    # 
    #     for remote in remotes:
    #         subprocess.run(["git", "push", remote, branch_name])

    def create_repository(self, student: "Student") -> "Repository":
        raise NotImplementedError

    def get_repository(self, student: "Student") -> "Repository":
        raise NotImplementedError

    def get_all_pull_requests(self):
        raise NotImplementedError

    @property
    def name(self) -> str:
        if self.__name is None:
            from core.core import get_organization_name
            self.__name = get_organization_name()
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
