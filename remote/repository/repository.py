class Repository:
    def __init__(self, context: "Context", student: "Student"):
        self.context = context
        self.student = student

    def add_student_colaborator(self, student: "Student"):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def get_pull_requests(self):
        raise NotImplementedError()

    # TODO: generate the name of the user fork from repository
    def get_remote_ssh(self) -> str:
        return f"{self.context.git_remote_url_prefix()}:{self.student.remote_login}/{self.name}.git"

    @property
    def organization(self) -> "Organization":
        if self.__organization is None:
            self.organization = self.context.organization()
        return self.__organization

    @organization.setter
    def organization(self, organization):
        self.__organization = organization

    @property
    def name(self):
        return self.student.repository_name
