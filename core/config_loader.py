import os
from enum import Enum
from typing import Optional, Callable, List

from errors import GLMException


class IMPORTANT_DIRECTORY(Enum):
    CONFIG = "config"
    LOCAL_CONFIG = "localconfig"
    REPORT = "report"
    OCTOPUS = "octopus"


POSSIBLE_FOLDERS = set([import_dir.value for import_dir in IMPORTANT_DIRECTORY])


def is_in_octopus_directory() -> bool:
    return get_current_pwd() == get_octopus_path()


def get_current_pwd() -> str:
    from core.core import shell_command

    return shell_command("pwd")


def get_local_config_path() -> str:
    return get_folder_path(IMPORTANT_DIRECTORY.LOCAL_CONFIG)


def get_config_path() -> str:
    return get_folder_path(IMPORTANT_DIRECTORY.CONFIG)


def get_report_path() -> str:
    return get_folder_path(IMPORTANT_DIRECTORY.REPORT)


def get_octopus_path() -> str:
    return get_folder_path(IMPORTANT_DIRECTORY.OCTOPUS)


def get_folder_path(folder_name: IMPORTANT_DIRECTORY) -> str:
    return f"{get_root_directory_path()}/{folder_name.value}"


def get_root_directory_path() -> str:
    try:
        root_directory_path = get_potential_root_directory_path()
    except FileNotFoundError as error:
        raise GLMException(
            "It appears that you are not located inside a glm directory", None, True
        ) from error
    else:
        os.environ["GLM_PATH"] = root_directory_path

        return root_directory_path


def get_potential_root_directory_path() -> str:
    root_directory_path = get_enviroment_directory_path()
    if root_directory_path:
        return root_directory_path

    current_path = get_current_pwd()
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

    raise FileNotFoundError("Root directory not found")


def get_enviroment_directory_path() -> Optional[str]:
    output = os.environ.get("GLM_PATH", "")
    return None if output == "" else output


def get_current_branch() -> Optional[str]:
    from core.core import shell_command

    return shell_command("git rev-parse --abbrev-ref HEAD")


def get_git_root_directory_path() -> Optional[str]:
    from core.core import shell_command

    path = shell_command("git rev-parse --show-toplevel", True)
    if is_config_directory_path(path):
        return path


def is_config_directory_path(path: str) -> bool:
    output = False
    for file_name in os.listdir(path):
        for important_folder in IMPORTANT_DIRECTORY:
            if file_name == important_folder.value:
                output = important_folder
                break

    # TODO maybe all of the options are not equiavalent, if config is not present but localconfig is maybe it can run but an warning will be throw

    return output is not False


def get_directory_path(directory_name: str) -> str:
    return get_node_path(directory_name, os.path.isdir)


def get_file_path(filename: str) -> str:
    return get_node_path(filename, os.path.isfile)


def get_node_path(
    node_partial_path: str, node_type_checker: Callable[[str], bool]
) -> str:
    root_directory_path = get_root_directory_path()
    path = node_in_localconfig(
        node_partial_path, root_directory_path, node_type_checker
    )
    if path:
        return path
    path = node_in_config(node_partial_path, root_directory_path, node_type_checker)
    if path:
        return path

    raise FileNotFoundError(
        f"{node_partial_path} does not exists in localconfig or in config"
    )


def node_in_config(
    node_partial_path: str,
    root_directory_path: Optional[str] = None,
    node_type_checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    if root_directory_path is None:
        root_directory_path = get_root_directory_path()
    return node_in_important_directory(
        node_partial_path,
        IMPORTANT_DIRECTORY.CONFIG,
        root_directory_path,
        node_type_checker,
    )


def node_in_localconfig(
    node_partial_path: str,
    root_directory_path: Optional[str] = None,
    node_type_checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    if root_directory_path is None:
        root_directory_path = get_root_directory_path()
    return node_in_important_directory(
        node_partial_path,
        IMPORTANT_DIRECTORY.LOCAL_CONFIG,
        root_directory_path,
        node_type_checker,
    )


def node_in_important_directory(
    node_partial_path: str,
    important_folder: IMPORTANT_DIRECTORY,
    root_directory_path: Optional[str] = None,
    node_type_checker: Callable[[str], bool] = os.path.isfile,
) -> Optional[str]:
    if root_directory_path is None:
        root_directory_path = get_root_directory_path()
    path_to_file = join_path(
        root_directory_path, important_folder.value, node_partial_path
    )
    if node_type_checker(path_to_file):
        return path_to_file


def join_path(*paths: List[str]):
    return "/".join(paths)
