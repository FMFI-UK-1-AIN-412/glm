from typing import Optional, Any, Dict, List
import yaml

from remote.context import Context
from errors import WrongLocationException
from core.core import shell_command, does_local_branch_exists
from remote.issue_comment.issue_comment import IssueComment
from core.config_loader import is_in_octopus_directory, get_octopus_path


class PullRequest:
    def __init__(
        self,
        context: Context,
        number: int,
        student: "Student",
        id: Optional[str] = None,
        head_branch: Optional[str] = None,
        head_repository_name: Optional[str] = None,
        base_branch: Optional[str] = None,
        status: Optional[str] = None,
        in_review: Optional[bool] = False,
    ):
        self.context = context
        self.number = number
        self.student = student
        self.id = id
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.head_repository_name = head_repository_name
        self.status = status
        self.in_review = in_review
        self.head_repository = None

    def save(self):
        with open(self.file_path, "w") as f:
            pull_request = {
                "id": self.id,
                "student_university_login": self.student.university_login,
                "head_branch": self.head_branch,
                "base_branch": self.base_branch,
                "head_repository_name": self.head_repository_name,
                "status": self.status,
            }

            f.writelines(yaml.dump(pull_request))

    def passes_filters(self, filters: Optional[Dict[str, Any]] = None) -> bool:
        if filters is None:
            return True

        for f in filters:
            if f == "student":
                if not self.student.passes_filters(filters[f]):
                    return False
            else:
                filter_type = type(filters[f])
                if filter_type(getattr(self, f)) != filters[f]:
                    return False

        return True

    def checkout_pull_request(self):
        if not is_in_octopus_directory():
            raise WrongLocationException(
                "You are not in octopus directory", f"type: cd {get_octopus_path()}"
            )

        self.head_repository.check_or_add_remotes()
        self.head_repository.pull_forked_remote(
            f"{self.base_branch}:{self.branch_name}"
        )

        if not does_local_branch_exists(self.branch_name):
            shell_command(
                f"git checkout -b {self.branch_name} --track {self.head_repository.forker_remote_name}/{self.head_branch}"
            )
        else:
            shell_command(f"git checkout {self.branch_name}")

    def merge_pull_request(self, comment: str):
        raise NotImplementedError()

    def create_issue_comment(self, comment: str):
        raise NotImplementedError()

    def create_comment(
        self, comment: str, commit_id: int, possition: int, file_path: str
    ):
        raise NotImplementedError()

    def get_issue_comments(self) -> List[IssueComment]:
        raise NotImplementedError()

    @property
    def branch_name(self) -> str:
        return f"{self.student.university_login}#{self.number}"

    @property
    def mergeable(self) -> bool:
        raise NotImplementedError()

    @property
    def id(self):
        if self.__id is None:
            self.load_properties()
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def base_branch(self):
        if self.__base_branch is None:
            self.load_properties()
        return self.__base_branch

    @base_branch.setter
    def base_branch(self, value):
        self.__base_branch = value

    @property
    def head_branch(self):
        if self.__head_branch is None:
            self.load_properties()
        return self.__head_branch

    @head_branch.setter
    def head_branch(self, value):
        self.__head_branch = value

    @property
    def head_repository_name(self):
        if self.__head_repository_name is None:
            self.load_properties()
        return self.__head_repository_name

    @head_repository_name.setter
    def head_repository_name(self, value):
        self.__head_repository_name = value

    @property
    def status(self):
        if self.__status is None:
            self.load_properties()
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def url(self):
        return self.context.pull_request_url(self)

    @property
    def head_repository(self):
        if self.__head_repository is None:
            self.head_repository = self.context.get_repository(self.student)
        return self.__head_repository

    @head_repository.setter
    def head_repository(self, value):
        self.__head_repository = value

    def load_properties(self):
        parsed_pull_request = self.get_parsed_pull_request(self.file_path)
        self.id = parsed_pull_request.get("id") if self.__id is None else self.__id

        self.base_branch = (
            parsed_pull_request.get("base_branch")
            if self.__base_branch is None
            else self.__base_branch
        )

        self.head_branch = (
            parsed_pull_request.get("head_branch")
            if self.__head_branch is None
            else self.__head_branch
        )

        self.head_repository_name = (
            parsed_pull_request.get("head_repository_name")
            if self.__head_repository_name is None
            else self.__head_repository_name
        )

        self.status = (
            parsed_pull_request.get("status")
            if self.__status is None
            else self.__status
        )

    @property
    def file_path(self) -> str:
        return f"{self.student.pulls_directory_path()}/{self.number}"

    @classmethod
    def get_parsed_pull_request(cls, file_path: str) -> Dict[str, str]:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def __repr__(self):
        return f"student = {self.student.university_login}, {self.head_branch} -> {self.base_branch}, status = {self.status}, number = {self.number}"
