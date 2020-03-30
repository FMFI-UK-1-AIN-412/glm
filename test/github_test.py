from test.test import Test
from github.GithubException import BadCredentialsException, UnknownObjectException


class GithubTest(Test):
    def check_correct_token(self) -> bool:
        try:
            self.context.remote.get_rate_limit()
            return True
        except BadCredentialsException:
            return False

    def check_correct_organization_name(self) -> bool:
        try:
            self.context.remote_organization
            return True
        except UnknownObjectException:
            return False

    def check_has_admin_rights_on_organization(self) -> bool:
        try:
            list(self.context.remote_organization.get_issues())
            return True
        except UnknownObjectException:
            return False

    def check_correct_repository_name(self) -> bool:
        try:
            self.context.remote_organization.get_repo(
                self.context.template_repository_name
            )
            return True
        except UnknownObjectException:
            return False
