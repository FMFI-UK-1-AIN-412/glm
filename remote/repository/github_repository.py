from typing import List
from requests.exceptions import ConnectionError
from github.GithubException import UnknownObjectException

from errors import RepositorySetupException, NoInternetConnectionException
from remote.repository.repository import Repository


class GithubRepository(Repository):
    def has_student_in_collaborators(self) -> bool:
        return self.remote_repository.has_in_collaborators(self.student.remote_login)

    def invite_student_to_collaborators(self):
        try:
            self.remote_repository.add_to_collaborators(
                self.student.remote_login, "pull"
            )
        except UnknownObjectException as e:
            if e.data.get("message", "raise me") != "Not Found":
                raise e
            raise RepositorySetupException(
                f"Couldn't add {self.student.name} as a collaborator to {self.name}",
                f"Check if '{self.student.remote_login}' exists.",
            ) from e

    def delete(self):
        self.remote_repository.delete()

    def get_remote_pull_requests(self) -> List["GithubPullRequest"]:
        pull_requests = []

        for pull_request in self.remote_repository.get_pulls("open"):
            pr = self.context.get_pull_request(
                number=pull_request.number,
                student=self.student,
                id=pull_request.id,
                head_branch=pull_request.head.ref,
                head_repository_name=pull_request.head.repo.name,
                base_branch=pull_request.base.ref,
                status="open",
                in_review=False,
            )
            pull_requests.append(pr)

        return pull_requests

    @property
    def remote_repository(self):
        if not hasattr(self, "__remote_repository") or self.__remote_repository is None:
            try:
                self.remote_repository = self.context.organization.remote_organization.get_repo(
                    self.student.repository_name
                )
            except ConnectionError as e:
                raise NoInternetConnectionException() from e
        return self.__remote_repository

    @remote_repository.setter
    def remote_repository(self, value):
        self.__remote_repository = value
