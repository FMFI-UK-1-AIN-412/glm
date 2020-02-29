from subprocess import check_output
from typing import Optional, List

from core.config_loader import get_root_directory_path


def get_token() -> Optional[str]:
    root_directory_path = get_root_directory_path()
    return read_line_file(root_directory_path + "/token")


def read_line_file(filename) -> Optional[str]:
    try:
        with open(filename) as f:
            line = f.readline()
            if line[-1] == "\n":
                line = line[:-1]
            return line
    except:
        return None


def read_lines(file_path: str) -> List[str]:
    with open(file_path) as f:
        for line in f.readlines():
            if line[-1] == "\n":
                yield line[:-1]
            else:
                yield line


def shell_command(command: str) -> Optional[str]:
    try:
        command_list = [command]
        if " " in command:
            command_list = command.split(" ")
        output = check_output(command_list).decode("utf-8")[:-1]
        if output:
            return output
        if output != "":
            print(f"Wrong formatted $GLM_PATH, current value = {output}")
    except:
        return None
