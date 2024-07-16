from abc import ABC
from typing import List

from model import (
    ExerciseLevelConfig,
    ExerciseLevelConfigFilter,
    ExerciseTemplate,
    Item,
)
from model.exercise_builder_config import Exercise, ExerciseConfig


class ConfigBuilder(ABC):
    def __init__(self, template: ExerciseTemplate, config: list[ExerciseLevelConfig]):
        self.config = config
        self.template = template

    def filter_items(self, items: list[Item], filter_config: ExerciseLevelConfigFilter):
        filtered_items = items
        if "image" in {
            self.template.configuration.answer_format_type,
            self.template.configuration.task_format_type,
        }:
            filtered_items = list(filter(lambda x: x.has_image, filtered_items))

        if filter_config.syllables:
            syllables = filter_config.syllables
            min = syllables.min if syllables.min is not None else 0
            max = syllables.max if syllables.max is not None else 9999

            filtered_items = list(
                filter(
                    lambda x: min
                    <= (x.syllables if x.syllables is not None else 0)
                    <= max,
                    filtered_items,
                )
            )

        if filter_config.word_length:
            word_length = filter_config.word_length
            min = word_length.min if word_length.min is not None else 0
            max = word_length.max if word_length.max is not None else 9999

            filtered_items = list(
                filter(
                    lambda x: min <= (len(x.name) if x.name is not None else 0) <= max,
                    filtered_items,
                )
            )

        if filter_config.word_types:
            word_types = filter_config.word_types
            filtered_items = list(
                filter(
                    lambda x: x.word_type in word_types,
                    filtered_items,
                )
            )

        return filtered_items

    def build(self, items: list[Item]) -> ExerciseConfig:
        print(
            f"A3 Configuration Built with id {self.template.id} and {len(items)} items"
        )
        config = self.config
        exercises = []
        for index, level_config in enumerate(config):
            level = index + 1
            filtered_items_for_level = self.filter_items(items, level_config.filter)
            content_for_level = []
            for item in filtered_items_for_level:
                content_for_level.append(
                    self.item_to_exercise_content(item, level_config, level)
                )
            print(f"Level {index + 1} with {len(filtered_items_for_level)} items")
            exercises_for_level = Exercise(content=content_for_level, level=level)
            exercises.append(exercises_for_level)

        return ExerciseConfig(
            code=self.template.code,
            configuration=self.template.configuration,
            instructions=self.template.instructions,
            levels=self.template.levels,
            id=self.template.id,
            exercises=exercises,
        )

    def create_content_for_level(self) -> list[dict]:
        raise NotImplementedError("Subclasses should implement this method")
