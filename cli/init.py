import os
from plumbum.colors import info

from errors import RootDirectoryNotFoundException


def handle_args(args):
    from core.config_loader import (
        get_config_path,
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
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    print("organization name: ", end="")
    organization_name = input("")
    if organization_name != "":
        try:
            file_path = f"{config_path}/organization_name"
            with open(file_path, "w") as f:
                f.write(organization_name + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    print("template repository: ", end="")
    template_name = input("")
    if template_name != "":
        try:
            file_path = f"{config_path}/template_repository_name"
            with open(file_path, "w") as f:
                f.write(template_name + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    print("user repository prefix: ", end="")
    user_repository_prefix = input("")
    if user_repository_prefix != "":
        if user_repository_prefix[-1] not in ("-", "_"):
            print(
                info
                | "Prefix usually has a deliminator, consider adding ('-', '_') after the prefix"
            )
        try:
            file_path = f"{config_path}/user_repository_prefix"
            with open(file_path, "w") as f:
                f.write(user_repository_prefix + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    if not os.path.isdir(f"{config_path}/active/"):
        os.mkdir(f"{config_path}/active/")

    if not os.path.isdir(f"{root_directory_path}/{IMPORTANT_DIRECTORY.OCTOPUS.value}"):
        os.mkdir(f"{root_directory_path}/{IMPORTANT_DIRECTORY.OCTOPUS.value}")

    if not os.path.isdir(
        f"{root_directory_path}/{IMPORTANT_DIRECTORY.LOCAL_CONFIG.value}"
    ):
        os.mkdir(f"{root_directory_path}/{IMPORTANT_DIRECTORY.LOCAL_CONFIG.value}")
