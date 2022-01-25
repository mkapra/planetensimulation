from tkinter import ttk
from animals.animal import Animal


class Fish(Animal):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Fish"

    @staticmethod
    def color():
        return 'green'
