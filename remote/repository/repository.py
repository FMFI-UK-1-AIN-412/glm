from typing import Optional, Any


class Repository:
    def __init__(self, context: "Context", student: "Student"):
        self.context = context
        self.student = student

    def add_student_colaborator(self, student: "Student"):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def get_pull_requests(self):
        raise NotImplementedError

    def get_remote_ssh(self) -> str:
        raise NotImplementedError

    @property
    def organization(self) -> "Organization":
        if self.__organization is None:
            self.__organization = self.context.organization()
        return self.__organization

    @organization.setter
    def organization(self, organization):
        self.__organization = organization

    @property
    def name(self):
        return self.student.get_repository_name()
