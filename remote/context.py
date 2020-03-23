from enum import Enum
from typing import Optional

from core.config_loader import get_file_path
from core.core import read_line_file
from errors import ConfigFileException


class RemoteTypes(Enum):
    Github = 1


class Context:
    def get_repository(self, student: "Student") -> "Repository":
        return self.organization.get_repository(student)

    def git_remote_url(self, user_name: str, repository_name: str):
        prefix = self.git_remote_url_prefix()
        if self.remote_type == RemoteTypes.Github:
            return f"{prefix}:{user_name}/{repository_name}.git"
        raise NotImplementedError()

    def git_remote_url_prefix(self) -> str:
        if self.remote_type == RemoteTypes.Github:
            return "git@github.com"
        raise NotImplementedError()

    def pull_request_url(self, pull_request: "PullRequest"):
        if self.remote_type == RemoteTypes.Github:
            return f"https://github.com/{pull_request.student.remote_login}/{pull_request.head_repository_name}/pull/ID"
        raise NotImplementedError()

    def get_pull_request(
        self,
        number: int,
        student: "Student",
        id: Optional[str] = None,
        head_branch: Optional[str] = None,
        head_repository_name: Optional[str] = None,
        base_branch: Optional[str] = None,
        status: Optional[str] = None,
        in_review: Optional[bool] = False,
    ) -> "PullRequest":
        if self.remote_type == RemoteTypes.Github:
            from remote.pull_request.github_pull_request import GithubPullRequest

            return GithubPullRequest(
                self,
                number,
                student,
                id,
                head_branch,
                head_repository_name,
                base_branch,
                status,
                in_review,
            )
        raise NotImplementedError()

    @property
    def token(self) -> str:
        if not hasattr(self, "__token") or self.__token is None:
            from core.core import get_token

            self.token = get_token()
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def report_file_name(self) -> str:
        # TODO: load this from config/localconfig
        return "report.txt"

    @property
    def remote(self):
        if not hasattr(self, "__remote") or self.__remote is None:
            if self.remote_type == RemoteTypes.Github:
                from github import Github

                self.remote = Github(self.token)
            else:
                raise NotImplementedError()
        return self.__remote

    @remote.setter
    def remote(self, value):
        self.__remote = value

    @property
    def remote_type(self) -> RemoteTypes:
        if not hasattr(self, "__remote_type") or self.__remote_type is None:
            self.remote_type = RemoteTypes.Github
        return self.__remote_type

    @remote_type.setter
    def remote_type(self, value):
        self.__remote_type = value

    @property
    def organization(self) -> "Organization":
        if not hasattr(self, "__organization") or self.__organization is None:
            if self.remote_type == RemoteTypes.Github:
                from remote.organization.github_organization import GithubOrganization

                self.organization = GithubOrganization(self)
            else:
                raise NotImplementedError()

        return self.__organization

    @organization.setter
    def organization(self, value):
        self.__organization = value

    @property
    def remote_organization(self):
        return self.organization.remote_organization

    @property
    def organization_name(self) -> str:
        if not hasattr(self, "__organization_name") or self.__organization_name is None:
            try:
                organization_name_file_path = get_file_path("organization_name")
                organization_name = read_line_file(organization_name_file_path)
                self.__organization_name = organization_name
            except FileNotFoundError:
                raise ConfigFileException(
                    "File 'organization_name' was not found",
                    "Create organization_name file in localconfig or config directory",
                    True,
                )

        return self.__organization_name

    @property
    def user_repository_prefix(self) -> str:
        if (
            not hasattr(self, "__user_repository_prefix")
            or self.__user_repository_prefix is None
        ):
            try:
                user_repository_prefix_file_path = get_file_path(
                    "user_repository_prefix"
                )
                user_repository_prefix = read_line_file(
                    user_repository_prefix_file_path
                )
            except FileNotFoundError:
                raise ConfigFileException(
                    "File 'user_repository_prefix' was not found",
                    "Create user_repository_prefix file in localconfig or config directory",
                    True,
                )

            self.__user_repository_prefix = user_repository_prefix

        return self.__user_repository_prefix

    @property
    def template_repository_name(self) -> str:
        if (
            not hasattr(self, "__template_repository_name")
            or self.__template_repository_name is None
        ):
            try:
                template_repository_name_file_path = get_file_path(
                    "template_repository_name"
                )
                template_repository_name = read_line_file(
                    template_repository_name_file_path
                )
            except FileNotFoundError:
                raise ConfigFileException(
                    "File 'template_repository_name' was not found",
                    "Create template_repository_name file in localconfig or config directory",
                    True,
                )
            self.__template_repository_name = template_repository_name

        return self.__template_repository_name
