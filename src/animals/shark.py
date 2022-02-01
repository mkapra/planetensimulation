from animals.animal import Animal
from animals.plankton import Plankton
from animals.fish import Fish

import random
import logging


class Shark(Animal):

    color = 'red'
    breed_age = 8
    max_hunger = 5
    id = 0

    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
        self.hunger = 0
        self.id = Shark.id
        Shark.id = Shark.id + 1

    def __repr__(self):
        return f"S{self.age}"

    def is_fish(self, x, y, world):
        return type(world[x][y]) == Fish

    def is_empty(self, x, y, world):
        return type(world[x][y]) == Plankton

    def get_fish_neighbours(self, x, y, x_size, y_size, world):
        neighbours = []

        # Check if cell above is free
        if self.is_fish((x) % x_size, (y-1) % y_size, world):
            neighbours.append(world[(x) % x_size][(y-1) % y_size])
        # Check if cell below is free
        if self.is_fish((x) % x_size, (y+1) % y_size, world):
            neighbours.append(world[(x) % x_size][(y+1) % y_size])
        # Check if cell left is free
        if self.is_fish((x-1) % x_size, (y) % y_size, world):
            neighbours.append(world[(x-1) % x_size][(y) % y_size])
        # Check if cell right is free
        if self.is_fish((x+1) % x_size, (y) % y_size, world):
            neighbours.append(world[(x+1) % x_size][(y) % y_size])
        return neighbours

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

    def tick(self, world, x_size, y_size):
        # Look for fish in neighbouring cells
        neighbours = self.get_fish_neighbours(self.x, self.y, x_size, y_size, world)
        if len(neighbours) > 0:
            # Found a fish in a neighbouring cell
            logging.debug(f"Shark {self.id} found a fish")
            self.make_move(world, neighbours)
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