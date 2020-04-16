import os
import argparse
from plumbum.colors import info, fatal
from typing import List

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

    try:
        root_directory_path = get_root_directory_path()
    except RootDirectoryNotFoundException:
        print("Creating glm folder structure in current folder")
        root_directory_path = get_current_pwd()

    config_path = f"{root_directory_path}/{IMPORTANT_DIRECTORY.CONFIG.value}"
    if not os.path.isdir(config_path):
        os.mkdir(config_path)

    print(
        "Either type in the correct value or if you want to skip or have already filled in the value press Enter"
    )

    print("token: ", end="")
    token = input("")
    if token != "":
        try:
            file_path = f"{root_directory_path}/token"
            with open(file_path, "w") as f:
                f.write(token + "\n")
            print(f"Writing to {file_path}", end="\n\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")

    print("organization name: ", end="")
    organization_name = input("")
    if organization_name != "":
        try:
            file_path = f"{config_path}/{Filenames.ORGANIZATION_NAME}"
            with open(file_path, "w") as f:
                f.write(organization_name + "\n")
            print(f"Writing to {file_path}", end="\n\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")

    print("template repository: ", end="")
    template_name = input("")
    if template_name != "":
        try:
            file_path = f"{config_path}/{Filenames.TEMPLATE_REPOSITORY_NAME.value}"
            with open(file_path, "w") as f:
                f.write(template_name + "\n")
            print(f"Writing to {file_path}", end="\n\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")

    print("user repository prefix: ", end="")
    user_repository_prefix = input("")
    if user_repository_prefix != "":
        if user_repository_prefix[-1] not in ("-", "_"):
            print(
                info
                | "Prefix usually has a deliminator, consider adding ('-', '_') after the prefix"
            )
        try:
            file_path = f"{config_path}/{Filenames.USER_REPOSITORY_PREFIX.value}"
            with open(file_path, "w") as f:
                f.write(user_repository_prefix + "\n")
            print(f"Writing to {file_path}", end="\n\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")

    print("Type enter to use the default")
    print("Report filename: ", end="")
    report_filename = input("")
    if report_filename != "":
        try:
            file_path = f"{config_path}/{Filenames.REPORT_FILENAME.value}"
            with open(file_path, "w") as f:
                f.write(report_filename + "\n")
            print(f"Writing to {file_path}", end="\n\n")
        except IOError:
            print(fatal | "Failed", end="\n\n")

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
