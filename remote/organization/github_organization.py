import requests
import json
from typing import List, Dict, Optional
from requests.exceptions import ConnectionError
from github.GithubException import (
    UnknownObjectException,
    BadCredentialsException as GithubBadCredentialsException,
)


from remote.pull_request.pull_request import PullRequestState
from remote.organization.organization import Organization
from errors import (
    GLMException,
    BadCredentialsException,
    RepositorySetupException,
    PullRequestParsingException,
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

    @property
    def remote_organization(self):
        if (
            not hasattr(self, "__remote_organization")
            or self.__remote_organization is None
        ):
            try:
                self.remote_organization = self.context.remote.get_organization(
                    self.context.organization_name
                )
            except ConnectionError as e:
                raise NoInternetConnectionException() from e
        return self.__remote_organization

    @remote_organization.setter
    def remote_organization(self, value):
        self.__remote_organization = value

    def get_student_pull_requests(self, students: List["Student"]) -> Dict["Student", "PullRequest"]:
        content = self.get_content(students)
        return self.parse_content(students, json.loads(content))

    def get_content(self, students: List["Student"]) -> str:
        url = 'https://api.github.com/graphql'
        headers = {'Authorization': f"token {self.context.token}"}
        json = {"query": self.create_query(students)}
        try:
            response = requests.post(url=url, json=json, headers=headers)
            return response.text
        except ConnectionError as e:
            raise NoInternetConnectionException() from e

    def create_query(self, students: List["Student"]) -> str:
        query =f'{{organization(login: "{self.name}") {{'
        for student in students:
            query += """
                {university_login}: repository(name: "{repository_name}") {{
                    pullRequests(first: 100) {{
                        nodes {{
                            number
                            id
                            state
                            headRefName
                            headRepository {{
                                name
                            }}
                            baseRefName
                        }}
                    }}
                }}
            """.format(university_login=student.university_login, repository_name=student.repository_name)
        query += "\n}\n}"
        return query

    def parse_content(self, students: List["Student"], content: Dict) -> Dict["Student", "PullRequest"]:
        organization_content = content["data"]["organization"]
        student_pull_requests = {}
        for student in students:
            try:
                pull_requests = self.parse_student_content(student, organization_content[student.university_login])
                student_pull_requests[student] = pull_requests
            except PullRequestParsingException as e:
                e.show()

        return student_pull_requests

    def parse_student_content(self, student: "Student", content: Optional[Dict]) -> List["PullRequest"]:
        if content is None:
            raise PullRequestParsingException(f"{student.repository_name} doesn't exist")

        pull_requests = []
        pull_request_nodes = content["pullRequests"]["nodes"]
        for node in pull_request_nodes:
            pull_requests.append(
                self.context.get_pull_request(
                    number=int(node["number"]),
                    student=student,
                    id=node["id"],
                    head_branch=node["headRefName"],
                    head_repository_name=node["headRepository"]["name"],
                    base_branch=node["baseRefName"],
                    status=PullRequestState(node["state"].lower()),
                    in_review=False,
                )
            )

        return pull_requests
