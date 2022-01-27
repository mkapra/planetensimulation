from tkinter import ttk
from animals.animal import Animal


class Shark(Animal):

    breed_age = 1
    max_days_without_food = 1
    color = 'red'
    id = 0

    def __init__(self, x, y, age):
        self.x = x
        self.y = y
        self.age = age
        self.days_without_food = 0
        self.id = Shark.id
        Shark.id = Shark.id + 1

    def __repr__(self):
        return f"S{self.age}"

