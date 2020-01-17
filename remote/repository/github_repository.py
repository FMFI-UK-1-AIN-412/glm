from typing import Optional, List
from github import Repository
from github.Repository import Repository as RemoteRepository

from remote.repository.repository import Repository


class GithubRepository(Repository):
    def __init__(self, context: "Context", student: "Student", organization: Optional["Organization"] = None, remote_repository: Optional[RemoteRepository] = None):
        super().__init__(context, student, organization)
        self.remote_repository = remote_repository

    def add_student_colaborator(self):
        self.remote_repository.add_student_colaborator(self.student.remote_login, "pull")

    def delete(self):
        self.remote_repository.delete()

    def get_pull_requests(self) -> List["PullRequest"]:
        from remote.pull_request.pull_request import PullRequest
        pull_requests = []

        for pull_request in self.remote_repository.get_pulls("open"):
            pr = PullRequest(
                context=self.context,
                number=pull_request.number,
                student=self.student,
                id=pull_request.id,
                head_branch=pull_request.head.ref,
                base_branch=pull_request.base.ref,
                status="open",
                in_review=False
            )
            pull_requests.append(pr)

        return pull_requests

    # TODO: generate the name of the user fork from repository
    def get_remote_ssh(self) -> str:
        return f"{self.context.git_remote_url_prefix()}:{self.student.remote_login}/{self.name}.git"

    @property
    def remote_repository(self) -> RemoteRepository:
        if self.__remote_repository is None:
            self.remote_repository = self.context.remote_organization.get_repo(self.student.get_repository_name())
        return self.__remote_repository

    @remote_repository.setter
    def remote_repository(self, value):
        self.__remote_repository = value

    @property
    def organization(self) -> "GithubOrganization":
        if self.__organization is None:
            from remote.organization.github_organization import GithubOrganization
            self.organization = GithubOrganization(self.context)
        return self.__organization
