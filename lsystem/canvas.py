import dataclasses
from colorsys import hsv_to_rgb
from math import cos, radians, sin
from typing import List, Tuple

import pygame  # type: ignore

from lsystem.load import LSystem
from lsystem.tokenize import DrawOpType

Coord = Tuple[float, float]
RGBColour = Tuple[int, int, int]


@dataclasses.dataclass
class GraphicsState:
    pos: Coord = (0, 0)
    angle_rel: float = 90
    angle_abs: float = 90
    length: float = 50
    reverse: bool = False
    colour: int = 0


class Canvas:
    def __init__(self, screen, lsystem: LSystem):
        self.screen = screen

        self._lsystem = lsystem

        self.angle = lsystem.angle
        self.state = GraphicsState()
        self.graphics_stack: List[GraphicsState] = []

        self.min_x = 0.0
        self.max_x = 0.0
        self.min_y = 0.0
        self.max_y = 0.0

        num_colours = 20

        self.colours = [(0, 0, 0), (255, 255, 255)]

        for n in range(num_colours):
            self.colours.append(
                tuple(int(c * 255) for c in hsv_to_rgb(n / num_colours, 1, 1))
            )

    @property
    def lsystem(self) -> LSystem:
        return self._lsystem

    @lsystem.setter
    def lsystem(self, lsystem: LSystem) -> None:
        self._lsystem = lsystem
        self.angle = lsystem.angle

    @property
    def order(self) -> int:
        return self._lsystem.order

    @order.setter
    def order(self, value: int) -> None:
        self._lsystem.order = max(value, 0)

    @property
    def angle(self) -> int:
        return self._angle

    @angle.setter
    def angle(self, value: int) -> None:
        self._angle = max(value, 3)
        self._angle_degrees = 360 / self._angle

    @property
    def _reverse(self):
        if self.state.reverse:
            return -1
        return 1

    def draw(self) -> None:
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self._draw(paint=False)
        self._draw(paint=True)

        num_chars = len(self.lsystem.expander.get_str(self.order))
        num_ops = len(self.lsystem.expander.get_draw_ops(self.order))
        pygame.display.set_caption(
            f"{self.lsystem.title}: Order {self.order}, Angle {self.angle}, "
            f"({num_chars} chars, {num_ops} ops)"
        )

    def _draw(self, paint: bool):

        self.state = GraphicsState()
        self.graphics_stack = []

        if paint:
            window_w, window_h = pygame.display.get_window_size()
            image_w = max(self.max_x - self.min_x, 1)
            image_h = max(self.max_y - self.min_y, 1)

            x_scale = window_w / image_w
            y_scale = window_h / image_h

            if x_scale < y_scale:
                scale = x_scale
                x_padding = 0
                y_padding = (window_h - scale * image_h) / 2
            else:
                scale = y_scale
                x_padding = (window_w - scale * image_w) / 2
                y_padding = 0

            start_x = abs(self.min_x) * scale + x_padding
            start_y = abs(self.min_y) * scale + y_padding
            self.state.pos = (start_x, start_y)
            self.state.length = self.state.length * scale

        self.screen.fill(self.colours[0])

        for op in self.lsystem.expander.get_draw_ops(self.order):

            if op.type in {DrawOpType.DRAW_REL, DrawOpType.MOVE_REL}:
                pos_before = self.state.pos
                self.move_rel()
                if paint and op.type is DrawOpType.DRAW_REL:
                    self.draw_line(pos_before)

            elif op.type in {DrawOpType.DRAW_ABS, DrawOpType.MOVE_ABS}:
                pos_before = self.state.pos
                self.move_abs()
                if paint and op.type is DrawOpType.DRAW_ABS:
                    self.draw_line(pos_before)

            elif op.type is DrawOpType.TURN_R_REL:
                self.state.angle_rel += self._reverse * self._angle_degrees

            elif op.type is DrawOpType.TURN_L_REL:
                self.state.angle_rel -= self._reverse * self._angle_degrees

            elif op.type is DrawOpType.TURN_R_ABS:
                self.state.angle_abs += self._reverse * op.value

            elif op.type is DrawOpType.TURN_L_ABS:
                self.state.angle_abs -= self._reverse * op.value

            elif op.type is DrawOpType.SCALE:
                self.state.length *= op.value

            elif op.type is DrawOpType.GRAPHICS_SAVE:
                state_copy = dataclasses.replace(self.state)
                self.graphics_stack.append(state_copy)

            elif op.type is DrawOpType.GRAPHICS_RESTORE:
                if self.graphics_stack:
                    self.state = self.graphics_stack.pop()
                else:
                    print("Empty graphics stack")

            elif op.type is DrawOpType.INVERT_TURNS:
                self.state.reverse = not self.state.reverse

            elif op.type is DrawOpType.TURN_180:
                self.state.angle_rel += self._angle_degrees * int(self.angle / 2)

            elif op.type is DrawOpType.DECREMENT_COLOUR:
                self.state.colour -= int(op.value)

            elif op.type is DrawOpType.INCREMENT_COLOUR:
                self.state.colour += int(op.value)

            elif op.type is DrawOpType.SET_COLOUR:
                self.state.colour = int(op.value)

            else:
                print(f"Unsupported op {op!r}")

        pygame.display.update()

    def draw_line(self, coord: Coord):
        # Draws line from `coord` to current position
        index = self.state.colour % (len(self.colours) - 1)
        colour = self.colours[index + 1]  # index 0 is the background colour
        pygame.draw.aaline(self.screen, colour, coord, self.state.pos)

    def move_rel(self) -> None:
        self._move(self.state.angle_rel)

    def move_abs(self) -> None:
        self._move(self.state.angle_abs)

    def _move(self, angle: float) -> None:
        x, y = self.state.pos

        new_x = x + self.state.length * sin(radians(angle))
        new_y = y + self.state.length * cos(radians(angle))

        self.min_x = min(self.min_x, new_x)
        self.max_x = max(self.max_x, new_x)
        self.min_y = min(self.min_y, new_y)
        self.max_y = max(self.max_y, new_y)

        self.state.pos = (new_x, new_y)
