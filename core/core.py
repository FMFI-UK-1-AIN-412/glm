import os

def organization_name():
    return "glm-testing"

def user_repo_prefix():
    return "osprog18-"

def get_repo_name(university_login) -> str:
    return user_repo_prefix() + university_login

def save_student(university_login, remote_login):
    path = os.getcwd()
    if os.path.exists(path + university_login):
        print(f"File for {university_login} already exists")
    else:
        try:
            f = open("./active/" + university_login, "w")
            f.write(remote_login + "\n")
            f.close()
        except:
            print(f"Error while writing file {university_login}")

def delete_student(university_login):
    if os.path.exists("./active/" + university_login):
        try:
            os.remove("./active/" + university_login)
            print(f"Student {university_login} removed from active students")
        except:
            print(f"Failed removing {university_login} from active students")
    else:
        print(f"Student {university_login} is an active student")


def active_students():
    students = []
    for file_name in os.listdir("./active"):
        file = open("./active/" + file_name)
        students.append((file_name, file.readline()[:-1]))
        file.close()
    return students

def get_token():
    with open("token") as f:
        token = f.readline()
        if token[-1] == "\n":
            token = token[:-1]
        return token

def generate_name(university_login):
    return user_repo_prefix() + university_login

if __name__ == "__main__":
    print("Printing database summary")
    print(f"user repo prefix = {user_repo_prefix()}")
    print(f"organization name = {organization_name()}")
    students = "".join(map(lambda x: "\t" + x[0] + " -> " + x[1] + "\n", active_students()))
    print(f"active stundets = \n {students}")
