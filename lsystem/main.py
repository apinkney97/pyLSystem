import sys
from glob import glob

import pygame  # type: ignore

from lsystem.canvas import Canvas
from lsystem.load import load

FPS = 10


def main():
    pygame.init()

    size = (640, 480)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    files = glob("*.l")
    print(files)
    lsystems = load(files)
    for l in lsystems:
        print(l)

    # angle = 4
    # axiom = "FX"
    # rules = {"X": "X+YF+", "Y": "-FX-Y"}
    # order = 7
    #
    # axiom = "+Fa"
    # rules = {"a": ">1[@0.48[-Fa][Fa][+Fa]]"}

    lsystem_index = 0

    canvas = Canvas(screen, lsystems[lsystem_index])

    canvas.draw()

    while True:
        for event in pygame.event.get():
            redraw = False
            # if event.type != pygame.MOUSEMOTION:
            #     print(event)

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                redraw = True

            if event.type == pygame.KEYUP:
                if event.scancode == pygame.KSCAN_UP:
                    canvas.order += 1
                    redraw = True
                elif event.scancode == pygame.KSCAN_DOWN:
                    canvas.order -= 1
                    redraw = True
                elif event.scancode == pygame.KSCAN_MINUS:
                    canvas.angle -= 1
                    redraw = True
                elif event.scancode == pygame.KSCAN_EQUALS:
                    canvas.angle += 1
                    redraw = True
                elif event.scancode == pygame.KSCAN_RIGHT:
                    lsystem_index = (lsystem_index + 1) % len(lsystems)
                    canvas.lsystem = lsystems[lsystem_index]
                    redraw = True
                elif event.scancode == pygame.KSCAN_LEFT:
                    lsystem_index = (lsystem_index - 1) % len(lsystems)
                    canvas.lsystem = lsystems[lsystem_index]
                    redraw = True

            if redraw:
                canvas.draw()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
