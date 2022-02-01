#!/usr/bin/python3
import random

from canvas import *
from animals.animal import Animal
from animals.fish import Fish
from animals.shark import Shark
from animals.plankton import Plankton
import logging

class Game():
    def __init__(self):
        # Width of the world
        self.x_size: int = 10

        # Height of the world
        self.y_size: int = 5

        # If there are more animals than there is space in the world, raise an error
        if self.x_size * self.y_size < Fish.total + Shark.total:
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
        while sharks_placed < Shark.total:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Shark(x, y, random.randint(0, Shark.breed_age))
                sharks_placed += 1

        # Place fish randomly
        while fishes_placed < Fish.total:
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
    Game().run()