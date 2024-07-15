import json
import os


def read_json_files(directory: str):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                config = json.load(file)
                files.append(config)
    return files


def read_json_file(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")
    with open(path, "r") as file:
        config = json.load(file)
        return config


def write_file(data, path):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    print(path)
    with open(path, "w") as file:
        file.write(data)
