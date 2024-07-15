import random

from model import (
    ExerciseLevelConfig,
    ExerciseLevelConfigFilter,
    ExerciseTemplate,
    Item,
)

from .config_builder import ConfigBuilder


class C2ConfigBuilder(ConfigBuilder):
    def __init__(self, template: ExerciseTemplate, config: list[ExerciseLevelConfig]):
        super().__init__(template, config)

    def filter_items(
        self, items: list[Item], filter_config: ExerciseLevelConfigFilter
    ) -> list[Item]:
        filtered_items = super().filter_items(items, filter_config)
        return list(
            filter(
                lambda x: x.has_letter_distractors,
                filtered_items,
            )
        )

    def build(self, items: list[Item]):
        return super().build(items)

    def item_to_exercise_content(
        self,
        item: Item,
        level_config: ExerciseLevelConfig,
        level: int,
    ):
        if (
            level_config.configuration.gaps is None
            or level_config.configuration.distractors is None
        ):
            raise ("Level configuration for C2 must have gaps and distractors")

        def replace_compounds(word: str):
            return word.replace("SCH", "$").replace("SP", "#").replace("CH", "§")

        def restore_compounds(word: str):
            return word.replace("$", "SCH").replace("#", "SP").replace("§", "CH")

        blanked_letters = []
        indices = []
        blanked_word = replace_compounds(item.name.upper())

        for _ in range(level_config.configuration.gaps):
            random_index = random.randint(0, len(blanked_word) - 1)
            while random_index in indices:
                random_index = random.randint(0, len(blanked_word) - 1)
            indices.append(random_index)
            letter = blanked_word[random_index]
            blanked_letters.append(letter)
            blanked_word = (
                blanked_word[:random_index] + "_" + blanked_word[random_index + 1 :]
            )

        sorted_indices = sorted(range(len(indices)), key=lambda k: indices[k])

        distractors = random.sample(
            item.letter_distractors,
            min(level_config.configuration.distractors, len(item.letter_distractors)),
        )

        blanked_word = restore_compounds(blanked_word)
        blanked_letters = [restore_compounds(letter) for letter in blanked_letters]

        answers = [
            {"answer": distractor.upper(), "label": 0} for distractor in distractors
        ]
        answers += [
            {"answer": blanked_letters[i].upper(), "label": sorted_indices.index(i) + 1}
            for i in range(len(blanked_letters))
        ]

        return {
            "answers": answers,
            "exercise_id": f"{self.template.id}_lvl_{level}_{item.name}",
            "question": level_config.question,
            "tasks": [blanked_word],
        }
