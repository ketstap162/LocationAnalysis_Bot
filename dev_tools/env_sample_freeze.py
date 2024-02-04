import os

current_directory = os.path.dirname(__file__)

env_file_path = os.path.join(current_directory, "..", ".env")
env_sample_file_path = os.path.join(current_directory, "..", ".env.sample")

with open(env_file_path, "r") as env_file:
    with open(env_sample_file_path, "w") as env_sample_file:
        data = ""
        for line in env_file:
            if line.isspace() or line == "":
                data += "\n"
            else:
                data += line.split("=")[0] + "\n"

        env_sample_file.write(data.strip())

print("ENV VARIABLES FREEZED!")
