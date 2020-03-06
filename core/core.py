from subprocess import check_output, call
from typing import Optional, List


def get_token() -> Optional[str]:
    from core.config_loader import get_root_directory_path

    root_directory_path = get_root_directory_path()
    return read_line_file(root_directory_path + "/token")


def read_line_file(filename) -> Optional[str]:
    try:
        with open(filename) as f:
            line = f.readline()
            if line[-1] == "\n":
                line = line[:-1]
            return line
    except:  # TODO: not acceptable
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
        command_list = parse_command(command)
        output = check_output(command_list).decode("utf-8")[:-1]
        if output:
            return output
        if output != "":
            print(f"Wrong formatted $GLM_PATH, current value = {output}")
    except:  # TODO: not acceptable
        return None


def parse_command(command: str) -> List[str]:
    if " " in command:
        return command.split(" ")
    return [command]


def get_exit_code(command: str) -> int:
    command_list = parse_command(command)
    print(command_list)
    return call(command_list)


def get_all_branches() -> List[str]:
    # TODO: you need to remove tracking branch indicator, master -> origin/master
    branches_unparsed = shell_command("git branch --all").split("\n")
    branches_unparsed = [
        branch.replace("*", "") for branch in branches_unparsed
    ]  # remove current branch indicator
    branches = [branch.strip() for branch in branches_unparsed]

    return branches


def can_push_branch(
    remote_name: str, branch_name: str, all_braches: Optional[List[str]] = None,
) -> bool:
    return not check_if_branch_exists(
        remote_name, branch_name, all_braches
    ) or is_branch_ancestor_of_origin(remote_name, branch_name)


def check_if_branch_exists(
    remote_name: str, branch_name: str, all_braches: Optional[List[str]] = None,
) -> bool:
    if all_braches is None:
        all_braches = get_all_branches()
    return f"remotes/{remote_name}/{branch_name}" in all_braches


def is_branch_ancestor_of_origin(remote_name: str, branch_name: str) -> bool:
    return (
        get_exit_code(
            f"git merge-base --is-ancestor {remote_name}/{branch_name} origin/{branch_name}"
        )
        == 0
    )


def get_current_remotes() -> List[str]:
    return shell_command("git remote").split("\n")
