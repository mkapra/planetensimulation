from . import *

import random
import logging

class Shark(Animal):

    # Color of the shark
    color = 'red'

    # How many iterations to wait before giving birth
    breed_age = None

    # How many iterations to wait before dying of hunger
    max_hunger = None

    # Static variable to keep track of the next id
    id = 0

    def __init__(self, x, y, age):
        super().__init__(x, y, self.color, self.breed_age, self.id, age)

        self.hunger = 0
        Shark.id = Shark.id + 1

    # Check if neighbouring cells contain fish
    def get_fish_neighbours(self, x, y, x_size, y_size, world):
        neighbours = []

        # Check cell above
        if self.is_fish(world[(x) % x_size][(y-1) % y_size]):
            neighbours.append(world[(x) % x_size][(y-1) % y_size])
        # Check cell below
        if self.is_fish(world[(x) % x_size][(y+1) % y_size]):
            neighbours.append(world[(x) % x_size][(y+1) % y_size])
        # Check cell left
        if self.is_fish(world[(x-1) % x_size][(y) % y_size]):
            neighbours.append(world[(x-1) % x_size][(y) % y_size])
        # Check cell right
        if self.is_fish(world[(x+1) % x_size][(y) % y_size]):
            neighbours.append(world[(x+1) % x_size][(y) % y_size])

        return neighbours

    # Check if the cell contains a fish
    def is_fish(self, animal):
        return type(animal) == Fish

    # Try to move to a neighbouring cell containing a fish.
    # Else move to a free neighbouring cell.
    # Give birth if the shark is old enough.
    def make_move(self, world, neighbours):
        # Pick a random neighbouring cell
        neighbour = random.choice(neighbours)

        # If old enough, give birth to a new shark
        if self.age >= self.breed_age:
            logging.debug(f"Shark {self.id} gave birth")
            world[self.x][self.y] = Shark(self.x, self.y, 0)
            self.age = -1
        else:
            world[self.x][self.y] = Plankton(self.x, self.y)

        # Move to that cell
        logging.debug(f"Shark {self.id} moved from ({self.x}, {self.y}) to ({neighbour.x}, {neighbour.y})")
        self.x = neighbour.x
        self.y = neighbour.y
        world[self.x][self.y] = self

    # Tick the shark
    def tick(self, world, x_size, y_size):
        # Look for fish in neighbouring cells
        neighbours = self.get_fish_neighbours(self.x, self.y, x_size, y_size, world)
        if len(neighbours) > 0:
            # Found a fish in a neighbouring cell
            logging.debug(f"Shark {self.id} found a fish")
            self.make_move(world, neighbours)
            # Reset hunger
            self.hunger = 0
            self.age += 1
            return

        # No fish has been found. Move to a free neighbouring cell
        logging.debug(f"Shark {self.id} found no fish")
        neighbours = self.get_free_neighbours(self.x, self.y, x_size, y_size, world)
        if len(neighbours) > 0:
            # Found a free neighbouring cell
            logging.debug(f"Shark {self.id} found a free cell")
            self.make_move(world, neighbours)

        # Increase hunger because no fish has been found
        self.hunger += 1

        # Increase age
        self.age += 1

        # Die if hunger is too high
        if self.hunger >= self.max_hunger:
            logging.debug(f"Shark {self.id} died of hunger")
            world[self.x][self.y] = Plankton(self.x, self.y)