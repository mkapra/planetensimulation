from . import *

class Animal(Field):

    def __init__(self, x, y, color, breed_age, id, age):
        self.x = x
        self.y = y
        self.color = color
        self.breed_age = breed_age
        self.age = age
        self.id = id

    def __repr__(self) -> str:
        return f"{type(self).__name__[0]}{self.age}"

    # Check if neighbouring cells are free
    def get_free_neighbours(self, x, y, x_size, y_size, world):
        neighbours = []

        # Check cell above
        if self.is_empty(world[(x) % x_size][(y-1) % y_size]):
            neighbours.append(world[(x) % x_size][(y-1) % y_size])
        # Check cell below
        if self.is_empty(world[(x) % x_size][(y+1) % y_size]):
            neighbours.append(world[(x) % x_size][(y+1) % y_size])
        # Check cell left
        if self.is_empty(world[(x-1) % x_size][(y) % y_size]):
            neighbours.append(world[(x-1) % x_size][(y) % y_size])
        # Check cell right
        if self.is_empty(world[(x+1) % x_size][(y) % y_size]):
            neighbours.append(world[(x+1) % x_size][(y) % y_size])

        return neighbours

    # Check if the cell is free
    def is_empty(self, animal):
        return type(animal) == Plankton

    def make_move(self, world, neighbours):
        pass

    def tick(self, world, x_size, y_size):
        pass