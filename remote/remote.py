import sys
import subprocess
import core.core as Core

from enum import Enum
from remote.pull_request import PullRequest
from typing import Optional, Sequence, List


class RemoteService(Enum):
    Github = 1
    Gitlab = 2

class Remote:
    def __init__(self, token: Optional[str]=None, remote_service=RemoteService.Github):
        self.service = remote_service #TODO: find out appropriate git servicee
        self.token = token
        if token == None:
            self.token = Core.get_token()

        self.organization = None
        self.remote_user = None
        if self.service == RemoteService.Github:
            import github
            self.remote_user = github.Github(Core.get_token())
            self.organization = self.remote_user.get_organization(Core.organization_name())
        else:
            pass

    def create_repository(self, university_login: str, student_remote_name: str, private: Optional[bool]=True, has_issues: Optional[bool]=False, has_wiki: Optional[bool]=False, auto_init: Optional[bool]=False):
        repo = self.get_user_repo(university_login)
        if repo is None:
            if self.service == RemoteService.Github:
                repo = self.organization.create_repo(Core.get_repo_name(university_login), private=private, has_issues=has_issues, has_wiki=has_wiki, auto_init=auto_init)
            else:
                repo = None
        else:
            print("Repo for {university_login} already exists")

        try:
            print(f"Adding {student_remote_name} as collaborator for {repo.name}")
            if self.service == RemoteService.Github:
                repo.add_to_collaborators(student_remote_name, "pull")
            else:
                pass
        except:
            print(f"ERROR: can't add {student_remote_name} as collaborator to {repo.name}")

        Core.save_student(university_login, student_remote_name)

        return repo

    def delete_repo(self, university_login: str):
        repo = self.get_user_repo(university_login)

        if repo is None:
            print(f"Repo {Core.get_repo_name(university_login)} for user {repo} doesn't exists")

        if self.service == RemoteService.Github:
            try:
                repo.delete()
            except:
                print("Cannot delete repo {}")
        else:
            repo = None

        Core.delete_student(university_login)


    def get_user_repo(self, name: str):
        repo_name = Core.get_repo_name(name)
        try:
            if self.service == RemoteService.Github:
                return self.organization.get_repo(repo_name)
            else:
                return None
        except:
            pass

    def generate_remote_url_for_student(self, university_login: str):
        return self.generate_remote_url_for_remote_student(Core.get_repo_name(university_login))

    def generate_remote_url_for_remote_student(self, remote_login: str):
        if self.service == RemoteService.Github:
            return "git@github.com:" + Core.organization_name() + "/" + remote_login + ".git"

    def push_branch(self, branch_name: str, university_login: Optional[str]=None):
        subprocess.run(["git", "checkout", branch_name])
        remotes = []

        if university_login == None:
            students = Core.active_students()
            for student in students:
                subprocess.run(["git", "remote", "add", "-t", branch_name, student[0], self.generate_remote_url_for_remote_student(student[1])])
                remotes.append(self.generate_remote_url_for_remote_student(student[1]))
        else:
            subprocess.run(["git", "remote", "add", "-t", branch_name, university_login, self.generate_remote_url_for_student(university_login)])
            remotes.append(self.generate_remote_url_for_remote_student(university_login))

        for remote in remotes:
            subprocess.run(["git", "push", remote, branch_name])

    def get_pull_requests(self, students: Optional[Sequence[str]] = None, branch: Optional[str] = None) -> List[PullRequest]:
        if students == None or len(students) == 0:
            students = map(lambda x: x[0], Core.active_students())

        pull_requests = []
        if self.service == RemoteService.Github:
            for student in students:
                for pull in self.organization.get_repo(Core.get_repo_name(student)).get_pulls():
                    # print(pull)
                    # import pdb; pdb.set_trace()
                    pull_requests.append(PullRequest(student, pull.head.label, pull.base.label))
        else:
            pass

        return pull_requests
