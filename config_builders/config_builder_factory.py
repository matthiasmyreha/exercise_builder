from model import ExerciseBuilderConfig

from .a3_config_builder import A3ConfigBuilder
from .c2_config_builder import C2ConfigBuilder


class ConfigBuilderFactory:
    _builders = {
        "a3": A3ConfigBuilder,
        "c2": C2ConfigBuilder,
    }

    @staticmethod
    def get_builder(config: ExerciseBuilderConfig):
        code = config.code

        builder_class = ConfigBuilderFactory._builders.get(code)

        if not builder_class:
            raise ValueError(f"No ConfigBuilder found for code: {code}")

        return builder_class(config)
