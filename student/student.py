from typing import Optional, Dict, Any
from pyaml import yaml
import os

from core.config_loader import get_directory_path, get_local_config_path


class Student:
    __active_students_directory_path = None

    def __init__(
        self,
        context: "Context",
        university_login: str,
        remote_login: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        repository_id: Optional[str] = None,
        repository_name: Optional[str] = None,
    ):
        self.context = context
        self.university_login = university_login
        self.remote_login = remote_login
        self.name = name
        self.email = email
        self.repository_id = repository_id
        self.repository_name = repository_name

    def save(self):
        student = {
            "university_login": self.university_login,
            "remote_login": self.remote_login,
            "name": self.name,
            "email": self.email,
        }

        if self.__repository_id is not None:
            student["repository_id"] = self.repository_id
        if self.__repository_name is not None:
            student["repository_name"] = self.repository_name

        with open(
            f"{self.get_active_directory_path()}/{self.university_login}", "w"
        ) as f:
            f.writelines(yaml.dump(student))

    def directory_name(self) -> str:
        return self.university_login

    def pulls_directory_path(self) -> str:
        path_to_pulls = f"{get_local_config_path()}/pulls/{self.directory_name()}"
        if not os.path.exists(path_to_pulls):
            print(
                f"Creating pulls directory for {self.university_login} at {path_to_pulls}"
            )
            os.mkdir(path_to_pulls)

        return path_to_pulls

    def passes_filters(self, filters: Optional[Dict[str, Any]] = None):
        if filters is None:
            return True

        for f in filters:
            filter_type = type(filters[f])
            if filter_type(getattr(self, f)) != filters[f]:
                return False

        return True

    @property
    def remote_login(self) -> Optional[str]:
        if self.__remote_login is None:
            self.load_properties()
        return self.__remote_login

    @remote_login.setter
    def remote_login(self, value):
        self.__remote_login = value

    @property
    def email(self) -> Optional[str]:
        if self.__email is None:
            self.load_properties()
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def name(self) -> Optional[str]:
        if self.__name is None:
            self.load_properties()
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def repository_id(self) -> Optional[str]:
        if self.__repository_id is None:
            self.load_properties()
        return self.__repository_id

    @repository_id.setter
    def repository_id(self, value):
        self.__repository_id = value

    @property
    def repository_name(self) -> Optional[str]:
        if self.__repository_name is None:
            self.load_properties()
        if self.__repository_name is None:
            self.repository_name = self.generate_repository_name()
        return self.__repository_name

    def generate_repository_name(self):
        return self.context.user_repository_prefix + self.university_login

    @repository_name.setter
    def repository_name(self, value):
        self.__repository_name = value

    def load_properties(self):
        active_students_path = Student.get_active_directory_path()
        parsed_student = self.get_parsed_student(
            f"{active_students_path}/{self.university_login}"
        )

        self.remote_login = (
            parsed_student.get("remote_login")
            if self.__remote_login is None
            else self.__remote_login
        )
        self.name = parsed_student.get("name") if self.__name is None else self.__name
        self.email = (
            parsed_student.get("email") if self.__email is None else self.__email
        )
        self.repository_id = (
            parsed_student.get("repository_id")
            if self.__repository_id is None
            else self.__repository_id
        )
        self.repository_name = (
            parsed_student.get("repository_name")
            if self.__repository_name is None
            else self.__repository_name
        )

    @classmethod
    def get_parsed_student(cls, file_path: str) -> Dict[str, str]:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    def get_active_directory_path(cls) -> str:
        if cls.__active_students_directory_path is None:
            cls.__active_students_directory_path = get_directory_path("active/")
        if cls.__active_students_directory_path is None:
            local_config_path = get_local_config_path()
            print(f"Creating active directory in {local_config_path}")
            os.mkdir(f"{local_config_path}/active")
            cls.__active_students_directory_path = f"{local_config_path}/active"

        return cls.__active_students_directory_path

    def __repr__(self) -> str:
        return f"university login = {self.university_login}, remote login = {self.remote_login}, name = {self.name}, email = {self.email}"
