import os
import argparse
from plumbum.colors import info, fatal
from typing import List, Callable, Optional

from errors import RootDirectoryNotFoundException
from remote.context import Filenames


def init_handler(args: List[str]):
    parser = argparse.ArgumentParser(
        prog="init", description="Command used for setting up the environment"
    )
    parser.parse_args(args)

    initialize_glm()


def initialize_glm():
    from core.config_loader import (
        get_current_pwd,
        get_root_directory_path,
        IMPORTANT_DIRECTORY,
    )

    # GENERATING
    try:
        root_directory_path = get_root_directory_path()
    except RootDirectoryNotFoundException:
        print("Creating glm folder structure in current folder")
        root_directory_path = get_current_pwd()

    config_path = f"{root_directory_path}/{IMPORTANT_DIRECTORY.CONFIG.value}"
    if not os.path.isdir(config_path):
        os.mkdir(config_path)

    if not os.path.isdir(f"{config_path}/active/"):
        os.mkdir(f"{config_path}/active/")

    octopus_directory_path = (
        f"{root_directory_path}/{IMPORTANT_DIRECTORY.OCTOPUS.value}"
    )
    if not os.path.isdir(octopus_directory_path):
        os.mkdir(octopus_directory_path)

    if not os.path.isdir(
        f"{root_directory_path}/{IMPORTANT_DIRECTORY.LOCAL_CONFIG.value}"
    ):
        os.mkdir(f"{root_directory_path}/{IMPORTANT_DIRECTORY.LOCAL_CONFIG.value}")

    review_directory_path = f"{root_directory_path}/{IMPORTANT_DIRECTORY.REVIEW.value}"
    if not os.path.isdir(review_directory_path):
        os.mkdir(review_directory_path)

    print(
        "Either type in the correct value or if you want to skip or have already filled in the value press Enter"
    )

    # TOKEN
    get_user_input_and_create_file("token: ", f"{root_directory_path}/token")

    # ORGANIZATION
    get_user_input_and_create_file(
        "organization name: ", f"{config_path}/{Filenames.ORGANIZATION_NAME.value}"
    )

    # TEMPLATE NAME
    get_user_input_and_create_file(
        "template repository: ",
        f"{config_path}/{Filenames.TEMPLATE_REPOSITORY_NAME.value}",
    )

    # REPO PREFIX
    get_user_input_and_create_file(
        "user repository prefix: ",
        f"{config_path}/{Filenames.USER_REPOSITORY_PREFIX.value}",
        repo_prefix_checker,
    )

    # REPORT FILENAME
    print("Type enter to use the default")
    get_user_input_and_create_file(
        "Report filename: ", f"{config_path}/{Filenames.REPORT_FILENAME.value}",
    )

    # REMOTE REPORT BRANCH NAME
    print("Type enter to use the default")
    get_user_input_and_create_file(
        "Remote report branch name: ",
        f"{config_path}/{Filenames.REMOTE_REPORT_BRANCH_NAME.value}",
    )


def get_user_input_and_create_file(
    message: str, file_path: str, checker: Optional[Callable[[str], None]] = None,
):
    print(message, end="")
    user_input = input("")
    if user_input != "":
        if checker is not None:
            checker(user_input)
        try:
            with open(file_path, "w") as f:
                f.write(user_input + "\n")
            print(f"Writing to {file_path}", end="\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")
    print()


def repo_prefix_checker(user_repository_prefix: str):
    if user_repository_prefix[-1] not in ("-", "_"):
        print(
            info
            | "Prefix usually has a deliminator, consider adding ('-', '_') after the prefix"
        )
