import os
from subprocess import check_output, DEVNULL
from enum import Enum
from typing import Optional, Generator, Callable


class IMPORTANT_FOLDERS(Enum):
    CONFIG = "config"
    LOCAL_CONFIG = "localconfig"
    REPORT = "report"


class DirectoryNotFound(Exception):
    pass


POSSIBLE_FOLDERS = set([import_dir.value for import_dir in IMPORTANT_FOLDERS])


def get_local_config() -> str:
    return f"{get_root_directory()}/{IMPORTANT_FOLDERS.LOCAL_CONFIG.value}"


def get_config() -> str:
    return f"{get_root_directory()}/{IMPORTANT_FOLDERS.CONFIG.value}"


def get_root_directory() -> str:
    root_directory = get_potential_root_directory()
    os.environ["GLM_PATH"] = root_directory

    return root_directory


def get_potential_root_directory() -> str:
    root_directory = get_enviroment_directory()
    if root_directory:
        return root_directory

    from core.core import shell_command
    current_path = shell_command("pwd")
    root_directory = current_path if is_config_directory(current_path) else None
    if root_directory:
        return current_path

    root_directory = get_git_root_directory()
    if root_directory:
        return root_directory

    while current_path != "":
        if is_config_directory(current_path):
            return current_path
        current_path = current_path[:current_path.rfind("/")]

    raise DirectoryNotFound("Root directory not found")


def get_enviroment_directory() -> Optional[str]:
    output = os.environ.get('GLM_PATH', '')
    return None if output == "" else output


def get_git_root_directory() -> Optional[str]:
    from core.core import shell_command
    path = shell_command("git rev-parse --show-toplevel")
    if is_config_directory(path):
        return path


def is_config_directory(path: str) -> bool:
    output = False
    for file_name in os.listdir(path):
        if file_name == IMPORTANT_FOLDERS.CONFIG.value:
            output = IMPORTANT_FOLDERS.CONFIG
            break
        if file_name == IMPORTANT_FOLDERS.LOCAL_CONFIG.value:
            output = IMPORTANT_FOLDERS.LOCAL_CONFIG
            break
        if file_name == IMPORTANT_FOLDERS.REPORT.value:
            output = IMPORTANT_FOLDERS.REPORT
            break

    #TODO maybe all of the options are not equiavalent, if config is not present but localconfig is maybe it can run but an exception will be throw

    return output != False


def directory_path(directory_name: str) -> Optional[str]:
    if directory_name[-1] != "/":
        directory_name = directory_name + "/"
    return file_path(directory_name, os.path.isdir)


def file_path(filename: str, checker: Callable[[str], bool] = os.path.isfile) -> Optional[str]:
    root_directory = get_root_directory()
    path = file_in_localconfig(filename, root_directory, checker)
    if path:
        return path
    path = file_in_config(filename, root_directory, checker)
    if path:
        return path

    raise DirectoryNotFound(f"{filename} does not exists in localconfig or in config")


def file_in_config(filename: str, root_directory: Optional[str]=get_root_directory(), checker: Callable[[str], bool] = os.path.isfile) -> Optional[str]:
    path_to_file = join_path(root_directory, IMPORTANT_FOLDERS.CONFIG.value, filename)
    if checker(path_to_file):
        return path_to_file


def file_in_localconfig(filename: str, root_directory: Optional[str]=get_root_directory(), checker: Callable[[str], bool] = os.path.isfile) -> Optional[str]:
    path_to_file = join_path(root_directory, IMPORTANT_FOLDERS.LOCAL_CONFIG.value, filename)
    if checker(path_to_file):
        return path_to_file


def join_path(*path: str):
    return "/".join(path)


if __name__ == "__main__":
    print(get_root_directory())
