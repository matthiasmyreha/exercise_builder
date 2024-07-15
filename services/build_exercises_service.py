import os
import tempfile
from datetime import datetime

from git import GitCommandError, Repo
from pydantic import ValidationError

from api.data_fetchers.sheets_data_fetcher import SheetsDataFetcher
from config_builders import ConfigBuilderFactory
from model import ExerciseBuilderConfig
from utils.files import read_json_files, write_file

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/matthiasmyreha/exercise_configs"


def generate_branch_name():
    current_time = datetime.now().strftime("%Y%m%d-%H%M")
    return f"ec_{current_time}"


def build_exercises():
    sheets_fetcher = SheetsDataFetcher()
    phonemes = sheets_fetcher.fetchPhonemes()
    categories = sheets_fetcher.fetchCategories()
    items = sheets_fetcher.fetchItems()
    config = sheets_fetcher.fetchExerciseLevelConfiguration()

    config_directory = "data/in/exercise_builder_configs"
    json_configs = read_json_files(config_directory)
    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            repo = Repo.clone_from(REPO_URL, tmpdirname)
            branch_name = generate_branch_name()
            new_branch = repo.create_head(branch_name)
            new_branch.checkout()

            written_configs = []
            for json_config in json_configs:
                try:
                    config = ExerciseBuilderConfig(**json_config)
                    print(f"Validation successful for {config.code}")
                    try:
                        builder = ConfigBuilderFactory.get_builder(config)
                        result = builder.build(items)
                        filename = f"{config.code}.json"
                        write_file(
                            result.model_dump_json(),
                            f"{tmpdirname}/{filename}",
                        )
                        repo.index.add([filename])
                        written_configs.append(config.code)
                        print(f"Config for code {config.code} writte")
                    except ValueError as e:
                        print(e)
                except ValidationError as e:
                    print(f"Validation error: {e}")

            repo.index.commit("Exercise configs written")
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{branch_name}:{branch_name}")

        except GitCommandError as e:
            print(f"Git operation failed: {e}")
