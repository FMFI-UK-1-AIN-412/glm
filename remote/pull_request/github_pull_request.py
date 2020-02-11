from github.PullRequest import PullRequest as RemotePullRequest
from typing import Optional

from remote.context import Context
from core.config_loader import IMPORTANT_FOLDERS, get_root_directory
from remote.pull_request.pull_request import PullRequest

class GithubPullRequest(PullRequest):
    def __init__(self, context: Context, number: int, student: "Student", id: Optional[str] = None, head_branch: Optional[str] = None, head_repository_name: Optional[str] = None, base_branch: Optional[str] = None, status: Optional[str] = None, in_review: Optional[bool] = False, remote_pull_request: Optional[RemotePullRequest] = None):
        super().__init__(context, number, student, id, head_branch, head_repository_name, base_branch, status, in_review)
        self.__remote_pull_request = remote_pull_request

    def merge_pull_request(self, message: str):
        self.remote_pull_request.merge(message)

    def create_issue_comment(self, comment: str):
        self.remote_pull_request.create_issue_comment(comment)

    def create_comment(self, comment: str, commit_id: int, position: int, file_path: str):
        self.remote_pull_request.create_comment(comment, commit_id, file_path, position)

    @property
    def mergeable(self) -> bool:
        return self.head_repository.get_pull(self.number).mergeable

    @property
    def remote_pull_request(self):
        if self.__remote_pull_request is None:
            self.remote_pull_request = self.context.get_repository(self.student).remote_repository.get_pull(self.number)
        return self.__remote_pull_request

    @remote_pull_request.setter
    def remote_pull_request(self, value):
        self.__remote_pull_request = value
