import sys
import subprocess
from enum import Enum
import core.core as core

class RemoteService(Enum):
    Github = 1
    Gitlab = 2

class Remote:
    def __init__(self, token=None, remote_service=RemoteService.Github, baseUrl=None):
        self.baseUrl = baseUrl
        self.service = remote_service #TODO: find out appropriate git servicee
        self.token = token
        if token == None:
            self.token = core.get_token()

        self.organization = None
        self.remote_user = None
        if self.service == RemoteService.Github:
            import github
            self.remote_user = github.Github(core.get_token())
            self.organization = self.remote_user.get_organization(core.organization_name())
        else:
            pass

    def create_repository(self, university_login, student_remote_name, private=True, has_issues=False, has_wiki=False, auto_init=False):
        repo = self.get_user_repo(university_login)
        if repo is None:
            if self.service == RemoteService.Github:
                repo = self.organization.create_repo(core.generate_name(university_login), private=private, has_issues=has_issues, has_wiki=has_wiki, auto_init=auto_init)
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

        core.save_student(university_login, student_remote_name)

        return repo

    def delete_repo(self, university_login):
        repo = self.get_user_repo(university_login)

        if repo is None:
            print(f"Repo {core.get_repo_name(university_login)} for user {repo} doesn't exists")

        if self.service == RemoteService.Github:
            try:
                repo.delete()
            except:
                print("Cannot delete repo {}")
        else:
            repo = None

        core.delete_student(university_login)


    def get_user_repo(self, name):
        repo_name = core.get_repo_name(name)
        try:
            if self.service == RemoteService.Github:
                return self.organization.get_repo(repo_name)
            else:
                return None
        except:
            pass

    def generate_remote_url_for_student(self, university_login):
        return self.generate_remote_url_for_remote_student(core.get_repo_name(university_login))

    def generate_remote_url_for_remote_student(self, remote_login):
        if self.service == RemoteService.Github:
            return "git@github.com:" + core.organization_name() + "/" + remote_login + ".git"

    def push_branch(self, branch_name, university_login=None):
        subprocess.run(["git", "checkout", branch_name])

        if university_login == None:
            students = core.active_students()
            for student in students:
                subprocess.run(["git", "remote", "add", "-t", branch_name, student[0], self.generate_remote_url_for_remote_student(student[1])])
        else:
            subprocess.run(["git", "remote", "add", "-t", branch_name, university_login, self.generate_remote_url_for_student(university_login)])





def create_remote():
    return Remote(core.get_token())


def login():
    """ Returns the login arguments as a dict."""
    l = None
    try:
            import auth
            l = auth.login()
    except:
            print("ERROR: no login info!")
            sys.exit(-1)
    return l

