from dataclasses import dataclass, field
from typing import List, Optional

from lsystem.expander import Expander, Rules


@dataclass
class LSystem:
    title: str
    comments: List[str] = field(default_factory=list)
    angle: int = 0
    axiom: str = ""
    rules: Rules = field(default_factory=dict)
    expander: Optional[Expander] = None
    order: int = 2


def load(paths: List[str]) -> List[LSystem]:
    lsystems = []
    for path in paths:
        lsystems.extend(_load(path))
    return lsystems


def _load(path: str) -> List[LSystem]:
    lsystems = []
    lsystem = None
    with open(path) as f:
        for line in f:
            data, _, comment = line.partition(";")
            data = data.strip()
            comment = comment.strip()

            if lsystem is None and data.endswith("{"):
                title = data.partition("{")[0].strip()
                lsystem = LSystem(title=title)

            elif data.upper().startswith("ANGLE"):
                lsystem.angle = int(data[len("ANGLE ") :])

            elif data.upper().startswith("AXIOM"):
                lsystem.axiom = data[len("AXIOM ") :].upper()

            elif len(data) >= 2 and data[1] == "=":
                letter, _, commands = data.upper().partition("=")
                # Rules may be split across multiple lines - these are appended together
                lsystem.rules[letter] = lsystem.rules.get(letter, "") + commands

            if comment and lsystem is not None:
                lsystem.comments.append(comment)

            if data == "}":
                lsystem.expander = Expander(axiom=lsystem.axiom, rules=lsystem.rules)
                lsystems.append(lsystem)
                lsystem = None

    return lsystems
