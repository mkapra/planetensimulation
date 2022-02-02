#!/usr/bin/python3
import random
import argparse

from canvas import *
from animals import *
import logging

class Game():
    def __init__(self, columns: 40, rows: 40, initial_fishes: 200, initial_sharks: 100, fish_breed: 5,
         shark_breed: 8, max_hunger: 5):

        # Width of the world
        self.x_size = columns

        # Height of the world
        self.y_size = rows

        Fish.breed_age = fish_breed
        Shark.breed_age = shark_breed
        Shark.max_hunger = max_hunger

        self.intial_fishes = initial_fishes
        self.initial_sharks = initial_sharks

        # If there are more animals than there is space in the world, raise an error
        if columns * rows < self.intial_fishes + self.initial_sharks:
            raise Exception("Not enough space for all animals")

        # Create the world
        self.world: list[list[Animal]] = []

        # Array of ids of animals that have moved, so they can't move twice
        self.moved_ids: list[int] = []

        # Initialize the world with plankton
        for x in range(self.x_size):
            self.world.append([])
            for y in range(self.y_size):
                self.world[x].append(Plankton(x, y))

    # Print the world to the console
    def print_world(self, _world):
        for row in _world:
            logging.debug(row)

    # Tick all animals in the world. This is the main logic of the game
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
                    # If the fish has already moved, skip it
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)

                    # Tick the fish
                    animal.tick(self.world, self.x_size, self.y_size)

        self.moved_ids.clear()

        # Tick all sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Shark:
                    # If the shark has already moved, skip it
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)

                    # Tick the shark
                    animal.tick(self.world, self.x_size, self.y_size)

        self.moved_ids.clear()

        # Loop world to count fish and sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Fish:
                    self.fishTotal += 1
                elif type(animal) is Shark:
                    self.sharkTotal += 1

        # Update the world plot
        for row in self.world:
            for animal in row:
                self.app.update_animal(animal.x, animal.y, animal.color)

        # Return statistics of the tick
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

        # Count how many fish and sharks have been created
        sharks_placed: int = 0
        fishes_placed: int = 0

        # Place sharks randomly
        while sharks_placed < self.initial_sharks:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Shark(x, y, random.randint(0, Shark.breed_age))
                sharks_placed += 1

        # Place fish randomly
        while fishes_placed < self.intial_fishes:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Fish(x, y, random.randint(0, Fish.breed_age))
                fishes_placed += 1

        self.print_world(self.world)

        # Create the canvas
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
    parser.add_argument("--rows", help="The rows of the field", type=int, default=40)
    parser.add_argument("--columns", help="The columns of the field", type=int, default=40)

    # Add breed cycles to the parser
    parser.add_argument("--fish_breed", help="Cycles until a fish can breed", type=int, default=5)
    parser.add_argument("--shark_breed", help="Cycles until a shark can breed", type=int, default=8)

    # Add hunger death cycles to the parser
    parser.add_argument("--max_hunger", help="Cycles until a shark dies due to hunger", type=int, default=5)

    # Add initial fishes and sharks to the parser
    parser.add_argument(
        "--initial_fishes", help="The number of fishes that are placed initially on the board", type=int, default=200)
    parser.add_argument(
        "--initial_sharks", help="The number of sharks that are placed initially on the board", type=int, default=100)

    # parse the arguments
    args = parser.parse_args()

    Game(rows=args.rows, columns=args.columns, initial_fishes=args.initial_fishes,
         initial_sharks=args.initial_sharks, fish_breed=args.fish_breed,
         shark_breed=args.shark_breed, max_hunger=args.max_hunger).run()
