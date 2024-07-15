from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class MinMax(BaseModel):
    min: Optional[Annotated[int, Field(ge=0)]] = None
    max: Optional[Annotated[int, Field(ge=0)]] = None


class ExerciseLevelConfigFilter(BaseModel):
    syllables: Optional[MinMax] = None
    word_length: Optional[MinMax] = None
    word_types: Optional[List[str]] = None  # maybe Literal["nound", "adjective", ...]


class ExerciseLevelConfigItemConfiguration(BaseModel):
    gaps: Optional[Annotated[int, Field(ge=0)]] = None
    distractors: Optional[Annotated[int, Field(ge=0)]] = None


class ExerciseLevelConfig(BaseModel):
    question: str
    filter: ExerciseLevelConfigFilter
    configuration: Optional[ExerciseLevelConfigItemConfiguration] = None


class LevelCondition(BaseModel):
    results: Annotated[int, Field(ge=0)]
    rounds: Annotated[int, Field(ge=0)]


class Level(BaseModel):
    level: Annotated[int, Field(ge=1)]
    level_down: LevelCondition
    level_up: LevelCondition
    tasks: Annotated[int, Field(ge=1)]


class InstructionContent(BaseModel):
    text: str


class Instructions(BaseModel):
    content: List[InstructionContent]
    type: str


class Configuration(BaseModel):
    answer_format_type: Literal["image", "audio", "custom"]
    answer_type: Literal["single-choice", "audio", "multiple-choice", "draw"]
    exercise_type: Literal["predefined", "dynamic"]
    show_bottom_bar: bool
    show_question: bool
    task_format_type: Literal["image", "audio", "custom", "multiple-gaps"]
    should_skip_to_next: Literal["on_correct", "if_correct", "never", "always"]


class ExerciseTemplate(BaseModel):
    code: str
    configuration: Configuration
    instructions: Instructions
    levels: List[Level]
    id: str
    exercises: List
