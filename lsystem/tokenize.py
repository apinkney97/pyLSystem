import re
from enum import Enum
from math import sqrt
from typing import List, NamedTuple, Optional

NUMBER_RE = re.compile(
    r"""
        (?P<modifiers>
            [qi]*     # Any number of 'q' or 'i' characters
        )
        (?P<number>
            \d*       # Any number of digits
            \.?       # An optional decimal place
            \d*       # Any number of digits
        )
        (?!   # (-ve lookahead, ie non-capturing)
            [\d]      # Followed by anything except a digit
        )
    """,
    re.VERBOSE | re.IGNORECASE,
)


class BadNumberError(Exception):
    pass


class DrawOpType(Enum):
    DRAW_REL = "F"
    MOVE_REL = "G"
    TURN_L_REL = "-"
    TURN_R_REL = "+"
    DRAW_ABS = "D"
    MOVE_ABS = "M"
    TURN_L_ABS = "\\"
    TURN_R_ABS = "/"
    INVERT_TURNS = "!"
    TURN_180 = "|"
    SCALE = "@"
    DECREMENT_COLOUR = "<"
    INCREMENT_COLOUR = ">"
    SET_COLOUR = "C"
    GRAPHICS_SAVE = "["
    GRAPHICS_RESTORE = "]"


OP_TYPES_WITH_VALUES = {
    DrawOpType.TURN_L_ABS,
    DrawOpType.TURN_R_ABS,
    DrawOpType.SCALE,
    DrawOpType.DECREMENT_COLOUR,
    DrawOpType.INCREMENT_COLOUR,
    DrawOpType.SET_COLOUR,
}


# Pylint seems to have some bugs with Python 3.9 :(
# https://github.com/PyCQA/pylint/issues/3882
# https://github.com/PyCQA/pylint/issues/3876
class DrawOp(NamedTuple):  # pylint: disable=inherit-non-class
    type: DrawOpType
    value: Optional[float] = None  # pylint: disable=unsubscriptable-object


def tokenize(lsystem_string: str) -> List[DrawOp]:
    # Breaks up `lsystem_string` into draw operations

    draw_ops = []

    for i, char in enumerate(lsystem_string):
        value = None

        try:
            token_type = DrawOpType(char.upper())
        except ValueError:
            # Don't care, this is some char not used for drawing
            continue

        if token_type in OP_TYPES_WITH_VALUES:
            value = _parse_value(lsystem_string, i)
            # There is no need to skip over the chars matched by the
            # regex inside parse_value, as none of them are valid
            # drawing operators.

        draw_ops.append(DrawOp(token_type, value))

    return draw_ops


def _parse_value(lsystem_string: str, pos: int) -> float:
    match = NUMBER_RE.match(lsystem_string, pos=pos + 1)
    if match is None:
        raise Exception(
            "Regex didn't have any match. The developer didn't expect this..."
        )

    number = match["number"]
    modifiers = match["modifiers"].lower()
    try:
        value = float(number)
    except (ValueError, TypeError):
        remaining_str = lsystem_string[pos + 1 :]
        raise BadNumberError(
            f"Couldn't parse {number!r} as a float value for {lsystem_string[pos]!r}. "
            f"Remaining unparsed string: {remaining_str!r}"
        )
    if "q" in modifiers:
        value = sqrt(value)
    if "i" in modifiers:
        value = 1 / value

    return value
