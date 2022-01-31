from animals.animal import Animal

class Plankton(Animal):

    color = 'blue'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "__"