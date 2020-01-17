from enum import Enum
import github


class RemoteTypes(Enum):
    GitHub = 1


class Context:
    def __init__(self):
        self.token = None
        self.remote = None
        self.remote_type = None
        self.organization = None

    def get_repository(self, student: "Student") -> "Repository":
        return self.organization.get_repository(student)

    def git_remote_url_prefix(self) -> str:
        if self.remote_type == RemoteTypes.GitHub:
            return "git@github.com"
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
        if self.__remote == None:
            if self.remote_type == RemoteTypes.GitHub:
                self.__remote = github.Github(self.token)
            else:
                raise NotImplementedError
        return self.__remote

    @remote.setter
    def remote(self, value):
        self.__remote = value

    @property
    def remote_type(self) -> RemoteTypes:
        if self.__remote_type == None:
            self.__remote_type = RemoteTypes.GitHub
        return self.__remote_type

    @remote_type.setter
    def remote_type(self, value):
        self.__remote_type = value

    @property
    def organization(self) -> "Organization":
        if self.__organization is None:
            if self.remote_type == RemoteTypes.GitHub:
                from remote.organization.github_organization import GithubOrganization
                self.__organization = GithubOrganization(self)
        return self.__organization

    @organization.setter
    def organization(self, value):
        self.__organization = value

    @property
    def remote_organization(self):
        return self.organization.remote_organization

