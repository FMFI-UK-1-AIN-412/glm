from requests.exceptions import ConnectionError

from remote.pull_request.pull_request import PullRequest
from errors import NoInternetConnectionException


class GithubPullRequest(PullRequest):
    def merge_pull_request(self, message: str):
        self.remote_pull_request.merge(message)

    def create_issue_comment(self, comment: str):
        self.remote_pull_request.create_issue_comment(comment)

    def create_comment(
        self, comment: str, commit_id: int, position: int, file_path: str
    ):
        self.remote_pull_request.create_comment(comment, commit_id, file_path, position)

    @property
    def mergeable(self) -> bool:
        return self.remote_pull_request.mergeable

    @property
    def remote_pull_request(self):
        if (
            not hasattr(self, "__remote_pull_request")
            or self.__remote_pull_request is None
        ):
            try:
                self.remote_pull_request = self.context.get_repository(
                    self.student
                ).remote_repository.get_pull(self.number)
            except ConnectionError as e:
                raise NoInternetConnectionException() from e
        return self.__remote_pull_request

    @remote_pull_request.setter
    def remote_pull_request(self, value):
        self.__remote_pull_request = value
