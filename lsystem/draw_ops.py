"""
TODO: Work out if this is a sensible replacement for the current enum implementation
"""
DRAW_OPS = {}


class DrawOp:

    draw_char: str = ""

    def __init__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        draw_char = cls.draw_char
        if len(draw_char) != 1:
            raise Exception(f"Invalid draw char {draw_char!r}")
        if draw_char in DRAW_OPS:
            raise Exception(f"Duplicate DrawOp {draw_char}")
        DRAW_OPS[draw_char] = cls


# class DrawOpType(Enum):
#     DRAW_REL = "F"
#     MOVE_REL = "G"
#     TURN_L_REL = "-"
#     TURN_R_REL = "+"
#     DRAW_ABS = "D"
#     MOVE_ABS = "M"
#     TURN_L_ABS = "\\"
#     TURN_R_ABS = "/"
#     INVERT_TURNS = "!"
#     TURN_180 = "|"
#     SCALE = "@"
#     DECREMENT_COLOUR = "<"
#     INCREMENT_COLOUR = ">"
#     SET_COLOUR = "C"
#     GRAPHICS_SAVE = "["
#     GRAPHICS_RESTORE = "]"
#
#
# OP_TYPES_WITH_VALUES = {
#     DrawOpType.TURN_L_ABS,
#     DrawOpType.TURN_R_ABS,
#     DrawOpType.SCALE,
#     DrawOpType.DECREMENT_COLOUR,
#     DrawOpType.INCREMENT_COLOUR,
#     DrawOpType.SET_COLOUR,
# }
