import os
from enum import Enum
from typing import Optional, Callable


class IMPORTANT_FOLDERS(Enum):
    CONFIG = "config"
    LOCAL_CONFIG = "localconfig"
    REPORT = "report"
    OCTOPUS = "octopus"


class DirectoryNotFound(Exception):
    pass


POSSIBLE_FOLDERS = set([import_dir.value for import_dir in IMPORTANT_FOLDERS])


def get_local_config_path() -> str:
    return get_folder_path(IMPORTANT_FOLDERS.LOCAL_CONFIG)


def get_config_path() -> str:
    return get_folder_path(IMPORTANT_FOLDERS.CONFIG)


def get_report_path() -> str:
    return get_folder_path(IMPORTANT_FOLDERS.REPORT)


def get_octopus_path() -> str:
    return get_folder_path(IMPORTANT_FOLDERS.OCTOPUS)


def get_folder_path(folder_name: IMPORTANT_FOLDERS) -> str:
    return f"{get_root_directory_path()}/{folder_name.value}"


def get_root_directory_path() -> str:
    root_directory_path = get_potential_root_directory_path()
    os.environ["GLM_PATH"] = root_directory_path

    return root_directory_path


def get_potential_root_directory_path() -> str:
    root_directory_path = get_enviroment_directory_path()
    if root_directory_path:
        return root_directory_path

    from core.core import shell_command

    current_path = shell_command("pwd")
    root_directory_path = (
        current_path if is_config_directory_path(current_path) else None
    )
    if root_directory_path:
        return current_path

    root_directory_path = get_git_root_directory_path()
    if root_directory_path:
        return root_directory_path

    while current_path != "":
        if is_config_directory_path(current_path):
            return current_path
        current_path = current_path[: current_path.rfind("/")]

    raise DirectoryNotFound("Root directory not found")


def get_enviroment_directory_path() -> Optional[str]:
    output = os.environ.get("GLM_PATH", "")
    return None if output == "" else output


def get_git_root_directory_path() -> Optional[str]:
    from core.core import shell_command

    path = shell_command("git rev-parse --show-toplevel")
    if is_config_directory_path(path):
        return path


def is_config_directory_path(path: str) -> bool:
    output = False
    for file_name in os.listdir(path):
        for important_folder in IMPORTANT_FOLDERS:
            if file_name == important_folder.value:
                output = important_folder
                break

    # TODO maybe all of the options are not equiavalent, if config is not present but localconfig is maybe it can run but an warning will be throw

    return output is not False


def get_directory_path(directory_name: str) -> Optional[str]:
    if directory_name[-1] != "/":
        directory_name = directory_name + "/"
    return get_file_path(directory_name, os.path.isdir)


def get_file_path(
    filename: str, checker: Callable[[str], bool] = os.path.isfile
) -> Optional[str]:
    root_directory_path = get_root_directory_path()
    path = file_in_localconfig(filename, root_directory_path, checker)
    if path:
        return path
    path = file_in_config(filename, root_directory_path, checker)
    if path:
        return path

    raise DirectoryNotFound(f"{filename} does not exists in localconfig or in config")


def file_in_config(
    filename: str,
    root_directory_path: Optional[str] = get_root_directory_path(),
    checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    return file_in_important_folder(
        filename, IMPORTANT_FOLDERS.CONFIG, root_directory_path, checker
    )


def file_in_localconfig(
    filename: str,
    root_directory_path: Optional[str] = get_root_directory_path(),
    checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    return file_in_important_folder(
        filename, IMPORTANT_FOLDERS.LOCAL_CONFIG, root_directory_path, checker
    )


def file_in_important_folder(
    filename: str,
    important_folder: IMPORTANT_FOLDERS,
    root_directory_path: Optional[str] = get_root_directory_path(),
    checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    path_to_file = join_path(root_directory_path, important_folder.value, filename)
    if checker(path_to_file):
        return path_to_file


def join_path(*path: str):
    return "/".join(path)


if __name__ == "__main__":
    print(get_root_directory_path())
