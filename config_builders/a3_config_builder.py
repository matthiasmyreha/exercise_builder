from model import (
    ExerciseLevelConfig,
    ExerciseLevelConfigFilter,
    ExerciseTemplate,
    Item,
)

from .config_builder import ConfigBuilder


class A3ConfigBuilder(ConfigBuilder):
    def __init__(self, template: ExerciseTemplate, config: list[ExerciseLevelConfig]):
        super().__init__(template, config)

    def filter_items(
        self, items: list[Item], filter: ExerciseLevelConfigFilter
    ) -> list[Item]:
        return super().filter_items(items, filter)

    def build(self, items: list[Item]):
        return super().build(items)

    def item_to_exercise_content(
        self,
        item: Item,
        config: ExerciseLevelConfig,
        level: int,
    ):
        return {
            "answers": [{"answer": item.name, "label": 1}],
            "exercise_id": f"{self.template.id}_lvl_{level}_{item.name}",
            "question": config.question,
            "tasks": [item.name],
        }
