class Animal:

    color = None
    breedAge = None

    def __init__(self):
        pass

    # Check if neighbouring cells are free
    def get_free_neighbours(self, x, y, x_size, y_size, world):
        neighbours = []

        # Check cell above
        if self.is_empty((x) % x_size, (y-1) % y_size, world):
            neighbours.append(world[(x) % x_size][(y-1) % y_size])
        # Check cell below
        if self.is_empty((x) % x_size, (y+1) % y_size, world):
            neighbours.append(world[(x) % x_size][(y+1) % y_size])
        # Check cell left
        if self.is_empty((x-1) % x_size, (y) % y_size, world):
            neighbours.append(world[(x-1) % x_size][(y) % y_size])
        # Check cell right
        if self.is_empty((x+1) % x_size, (y) % y_size, world):
            neighbours.append(world[(x+1) % x_size][(y) % y_size])

        return neighbours

    def is_empty(self, x, y, world):
       pass
