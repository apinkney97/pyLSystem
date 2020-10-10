import pytest

from lsystem.tokenize import NUMBER_RE, DrawOp, DrawOpType, tokenize


@pytest.mark.parametrize(
    "string,modifiers,number",
    [
        ("", "", ""),
        ("6", "", "6"),
        ("qI123", "qI", "123"),
        ("xxx123", "", ""),
        ("QQiiQQ.54321XXX", "QQiiQQ", ".54321"),
        ("q1.q2", "q", "1."),
    ],
)
def test_regex(string, modifiers, number):
    match = NUMBER_RE.match(string)
    assert match["modifiers"] == modifiers
    assert match["number"] == number


@pytest.mark.parametrize(
    "string,expected",
    [
        ("", []),
        ("qwerty", []),
        (
            "@4  @i.25  @q16  @qi0.0625",
            [
                DrawOp(DrawOpType.SCALE, 4.0),
                DrawOp(DrawOpType.SCALE, 4.0),
                DrawOp(DrawOpType.SCALE, 4.0),
                DrawOp(DrawOpType.SCALE, 4.0),
            ],
        ),
        (
            "F+f[@iq2.0|]",
            [
                DrawOp(DrawOpType.DRAW_REL),
                DrawOp(DrawOpType.TURN_R_REL),
                DrawOp(DrawOpType.DRAW_REL),
                DrawOp(DrawOpType.GRAPHICS_SAVE),
                DrawOp(DrawOpType.SCALE, 0.7071067811865475),
                DrawOp(DrawOpType.TURN_180),
                DrawOp(DrawOpType.GRAPHICS_RESTORE),
            ],
        ),
        (
            r"FG-+DM\90/270!|@5<1>2C99[]",
            [
                DrawOp(DrawOpType.DRAW_REL),
                DrawOp(DrawOpType.MOVE_REL),
                DrawOp(DrawOpType.TURN_L_REL),
                DrawOp(DrawOpType.TURN_R_REL),
                DrawOp(DrawOpType.DRAW_ABS),
                DrawOp(DrawOpType.MOVE_ABS),
                DrawOp(DrawOpType.TURN_L_ABS, 90.0),
                DrawOp(DrawOpType.TURN_R_ABS, 270.0),
                DrawOp(DrawOpType.INVERT_TURNS),
                DrawOp(DrawOpType.TURN_180),
                DrawOp(DrawOpType.SCALE, 5.0),
                DrawOp(DrawOpType.DECREMENT_COLOUR, 1.0),
                DrawOp(DrawOpType.INCREMENT_COLOUR, 2.0),
                DrawOp(DrawOpType.SET_COLOUR, 99.0),
                DrawOp(DrawOpType.GRAPHICS_SAVE),
                DrawOp(DrawOpType.GRAPHICS_RESTORE),
            ],
        ),
    ],
)
def test_tokenize(string, expected):
    assert tokenize(string) == expected
