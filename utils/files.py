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


def write_file(data, path):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    print(path)
    with open(path, "w") as file:
        file.write(data)
