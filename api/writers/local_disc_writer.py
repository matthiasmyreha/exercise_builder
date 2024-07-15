import os
from typing import Dict

from dotenv import load_dotenv
from pydantic import ValidationError

from utils.files import write_file

from .writer import Writer

load_dotenv()


class LocalDiskWriter(Writer):
    def writeExerciseConfigs(
        self, config_results: Dict, output_dir: str = "data/out/"
    ) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for code, config in config_results.items():
            try:
                filename = f"{code}.json"
                file_path = os.path.join(output_dir, filename)
                write_file(config, file_path)
                print(f"Config for code {code} written to {file_path}")
            except ValidationError as e:
                print(f"Validation error: {e}")
