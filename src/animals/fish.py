from . import *

import random
import logging

class Fish(Animal):

    # Color of the fish
    color = 'green'

    # How many iterations to wait before giving birth
    breed_age = 5

    # Global variable to keep track of the id of the next id
    id = 0

    def __init__(self, x, y, age):
        super().__init__(x, y, self.color, self.breed_age, self.id, age)

        Fish.id = Fish.id + 1

    # Move to a random neighbouring cell and give birth if old enough
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

    # Tick the fish
    def tick(self, world, x_size, y_size):
        # Look for free neighbouring cells
        neighbours = self.get_free_neighbours(self.x, self.y, x_size, y_size, world)
        if len(neighbours) > 0:
            # Found a free neighbouring cell, move there
            logging.debug(f"Fish {self.id} found free neighbour")
            self.make_move(world, neighbours)

        # Increase age
        self.age += 1