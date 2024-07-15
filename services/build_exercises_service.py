from pydantic import ValidationError

from api.data_fetchers.data_fetcher import DataFetcher
from api.writers.writer import Writer
from config_builders import ConfigBuilderFactory
from model import ExerciseLevelConfig, ExerciseTemplate
from utils.files import read_json_file


def build_exercises(fetcher: DataFetcher, writer: Writer):
    phonemes = fetcher.fetchPhonemes()
    categories = fetcher.fetchCategories()
    items = fetcher.fetchItems()
    configs = fetcher.fetchExerciseLevelConfiguration()

    config_directory = "data/in/exercise_builder_configs"
    config_results = {}
    for code, json_config in configs.items():
        try:
            exercise_template_json = read_json_file(f"{config_directory}/{code}.json")
            exercise_template = ExerciseTemplate(**exercise_template_json)
            exercise_config = [
                ExerciseLevelConfig(**level_config) for level_config in json_config
            ]
            try:
                builder = ConfigBuilderFactory.get_builder(
                    code, exercise_template, exercise_config
                )
                print(f"Validation successful for {code}")
                print(code, exercise_template)
                result = builder.build(items)
                config_results[code] = result.model_dump_json()
                print(f"Config for code {code} written")
            except ValueError as e:
                print(e)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except ValidationError as e:
            print(f"Validation error: {e}")
    print("RES", config_results.keys())
    if len(config_results) > 0:
        writer.writeExerciseConfigs(config_results)
