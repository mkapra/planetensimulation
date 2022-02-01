#!/usr/bin/python3
import random
import argparse

from canvas import *
from animals.animal import Animal
from animals.fish import Fish
from animals.shark import Shark
from animals.plankton import Plankton
import logging

class Game():
    def __init__(self, columns: 10, rows: 5):
        self.x_size = columns
        self.y_size = rows
        if columns * rows < Fish.total + Shark.total:
            raise Exception("Not enough space for all animals")

        self.world: list[list[Animal]] = []
        self.moved_ids: list[int] = []

        for x in range(self.x_size):
            self.world.append([])
            for y in range(self.y_size):
                self.world[x].append(Plankton(x, y))

    def print_world(self, _world):
        for row in _world:
            logging.debug(row)

    def tick(self):
        self.fishTotal = 0
        self.fishNew = 0
        self.fishDied = 0
        self.sharkTotal = 0
        self.sharkNew = 0
        self.sharkDied = 0

        logging.debug("tick")
        # Tick all fish
        for row in self.world:
            for animal in row:
                if type(animal) is Fish:
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)
                    animal.tick(self.world, self.x_size, self.y_size)
        self.moved_ids.clear()

        # Tick all sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Shark:
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)
                    animal.tick(self.world, self.x_size, self.y_size)
        self.moved_ids.clear()

        # Loop world to count fish and sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Fish:
                    self.fishTotal += 1
                elif type(animal) is Shark:
                    self.sharkTotal += 1

        # self.print_world(self.world)

        # Update the world
        for row in self.world:
            for animal in row:
                self.app.update_animal(animal.x, animal.y, animal.color)

        return {
            'fishTotal': self.fishTotal,
            'fishNew': self.fishNew,
            'fishDied': self.fishDied,
            'sharkTotal': self.sharkTotal,
            'sharkNew': self.sharkNew,
            'sharkDied': self.sharkDied
        }

    def run(self):
        logging.info("Planetensimulation")

        sharks_placed: int = 0
        fishes_placed: int = 0

        # Place sharks
        while sharks_placed < Shark.total:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Shark(x, y, random.randint(0, Shark.breed_age))
                sharks_placed += 1

        # Place fish
        while fishes_placed < Fish.total:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Fish(x, y, random.randint(0, Fish.breed_age))
                fishes_placed += 1

        self.print_world(self.world)

        root = tk.Tk()
        self.app = App(self, self.x_size, self.y_size, self.world, root)
        root.title("Number of fishes and sharks")
        root.resizable(False, False)
        self.app.pack()
        root.mainloop()


if __name__ == "__main__":
    # create parser
    parser = argparse.ArgumentParser()

    # Add rows and columns to the parser
    parser.add_argument("--rows", help="The rows of the field", type=int, default=10)
    parser.add_argument("--columns", help="The columns of the field", type=int, default=5)

    # parse the arguments
    args = parser.parse_args()

    Game(rows=args.rows, columns=args.columns).run()