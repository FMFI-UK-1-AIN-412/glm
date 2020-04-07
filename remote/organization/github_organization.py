import requests
from requests.exceptions import ConnectionError
from github.GithubException import (
    UnknownObjectException,
    BadCredentialsException as GithubBadCredentialsException,
)


from remote.organization.organization import Organization
from errors import (
    BadCredentialsException,
    RepositorySetupException,
    NoInternetConnectionException,
)


class GithubOrganization(Organization):
    def create_remote_repository(self, student: "Student"):
        try:
            response = requests.post(
                f"https://api.github.com/repos/{self.context.organization_name}/{self.context.template_repository_name}/generate",
                json={
                    "owner": self.context.organization_name,
                    "name": student.repository_name,
                    "private": True,
                },
                headers={
                    "Accept": "application/vnd.github.baptiste-preview+json",
                    "Authorization": f"token {self.context.token}",
                },
            )
        except ConnectionError as e:
            raise NoInternetConnectionException from e

        if not response.ok:
            response_json = response.json()
            message = response_json.get("message", "")
            if message == "Invalid owner":
                raise RepositorySetupException(
                    f"Organization name {self.context.organization_name} is wrong",
                    fatal=True,
                )
            elif message == "Bad credential":
                raise BadCredentialsException(
                    f"Couldn't create repository because the credentials are wrong",
                )
            elif message == "Not Found":
                raise RepositorySetupException(
                    f"Failed while creating repository for {student.name}",
                    f"Check if {self.context.organization_name}/{self.context.template_repository_name} is a template",
                    True,
                )
            else:
                errors = response_json.get("errors", None)
                if errors is not None:
                    raise RuntimeError(f"{message}, errors = {str(errors)}")
                else:
                    raise RuntimeError(message)

    def does_remote_repository_exists(self, student: "Student") -> bool:
        try:
            self.remote_organization.get_repo(student.repository_name)
            return True
        except UnknownObjectException as e:
            if e.data.get("message", "raise me") != "Not Found":
                raise e
            return False
        except GithubBadCredentialsException:
            raise BadCredentialsException(
                f"Couldn't check if repository exists because the credentials are wrong",
                fatal=True,
            )

    def _get_remote_organization(self):
        try:
            return self.context.remote.get_organization(self.context.organization_name)
        except ConnectionError as e:
            raise NoInternetConnectionException() from e

