import subprocess
import os

from enum import Enum
from typing import Optional, Generator


class IMPORTANT_FOLDERS(Enum):
    CONFIG = "config"
    LOCAL_CONFIG = "localconfig"
    REPORT = "report"


class RootDirectoryNotFound(Exception): pass


POSSIBLE_FOLDERS = set([import_dir.value for import_dir in IMPORTANT_FOLDERS])

def get_root_directory() -> str:
    root_directory = get_potential_root_directory()
    os.environ["GLM_PATH"] = root_directory

    return root_directory

def get_potential_root_directory() -> str:
    root_directory = get_enviroment_directory()
    if root_directory:
        return root_directory

    current_path = get_terminal_output("pwd")
    root_directory = None if is_config_directory(current_path) else current_path
    if root_directory:
        return current_path

    root_directory = get_git_root_directory()
    if root_directory:
        return root_directory

    while current_path != "":
        if is_config_directory(current_path):
            return current_path
        current_path = current_path[:current_path.rfind("/")]

    raise RootDirectoryNotFound()

def get_enviroment_directory() -> Optional[str]:
    output = os.environ.get('GLM_PATH', '')
    return None if output == "" else output

def get_terminal_output(command: str) -> Optional[str]:
    try:
        command_list = [command]
        if " " in command:
            command_list = command.split(" ")
        output = subprocess.check_output(command_list).decode("utf-8")[:-1]
        if output:
            return output
        if output != "":
            print(f"Wrong formatted $GLM_PATH, current value = {output}")
    except:
        return None

def get_git_root_directory() -> Optional[str]:
    return get_terminal_output("git rev-parse --show-toplevel")

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

def file_in_config(filename: str, root_directory: Optional[str]=get_root_directory()) -> Optional[str]:
    path_to_file = join_path(root_directory, IMPORTANT_FOLDERS.CONFIG.value, filename)
    if os.path.isfile(path_to_file):
        return path_to_file

def file_in_localconfig(filename: str, root_directory: Optional[str]=get_root_directory()) -> Optional[str]:
    path_to_file = join_path(root_directory, IMPORTANT_FOLDERS.LOCAL_CONFIG.value, filename)
    if os.path.isfile(path_to_file):
        return path_to_file

def join_path(*path: str):
    return "/".join(path)


if __name__ == "__main__":
    print(get_root_directory())
