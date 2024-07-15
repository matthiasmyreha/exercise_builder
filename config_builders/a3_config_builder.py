from model import (
    ExerciseBuilderConfig,
    ExerciseLevelConfig,
    ExerciseLevelConfigFilter,
    Item,
)

from .config_builder import ConfigBuilder


class A3ConfigBuilder(ConfigBuilder):
    def __init__(self, config: ExerciseBuilderConfig):
        super().__init__(config)

    def filter_items(
        self, items: list[Item], filter: ExerciseLevelConfigFilter
    ) -> list[Item]:
        return super().filter_items(items, filter)

    def build(self, items: list[Item]):
        return super().build(items)

    def item_to_exercise_content(
        self,
        item: Item,
        level_config: ExerciseLevelConfig,
        level: int,
    ):
        return {
            "answers": [{"answer": item.name, "label": 1}],
            "exercise_id": f"{self.config.id}_lvl_{level}_{item.name}",
            "question": level_config.question,
            "tasks": [item.name],
        }
