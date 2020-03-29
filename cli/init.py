import os


def handle_args(args):
    from core.config_loader import get_local_config_path

    print(
        "Either type in the correct value or if you want to skip or have already filled in the value press Enter"
    )
    print("Type in organization name or press Enter to skip")

    local_config_path = get_local_config_path()
    if not os.path.isdir(local_config_path):
        os.mkdir(local_config_path)

    organization_name = input("")
    if organization_name != "":
        try:
            file_path = f"{local_config_path}/organization_name"
            with open(file_path, "w") as f:
                f.write(organization_name + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    print("Type in the name of template repository to use or press Enter to skip")
    template_name = input("")
    if template_name != "":
        try:
            file_path = f"{local_config_path}/template_repository_name"
            with open(file_path, "w") as f:
                f.write(template_name + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")

    print("Type in user repository prefix or press Enter to skip")
    user_repository_prefix = input("")
    if user_repository_prefix != "":
        try:
            file_path = f"{local_config_path}/user_repository_prefix"
            with open(file_path, "w") as f:
                f.write(user_repository_prefix + "\n")
            print(f"Writing to {file_path}")
        except IOError:
            print("Failed")
