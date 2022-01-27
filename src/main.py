#!/usr/bin/python3
import random
from re import I

from canvas2 import *
from animals.animal import Animal
from animals.fish import Fish
from animals.shark import Shark
from animals.plankton import Plankton

# Procedure:
# 1. Create a world
# 2. Create a population of animals
# 3. Start the simulation



class Game():
    def __init__(self):
        self.x_size: int = 40
        self.y_size: int = 40

        self.shark_count: int = 40
        self.fish_count: int = 70

        self.world: list[list[Animal]] = []
        self.moved_ids: list[int] = []

        for x in range(self.x_size):
            self.world.append([])
            for y in range(self.y_size):
                self.world[x].append(Plankton(x, y))

    def print_world(self, _world):
        for row in _world:
            print(row)

    def get_empty_neighbours(self, animal):
        neighbours = []

        x = animal.x
        y = animal.y

        if self.is_empty((x) % self.x_size, (y-1) % self.y_size):
            neighbours.append(self.world[(x) % self.x_size][(y-1) % self.y_size])
        if self.is_empty((x) % self.x_size, (y+1) % self.y_size):
            neighbours.append(self.world[(x) % self.x_size][(y+1) % self.y_size])
        if self.is_empty((x-1) % self.x_size, (y) % self.y_size):
            neighbours.append(self.world[(x-1) % self.x_size][(y) % self.y_size])
        if self.is_empty((x+1) % self.x_size, (y) % self.y_size):
            neighbours.append(self.world[(x+1) % self.x_size][(y) % self.y_size])

        return neighbours

    def get_fish_neighbours(self, animal):
        neighbours = []

        x = animal.x
        y = animal.y

        if self.is_fish((x) % self.x_size, (y-1) % self.y_size):
            neighbours.append(self.world[(x) % self.x_size][(y-1) % self.y_size])
        if self.is_fish((x) % self.x_size, (y+1) % self.y_size):
            neighbours.append(self.world[(x) % self.x_size][(y+1) % self.y_size])
        if self.is_fish((x-1) % self.x_size, (y) % self.y_size):
            neighbours.append(self.world[(x-1) % self.x_size][(y) % self.y_size])
        if self.is_fish((x+1) % self.x_size, (y) % self.y_size):
            neighbours.append(self.world[(x+1) % self.x_size][(y) % self.y_size])

        return neighbours


    def is_empty(self, x, y):
        return type(self.world[x][y]) is Plankton

    def move_animal(self, animal, neighbour):
        # 7 - If moved, and the age is greater than the breeding age, reproduce
        # print("Animal moved from ({}, {}) to ({}, {})".format(animal.x, animal.y, neighbour.x, neighbour.y))
        if animal.age > animal.breed_age:
            # Leave child in old position
            newAnimal = None
            if type(animal) is Fish:
                print('Fish reproduced')
                newAnimal = Fish(animal.x, animal.y, 0)
                self.fishNew += 1
            elif type(animal) is Shark:
                print('Shark reproduced')
                newAnimal = Shark(animal.x, animal.y, 0)
                self.sharkNew += 1

            self.world[animal.x][animal.y] = newAnimal
            self.moved_ids.append(newAnimal.id)
            animal.age = -1
        else:
            # Leave Plankton in old position
            self.world[animal.x][animal.y] = Plankton(animal.x, animal.y)
        self.world[neighbour.x][neighbour.y] = animal
        animal.x = neighbour.x
        animal.y = neighbour.y

    def is_fish(self, x, y):
        return type(self.world[x][y]) is Fish

    # 7 If moved, and the age is greater than the breeding age, reproduce
    # 8 Increase the age
    # 9 Loop over all sharks
    # 10 Look for fish in neighbouring cells
    # 11 If there are fish, eat one
    # 12 If there are no fish, look for free neighbouring cells
    # 13 If there are free neighbouring cells, move to one of them
    # 14 If moved, and the age is greater than the breeding age, reproduce
    # 15 Increase the age
    # 16 If the age is greater than the maximum age, die
    def tick(self):
        self.fishTotal = 0
        self.fishNew = 0
        self.fishDied = 0
        self.sharkTotal = 0
        self.sharkNew = 0
        self.sharkDied = 0

        print("tick")
        # 4 - Loop over all fish
        for row in self.world:
            for animal in row:
                if type(animal) is Fish:
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)
                    # 5 - Look for free neighbouring cells
                    neighbours = self.get_empty_neighbours(animal)
                    # 6 - If there are free neighbouring cells, move to one of them
                    if len(neighbours) > 0:
                        # 6.1 - Choose a random neighbour
                        neighbour = random.choice(neighbours)
                        # 6.2 - Move to the neighbour
                        self.move_animal(animal, neighbour)
                    # 8 - Increase the age
                    animal.age += 1
        self.moved_ids.clear()

        # 9 - Loop over all sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Shark:
                    if animal.id in self.moved_ids:
                        continue
                    self.moved_ids.append(animal.id)
                    # 10 - Look for fish in neighbouring cells
                    neighbours = self.get_fish_neighbours(animal)
                    # 11 - If there are fish, eat one
                    if len(neighbours) > 0:
                        print("Shark eats fish")
                        # 11.1 - Choose a random neighbour
                        neighbour = random.choice(neighbours)
                        # 11.2 - Eat the fish
                        self.fishDied += 1
                        # 11.3 - Move to the neighbour
                        self.move_animal(animal, neighbour)
                        # 11.3 - Reset the shark's hunger
                        animal.days_without_food = 0
                    # 12 - If there are no fish, look for free neighbouring cells
                    else:
                        print("Shark has no fish")
                        # 12.1 - Look for free neighbouring cells
                        neighbours = self.get_empty_neighbours(animal)
                        # 12.2 - If there are free neighbouring cells, move to one of them
                        if len(neighbours) > 0:
                            # 12.2.1 - Choose a random neighbour
                            neighbour = random.choice(neighbours)
                            # 12.2.2 - Move to the neighbour
                            self.move_animal(animal, neighbour)
                        # 13 - Increase the shark's hunger
                        animal.days_without_food += 1
                    # 14 - Increase the age
                    animal.age += 1
                    # 14 - If the shark's hunger is greater than the maximum hunger, die
                    if animal.days_without_food > Shark.max_days_without_food:
                        print("Shark died")
                        self.sharkDied += 1
                        self.world[animal.x][animal.y] = Plankton(animal.x, animal.y)
        self.moved_ids.clear()

        # Loop world to count fish and sharks
        for row in self.world:
            for animal in row:
                if type(animal) is Fish:
                    self.fishTotal += 1
                elif type(animal) is Shark:
                    self.sharkTotal += 1

        # self.print_world(self.world)

        # 15 - Update the world
        for row in self.world:
            for animal in row:
                self.app.update_animal(animal.x, animal.y, animal.color)

        return {
            'fishTotal': self.fishTotal,
            'fishNew': self.fishNew,
            'fishDied': self.fishDied,
            'sharkTotal': self.sharkTotal,
            'sharkNew': self.sharkNew,
            'sharkDied': self.sharkDied
        }

    def run(self):
        print("Planetensimulation")

        sharks_placed: int = 0
        fishes_placed: int = 0

        while sharks_placed < self.shark_count:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Shark(x, y, random.randint(0, Shark.breed_age))
                sharks_placed += 1

        while fishes_placed < self.fish_count:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - 1)
            if type(self.world[x][y]) is Plankton:
                self.world[x][y] = Fish(x, y, random.randint(0, Fish.breed_age))
                fishes_placed += 1
        
        self.print_world(self.world)

        root = tk.Tk()
        self.app = App(self, self.x_size, self.y_size, self.world, root)
        self.app.pack()
        root.mainloop()


if __name__ == "__main__":
    Game().run()