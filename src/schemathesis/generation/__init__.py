from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Union

from hypothesis import strategies as st


class DataGenerationMethod(str, Enum):
    """Defines what data Schemathesis generates for tests."""

    # Generate data, that fits the API schema
    positive = "positive"
    # Doesn't fit the API schema
    negative = "negative"

    @classmethod
    def default(cls) -> DataGenerationMethod:
        return cls.positive

    @classmethod
    def all(cls) -> list[DataGenerationMethod]:
        return list(DataGenerationMethod)

    def as_short_name(self) -> str:
        return {
            DataGenerationMethod.positive: "P",
            DataGenerationMethod.negative: "N",
        }[self]

    @property
    def is_negative(self) -> bool:
        return self == DataGenerationMethod.negative

    @classmethod
    def ensure_list(
        cls, value: DataGenerationMethodInput
    ) -> list[DataGenerationMethod]:
        if isinstance(value, DataGenerationMethod):
            return [value]
        return list(value)


DataGenerationMethodInput = Union[DataGenerationMethod, Iterable[DataGenerationMethod]]

DEFAULT_DATA_GENERATION_METHODS = (DataGenerationMethod.default(),)


CASE_ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(CASE_ID_ALPHABET)
# Separate `Random` as Hypothesis might interfere with the default one
RANDOM = random.Random()


def generate_random_case_id(length: int = 6) -> str:
    number = RANDOM.randint(62 ** (length - 1), 62**length - 1)
    output = ""
    while number > 0:
        number, rem = divmod(number, BASE)
        output += CASE_ID_ALPHABET[rem]
    return output


@dataclass
class GenerationConfig:
    """Holds various configuration options relevant for data generation."""

    # Allow generating `\x00` bytes in strings
    allow_x00: bool = True
    # Generate strings using the given codec
    codec: str | None = "utf-8"


ASCII_CHAR_ST = st.characters(
    blacklist_categories=("Cs",), min_codepoint=33, max_codepoint=126
)
ASCII_TEXT_ST = st.text(alphabet=ASCII_CHAR_ST, min_size=0)

JP_CHAR_ST = st.characters(
    blacklist_categories=("Cs",),
    min_codepoint=ord("\u3040"),
    max_codepoint=ord("\u309F"),
)
JP_TEXT_ST = st.text(alphabet=JP_CHAR_ST, min_size=0)
AVAILABLE_LANGUAGES = ["en", "jp"]
AVAILABLE_LANGUAGES_ST = {
    "en": {"char": ASCII_CHAR_ST, "text": ASCII_TEXT_ST},
    "jp": {"char": JP_CHAR_ST, "text": JP_TEXT_ST},
}
