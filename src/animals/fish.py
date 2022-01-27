from tkinter import ttk
from animals.animal import Animal


class Fish(Animal):

    breed_age = 1
    color = 'green'
    id = 0

    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
        self.id = Fish.id
        Fish.id = Fish.id + 1

    def __repr__(self):
        return f"F{self.age}"
