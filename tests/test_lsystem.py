from lsystem.expander import Expander
from lsystem.tokenize import DrawOp, DrawOpType


def test_get_no_rules():
    e = Expander(axiom="A", rules={})
    assert e.get_str(0) == "A"
    assert e.get_str(5) == "A"
    assert e.get_draw_ops(5) == []


def test_get_algae():
    e = Expander(axiom="A", rules={"A": "AB", "B": "A"})
    assert e.get_str(0) == "A"
    assert e.get_str(5) == "ABAABABAABAAB"
    assert e.get_draw_ops(5) == []


def test_get_dragon():
    e = Expander(axiom="FX", rules={"X": "X+YF+", "Y": "-FX-Y"})
    assert e.get_str(2) == "FX+YF++-FX-YF+"
    assert e.get_draw_ops(2) == [
        DrawOp(DrawOpType.DRAW_REL),  # :    F
        DrawOp(DrawOpType.TURN_R_REL),  # :  +
        DrawOp(DrawOpType.DRAW_REL),  # :    F
        DrawOp(DrawOpType.TURN_R_REL),  # :  +
        DrawOp(DrawOpType.TURN_R_REL),  # :  +
        DrawOp(DrawOpType.TURN_L_REL),  # :  -
        DrawOp(DrawOpType.DRAW_REL),  # :    F
        DrawOp(DrawOpType.TURN_L_REL),  # :  -
        DrawOp(DrawOpType.DRAW_REL),  # :    F
        DrawOp(DrawOpType.TURN_R_REL),  # :  +
    ]
