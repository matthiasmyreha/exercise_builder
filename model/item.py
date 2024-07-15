from typing import List, NamedTuple


class Item(NamedTuple):
    id: str
    locale: str
    name: str
    phonemes: List[str]
    category: str
    image: str
    has_image: bool
    gender: str
    type: str
    syllables: int
    word_type: str
    has_letter_distractors: bool
    letter_distractors: List[str]
