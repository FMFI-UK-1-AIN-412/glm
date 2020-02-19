from enum import Enum
from typing import Optional


class RemoteTypes(Enum):
    Github = 1


class Context:
    def __init__(self):
        self.token = None
        self.remote = None
        self.remote_type = None
        self.organization = None

    def get_repository(self, student: "Student") -> "Repository":
        return self.organization.get_repository(student)

    def git_remote_url(self, student: "Student"):
        prefix = self.git_remote_url_prefix()
        if self.remote_type == RemoteTypes.Github:
            return f"{prefix}:{self.organization.name}/{student.repository_name}.git"
        raise NotImplementedError

    def git_remote_url_prefix(self) -> str:
        if self.remote_type == RemoteTypes.Github:
            return "git@github.com"
        raise NotImplementedError

    def pull_request_url(self, pull_request: "PullRequest"):
        if self.remote_type == RemoteTypes.Github:
            return f"https://github.com/{pull_request.student.remote_login}/{pull_request.head_repository_name}/pull/ID"
        raise NotImplementedError

    def pull_request(self, number: int, student: "Student", id: Optional[str] = None, head_branch: Optional[str] = None, head_repository_name: Optional[str] = None, base_branch: Optional[str] = None, status: Optional[str] = None, in_review: Optional[bool] = False) -> "PullRequest":
        if self.remote_type == RemoteTypes.Github:
            from remote.pull_request.github_pull_request import GithubPullRequest
            return GithubPullRequest(self, number, student, id, head_branch, head_repository_name, base_branch, status, in_review)
        raise NotImplementedError

    @property
    def token(self) -> str:
        if self.__token is None:
            from core.core import get_token
            self.__token = get_token()
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def remote(self):
        if self.__remote is None:
            if self.remote_type == RemoteTypes.Github:
                from github import Github
                self.__remote = Github(self.token)
            else:
                raise NotImplementedError
        return self.__remote

    @remote.setter
    def remote(self, value):
        self.__remote = value

    @property
    def remote_type(self) -> RemoteTypes:
        if self.__remote_type is None:
            self.__remote_type = RemoteTypes.Github
        return self.__remote_type

    @remote_type.setter
    def remote_type(self, value):
        self.__remote_type = value

    @property
    def organization(self) -> "Organization":
        if self.__organization is None:
            if self.remote_type == RemoteTypes.Github:
                from remote.organization.github_organization import GithubOrganization
                self.organization = GithubOrganization(self)
            else:
                raise NotImplementedError

        return self.__organization

    @organization.setter
    def organization(self, value):
        self.__organization = value

    @property
    def remote_organization(self):
        return self.organization.remote_organization
