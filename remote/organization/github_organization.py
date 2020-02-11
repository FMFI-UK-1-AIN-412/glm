from typing import List
import requests

from remote.context import Context
from remote.organization.organization import Organization


class GithubOrganization(Organization):
    def __init__(self, context: Context):
        super().__init__(context)
        self.remote_organization = None

    def create_repository(self, student: "Student") -> "GithubRepository":
        import core.core as Core
        requests.post(
            f"https://api.github.com/repos/{Core.get_organization_name()}/{Core.get_template_name()}/generate",
            json={
                "owner": Core.get_organization_name(),
                "name": student.get_repository_name(),
                "private": False,
            },
            headers={
                "Accept": "application/vnd.github.baptiste-preview+json",
                "Authorization": f"token{Core.get_token()}"
            }
        )

        from remote.repository.github_repository import GithubRepository
        repository = GithubRepository(self.context, student)
        repository.add_student_colaborator()

        return repository

    def get_repository(self, student: "Student") -> "GithubRepository":
        from remote.repository.github_repository import GithubRepository
        return GithubRepository(self.context, student)

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
            self.__remote_organization = self.context.remote.get_organization(get_organization_name())
        return self.__remote_organization

    @remote_organization.setter
    def remote_organization(self, value):
        self.__remote_organization = value
