from typing import Optional, List


class Repository:
    def __init__(self, context: "Context", student: "Student"):
        self.context = context
        self.student = student

    def distribute_branch(
        self,
        branch_name: str,
        check_location: Optional[bool] = True,
        check_if_remote_added: Optional[bool] = True,
        should_fetch: Optional[bool] = True,
        all_branches: Optional[List[str]] = None,
    ):
        from core.core import shell_command

        if check_location:
            pass  # TODO

        if check_if_remote_added:
            self.check_or_add_remotes()

        if should_fetch:
            shell_command(f"git fetch {self.base_remote_name}")
            shell_command(f"git fetch {self.forked_remote_name}")

        self.push_branch(branch_name, self.base_remote_name, all_branches)
        self.push_branch(branch_name, self.forked_remote_name, all_branches)

    def check_or_add_remotes(self, current_remotes: Optional[List[str]] = None):
        """Add remotes for 'base' repository and forked repository if missing"""
        from core.core import shell_command, get_current_remotes

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

    # TODO: think about moving this to core.py, it has all the information it need from repository
    def push_branch(
        self,
        branch_name: str,
        remote_name: str,
        all_branches: Optional[List[str]] = None,
    ):
        from core.core import shell_command, can_push_branch

        if can_push_branch(remote_name, branch_name, all_branches):
            shell_command(
                f"git push {remote_name} origin/{branch_name}:refs/heads/{branch_name}"
            )
        else:
            print(f"NOT updating diverged {remote_name}/{branch_name}")

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
