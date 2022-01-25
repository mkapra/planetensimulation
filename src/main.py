#!/usr/bin/python3
import random

from canvas import *
from animals.animal import Animal
from animals.fish import Fish
from animals.shark import Shark


def print_world(_world):
    for row in _world:
        print(row)


if __name__ == "__main__":
    print("Planetensimulation")

    x_size = 50
    y_size = 50
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

    print_world(world)

    canvas = Canvas(world, x_size, y_size)
