from pydantic import ValidationError

from api.data_fetchers.sheets_data_fetcher import SheetsDataFetcher
from config_builders import ConfigBuilderFactory
from model import ExerciseBuilderConfig
from utils.files import read_json_files, write_file


def main():
    sheets_fetcher = SheetsDataFetcher()
    phonemes = sheets_fetcher.fetchPhonemes()
    categories = sheets_fetcher.fetchCategories()
    items = sheets_fetcher.fetchItems()
    config = sheets_fetcher.fetchExerciseLevelConfiguration()

    output_directory = "data/out/exercise_configs"
    config_directory = "data/in/exercise_builder_configs"
    json_configs = read_json_files(config_directory)

    for json_config in json_configs:
        try:
            config = ExerciseBuilderConfig(**json_config)
            print(f"Validation successful for {config.code}")
            try:
                builder = ConfigBuilderFactory.get_builder(config)
                result = builder.build(items)
                write_file(
                    result.model_dump_json(), f"{output_directory}/{config.code}.json"
                )
                print(f"Config for code {config.code} writte")
            except ValueError as e:
                print(e)
        except ValidationError as e:
            print(f"Validation error: {e}")


if __name__ == "__main__":
    main()
