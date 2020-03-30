from typing import Callable
from plumbum.colors import fatal, success


class Test:
    def __init__(self, context: "Context"):
        self.context = context

    def do_tests(self):
        Test.do_test("Checking correct token", self.check_correct_token)
        Test.do_test("Checking correct organization name", self.check_correct_organization_name)
        Test.do_test("Checking if user has admin rights on organization", self.check_has_admin_rights_on_organization)
        Test.do_test("Checking correct organization/repository name", self.check_correct_repository_name)


    def do_test(name: str, method: Callable):
        print(f"{name} -> ", end="")
        if method():
            print(success | "OK")
        else:
            print(fatal | "ERROR")
        pass

    def check_correct_token(self) -> bool:
        raise NotImplementedError()

    def check_correct_organization_name(self) -> bool:
        raise NotImplementedError()

    def check_has_admin_rights_on_organization(self) -> bool:
        raise NotImplementedError()

    def check_correct_repository_name(self) -> bool:
        raise NotImplementedError()
