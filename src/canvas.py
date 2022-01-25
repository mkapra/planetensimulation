import numpy as numpy


class Canvas:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.world = numpy.zeros((self.x, self.y), dtype=int)

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
