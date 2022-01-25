from tkinter import ttk
from animals.animal import Animal


class Shark(Animal):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Shark"

    @staticmethod
    def color():
        return 'red'
