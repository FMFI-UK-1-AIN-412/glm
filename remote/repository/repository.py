from typing import Optional, List
from plumbum.colors import success
from os import listdir

from errors import GLMException, GitException
from core.core import (
    shell_command,
    get_current_remotes,
    can_push_branch,
    does_local_branch_exists,
    get_exit_code,
)


class Repository:
    def __init__(self, context: "Context", student: "Student"):
        self.context = context
        self.student = student

    def check_or_add_remotes(self, current_remotes: Optional[List[str]] = None):
        """Add remotes for 'base' repository and forked repository if missing"""
        if current_remotes is None:
            current_remotes = get_current_remotes()

        if self.base_remote_name not in current_remotes:
            remote_url = self.context.git_remote_url(
                self.organization.name, self.student.repository_name,
            )
            shell_command(f"git remote add {self.base_remote_name} {remote_url}")
        if self.forked_remote_name not in current_remotes:
            remote_url = self.context.git_remote_url(
                self.student.remote_login,
                self.student.repository_name,  # TODO: change this to the actual fork name
            )
            shell_command(f"git remote add {self.forked_remote_name} {remote_url}")

    def distribute_branch(
        self, branch_name: str, all_branches: List[str],
    ):
        try:
            self.fetch_base_remote()
            self.push_branch(branch_name, self.base_remote_name, all_branches)
            print(self.base_remote_name, success | "OK")
        except GitException as e:
            e.show()

        try:
            self.fetch_forked_remote()
            self.push_branch(branch_name, self.forked_remote_name, all_branches)
            print(self.forked_remote_name, success | "OK")
        except GitException as e:
            e.show()

    def fetch_base_remote(self, refspec: str = ""):
        code = get_exit_code(f"git fetch {self.base_remote_name} {refspec}", True, True)
        if code != 0:
            raise GitException(f"Couldn't fetch {self.base_remote_name} {refspec}")

    def fetch_forked_remote(self, refspec: str = ""):
        code = get_exit_code(
            f"git fetch {self.forked_remote_name} {refspec}", True, True
        )
        if code != 0:
            raise GitException(f"Couldn't fetch {self.forked_remote_name} {refspec}")

    def push_branch(
        self, branch_name: str, remote_name: str, all_branches: List[str],
    ):
        if can_push_branch(remote_name, branch_name, all_branches):
            code = get_exit_code(
                f"git push {remote_name} origin/{branch_name}:refs/heads/{branch_name}",
                True,
                True,
            )
            if code != 0:
                raise GitException(f"Couldn't push to {remote_name}")
        else:
            raise GitException(f"NOT updating diverged {remote_name}/{branch_name}")

    def generate_and_push_report(self, report_command: str, filename: str):
        # TODO: check if octopus has origin set up, you need origin/master when settings report branches UP

        shell_command("git checkout master")

        shell_command(f"git fetch {self.base_remote_name}")
        shell_command(f"git fetch {self.forked_remote_name}")

        print(" Dropping changes")
        shell_command("git reset --hard")

        if does_local_branch_exists(self.local_report_branch_name):
            shell_command(f"git checkout {self.local_report_branch_name}")
        else:
            shell_command(
                f"git checkout -B {self.local_report_branch_name} origin/master"
            )

        shell_command(f"sh {report_command} {self.base_remote_name}")

        if get_exit_code(f"git add {filename}") == 0:
            shell_command(["git", "commit", "-m", f'"update {filename}"'])
            shell_command(
                f"git push {self.base_remote_name} HEAD:{self.remote_report_branch_name}"
            )
            shell_command(
                f"git push {self.forked_remote_name} HEAD:{self.remote_report_branch_name}"
            )
        else:
            print("Nothing to add")

    def get_local_pull_requests(self) -> List["PullRequest"]:
        pulls = []

        for student_pull_file in listdir(self.student.pulls_directory_path()):
            try:
                pr_number = int(student_pull_file)
            except ValueError as e:
                raise GLMException(
                    "Student PR file error",
                    f"Student PR files should be named after their numbers in remote. So it should be integer, not '{student_pull_file}'.",
                    True,
                ) from e
            pr = self.context.get_pull_request(pr_number, self.student)
            pulls.append(pr)

        return pulls

    def pull_base_remote(self, refspec: str = ""):
        shell_command(f"git pull {self.base_remote_name} {refspec}")

    def pull_forked_remote(self, refspec: str = ""):
        shell_command(f"git pull {self.forked_remote_name} {refspec}")

    # TODO: generate the name of the user fork from repository
    def get_remote_ssh(self) -> str:
        return f"{self.context.git_remote_url_prefix()}:{self.student.remote_login}/{self.name}.git"

    def has_student_in_collaborators(self) -> bool:
        raise NotImplementedError()

    def invite_student_to_collaborators(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def get_remote_pull_requests(self) -> List["PullRequest"]:
        raise NotImplementedError()

    @property
    def remote_report_branch_name(self) -> str:
        return self.context.remote_report_branch_name

    @property
    def local_report_branch_name(self) -> str:
        return f"{self.base_remote_name}-{self.remote_report_branch_name}"

    @property
    def base_remote_name(self) -> str:
        return self.student.repository_name

    @property
    def forked_remote_name(self) -> str:
        return f"{self.student.repository_name}-fork"

    @property
    def organization(self) -> "Organization":
        if not hasattr(self, "__organization") or self.__organization is None:
            self.__organization = self.context.organization
        return self.__organization

    @property
    def name(self):
        return self.student.repository_name
