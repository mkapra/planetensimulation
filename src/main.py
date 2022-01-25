#!/usr/bin/python3
import random
import time
import threading

from canvas import *
from animals.animal import Animal
from animals.fish import Fish
from animals.shark import Shark


def print_world(_world):
    for row in _world:
        print(row)


def loop(_canvas):
    colors = ['red', 'blue', 'green']
    for i in range(100):
        print(f"Update {i}")
        time.sleep(1)
        for _x in range(25):
            for _y in range(25):
                _canvas.update_animal(_x, _y, colors[random.randint(0, 2)])

# [
# {
# Animal: [Total, New, Died]
# Fish: [100, 20, 30],
# Shark: [100, 20, 30]
# },
# {
# Animal: [Total, New, Died]
# Fish: [100, 20, 30],
# Shark: [100, 20, 30]
# }
# ]

# {
# FishTotal: []
# FishNew: []
# ...
# }

def end_report():
    pass


if __name__ == "__main__":
    print("Planetensimulation")

    x_size = 25
    y_size = 25
    world: "list[list[Animal|None]]" = [[None] * y_size for i in range(x_size)]

    for x in range(x_size):
        for y in range(y_size):
            randint: int = random.randint(0, 2)
            if randint == 0:
                world[x][y] = None
            elif randint == 1:
                world[x][y] = Fish(x, y)
            else:
                world[x][y] = Shark(x, y)

    # print_world(world)

    canvas = Canvas(world, x_size, y_size)

    x = threading.Thread(target=loop, args=(canvas,))
    x.start()

    canvas.start_loop()
