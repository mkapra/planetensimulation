from animals.animal import Animal
from animals.plankton import Plankton

import random
import logging

class Fish(Animal):

    color = 'green'
    breed_age = 5
    id = 0

    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
        self.id = Fish.id
        Fish.id = Fish.id + 1

    def __repr__(self):
        return f"F{self.age}"

    def is_empty(self, x, y, world):
        return type(world[x][y]) == Plankton

    def make_move(self, world, neighbours):
        # Pick a random neighbouring cell
        neighbour = random.choice(neighbours)

        # If old enough, give birth to a new fish
        if self.age >= self.breed_age:
            logging.debug(f"Fish {self.id} gave birth")
            world[self.x][self.y] = Fish(self.x, self.y, 0)
            self.age = -1
        else:
            world[self.x][self.y] = Plankton(self.x, self.y)

        # Move to that cell
        logging.debug(f"Fish {self.id} moved from ({self.x}, {self.y}) to ({neighbour.x}, {neighbour.y})")
        self.x = neighbour.x
        self.y = neighbour.y
        world[self.x][self.y] = self

    def tick(self, world, x_size, y_size):
        # Look for free neighbouring cells
        neighbours = self.get_free_neighbours(self.x, self.y, x_size, y_size, world)
        if len(neighbours) > 0:
            # Found a free neighbouring cell
            logging.debug(f"Fish {self.id} found free neighbour")
            self.make_move(world, neighbours)

        # Increase age
        self.age += 1