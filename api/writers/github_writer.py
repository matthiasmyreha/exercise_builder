import os
import os.path
import tempfile
from datetime import datetime
from typing import Dict

from dotenv import load_dotenv
from git import GitCommandError, Repo
from pydantic import ValidationError

from utils.files import write_file

from .writer import Writer

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/matthiasmyreha/exercise_configs"


def generate_branch_name():
    current_time = datetime.now().strftime("%Y%m%d-%H%M")
    return f"ec_{current_time}"


class GithubWriter(Writer):
    def writeExerciseConfigs(self, config_results: Dict) -> str:
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                repo = Repo.clone_from(REPO_URL, tmpdirname)
                branch_name = generate_branch_name()
                new_branch = repo.create_head(branch_name)
                new_branch.checkout()

                for code, config in config_results.items():
                    try:
                        filename = f"{code}.json"
                        write_file(
                            config,
                            f"{tmpdirname}/{filename}",
                        )
                        repo.index.add([filename])
                        print(f"Config for code {code} written")
                    except ValidationError as e:
                        print(f"Validation error: {e}")

                repo.index.commit("Exercise configs written")
                origin = repo.remote(name="origin")
                origin.push(refspec=f"{branch_name}:{branch_name}")

            except GitCommandError as e:
                print(f"Git operation failed: {e}")
