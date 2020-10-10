from typing import Dict, List

from lsystem.tokenize import DrawOp, tokenize

Rules = Dict[str, str]


class Expander:
    def __init__(self, axiom: str, rules: Rules):
        self.axiom = axiom
        self.rules = rules

        self._expansions: Dict[int, str] = {0: axiom}
        self._draw_ops: Dict[int, List[DrawOp]] = {}

    def get_str(self, n: int) -> str:
        if n < 0:
            raise ValueError(f"n must be positive, not {n}")
        if n not in self._expansions:
            self._expansions[n] = "".join(
                self.rules.get(c, c) for c in self.get_str(n - 1)
            )

        return self._expansions[n]

    def get_draw_ops(self, n: int):
        if n not in self._draw_ops:
            lsystem_str = self.get_str(n)
            self._draw_ops[n] = tokenize(lsystem_str)

        return self._draw_ops[n]
