from typing import List, Optional

from remote.context import Context


class Organization:
    def __init__(self, context: Context):
        self.context = context
        self.name = None

    def create_repositories(self, student: List["Student"]) -> List["Repository"]:
        raise NotImplementedError

    def get_repository(self, student: "Student"):
        raise NotImplementedError

    def delete_student_repository(self, student: "Student"):
        repository = self.context.get_repository(student)

        try:
            repo.delete()
            from core.core import delete_student
            delete_student(student)
        except:
            print(f"Cannot delete repo {repository.name}")

    def get_student_git_ssh_remote_url(self, student: "Student"):
        raise NotImplementedError
        return self.context.git_remote_url_prefix + self.name + "/" + student.remote_login + ".git"

    def push_branch(self, branch_name: str, university_login: Optional[str]=None):
        subprocess.run(["git", "checkout", branch_name])
        remotes = []

        if university_login == None:
            students = Core.active_students()
            for student in students:
                subprocess.run(["git", "remote", "add", "-t", branch_name, student[0], self.generate_remote_url_for_remote_student(student[1])])
                remotes.append(self.generate_remote_url_for_remote_student(student[1]))
        else:
            subprocess.run(["git", "remote", "add", "-t", branch_name, university_login, self.generate_remote_url_for_student(university_login)])
            remotes.append(self.generate_remote_url_for_remote_student(university_login))

        for remote in remotes:
            subprocess.run(["git", "push", remote, branch_name])

    def get_all_pull_requests(self):
        raise NotImplementedError

    @property
    def name(self) -> str:
        if self.__name == None:
            from core.core import get_organization_name
            self.__name = get_organization_name()
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
