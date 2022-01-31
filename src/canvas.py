import numpy as numpy


class Canvas(dict):
    """The Canvas is represents as a dictionary"""

    def __init__(self, *args, **kwargs):
        """Setting up out constructor."""
        super(Canvas, self).__init__(*args, **kwargs)
        self.world = numpy.zeros((self.x, self.y), dtype=int)

    def __missing__(self, *args, **kwargs):
        """An empty cell returns value zero.

        This is what lets us store a huge board and ignore dead cells.
        An Array based implementation would be very space intensive and
        expensive to iterate over."""
        return 0

    def update_animal(self, x: int, y:int):
        """Check in each tick the animal. Determine if the animal lives or dies.

        :return
        """


    def queue_animals(self):
        ainimals = []
        for x, y in self.keys():
            for


    def calculate_neighbours(self, xOff, yOff):
        neighbours = list()
        neighbours.append(((xOff + 1) % self.y, yOff)) #Rechter Nachbar
        neighbours.append(((xOff - 1) % self.y, yOff)) #Linker Nachbar
        neighbours.append((xOff, ((yOff + 1) % self.x)))
        neighbours.append((xOff, ((yOff - 1) % self.x)))
        return neighbours

    def get_position(self, to_get):
        return self.world[to_get[1], to_get[0]]

    def get_neighbours(self, location):
        neighbours = list()
        positions = self.calculate_neighbours(location[0], location[1])
        for position in positions:
            neighbours.append(self.get_position(position))
        return neighbours

    def update_field(self, pos, update_object):
        self.world[pos[1], pos[0]] = update_object


if __name__ == '__main__':
    can = Canvas(4, 5)
    print(can.get_neighbours((0, 0)))
