import os


def env_setup():
    current_directory = os.path.dirname(__file__)

    env_file_path = os.path.join(current_directory, "..", ".env")

    with open(env_file_path, "r") as env_file:
        for line in env_file:
            if not(line.isspace() or line == ""):
                data = line.strip().split("=")
                os.environ[data[0]] = data[1]

    print("ENV IS SETUP!")
