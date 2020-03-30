from typing import Optional
from plumbum.colors import info, fatal


class GLMException(Exception):
    def __init__(
        self, message: str, hint: Optional[str] = None, fatal: Optional[bool] = False
    ):
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.fatal = fatal

    def print_message(self):
        print(fatal | self.message)

    def print_hint(self):
        if self.hint:
            print("Hint ", end="")
            print(info | self.hint)

    def show(self):
        self.print_message()
        self.print_hint()


class ConfigFileException(GLMException):
    pass


class CoreFileException(GLMException):
    pass


class StudentDeleteException(GLMException):
    pass


class RootDirectoryNotFoundException(GLMException):
    pass


class BadCredentialsException(GLMException):
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, True)


class RepositoryCreationException(GLMException):
    pass


class WrongLocationException(GLMException):
    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, hint, True)
