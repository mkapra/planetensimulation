from . import *

class Plankton(Field):

    color = 'blue'

    def __init__(self, x, y):
        super().__init__(x, y, self.color)

    def __repr__(self) -> str:
        return "__"