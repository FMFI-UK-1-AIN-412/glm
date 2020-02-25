import requests
from typing import Optional
from github.GithubException import UnknownObjectException


from remote.context import Context
from remote.organization.organization import Organization


class GithubOrganization(Organization):
    def __init__(self, context: Context):
        super().__init__(context)
        self.remote_organization = None

    def create_repository(self, student: "Student") -> Optional[str]:
        """Return error that occured during generating."""
        import core.core as Core

        if not self.does_repository_exists(student):
            print(f"Creating repository ({student.repository_name}) for {student.name}", end="")
            # TODO: add gracefull handling of errors, e.g. not connected to internet
            response = requests.post(
                f"https://api.github.com/repos/{self.context.organization_name}/{self.context.template_repository_name}/generate",
                json={
                    "owner": self.context.organization_name,
                    "name": student.repository_name,
                    "private": True,
                },
                headers={
                    "Accept": "application/vnd.github.baptiste-preview+json",
                    "Authorization": f"token{self.context.token}"
                })

            if not response.ok:
                print(" ... FAIL ")
                response_json = response.json()
                message = response_json.get("message", "")
                if message == "Invalid owner":
                    raise RuntimeError(f"Organization name {self.context.organization_name} is wrong")
                elif message == "Bad credential":
                    raise RuntimeError(f"Bad credentials")
                elif message == "Not Found":
                    return f"Failed while creating repository for {student.name}. Check if {self.context.organization_name}/{self.context.template_repository_name} is a template"
                else:
                    errors = response_json.get("errors", None)
                    if errors is not None:
                        raise RuntimeError(f"{message}, errors = {str(errors)}")
                    else:
                        raise RuntimeError(message)
            else:
                print(" ... OK")

        from remote.repository.github_repository import GithubRepository
        repository = GithubRepository(self.context, student)

        if not repository.remote_repository.has_in_collaborators(student.remote_login):
            print(f"Inviting {student.name} to collaborate on ({repository.name})", end="")
            try:
                repository.add_student_colaborator()
                print(" ... OK")
            except UnknownObjectException as e:
                print(" ... FAIL")
                if e.data.get("message", "raise me") != "Not Found":
                    raise e
                return f"Couldn't add {student.name} as a collaborator to {repository.name}, {student.remote_login} doesn't exists."

    def get_repository(self, student: "Student") -> "GithubRepository":
        from remote.repository.github_repository import GithubRepository
        return GithubRepository(self.context, student)

    def does_repository_exists(self, student: "Student") -> bool:
        try:
            self.remote_organization.get_repo(student.repository_name)
            return True
        except UnknownObjectException as e:
            if e.data.get("message", "raise me") != "Not Found":
                raise e
            return False

    # def get_all_pull_requests(self) -> List[Repository]:
    #     url = 'https://api.github.com/graphql'
    #     json = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
    #     headers = {'Authorization': 'token %s' % Core.get_token()}
    # 
    #     json = {
    #         "query": '''
    #             rateLimit {
    #                 limit
    #                 cost
    #                 remaining
    #                 resetAt
    #             }
    #             organization(login:"glm-testing") {
    #                 repositories(first:100) {
    #                     nodes {
    #                         ...RepoInfo
    #                     }
    #                 }
    #             }
    #         '''
    #     }
    # 
    #     r = requests.post(url=url, json=json, headers=headers)
    #     print(r.text)

    @property
    def remote_organization(self):
        if self.__remote_organization is None:
            from core.core import get_organization_name
            self.__remote_organization = self.context.remote.get_organization(self.context.organization_name)
        return self.__remote_organization

    @remote_organization.setter
    def remote_organization(self, value):
        self.__remote_organization = value
