import random
from unittest import TestCase
from main import Game

class Test(TestCase):

    def test_optimum(self):
        sim = Game(40, 40, 200, 100, 3, 8, 5)
        sim.run()

    def test_unstable(self):
        sim = Game(40, 40, 200, 500, 3, 8, 5)
        sim.run()

    def test_unstable_size(self):
        sim = Game(4, 4, 2, 1, 3, 8, 5)
        sim.run()

    def test_unstable_too_much_sharks(self):
        sim = Game(40, 40, 200, 500, 3, 8, 5)
        sim.run()

    def test_unstable_no_enough_sharks(self):
        sim = Game(40, 40, 200, 5, 3, 8, 5)
        sim.run()

    def test_game(self):
        file = open('tested_parameter.csv', 'w')
        file.write("run, size, amount_fishes, amount_sharks, breed_time_fishes, breed_time_sharks, hunger_sharks")
        for run in range(10):
            size = random.randint(2,80)
            amount_fishes = random.randint(1, (size**2))
            amount_sharks = min(random.randint(1, (size**2)), size**2 - amount_fishes)
            breed_time_fishes = random.randint(1, 20)
            breed_time_sharks = random.randint(1, 20)
            hunger_sharks = random.randint(1, 20)
            sim = Game(size, size, amount_fishes, amount_sharks, breed_time_fishes, breed_time_sharks, hunger_sharks)
            file.write(f"{run}, {size}, {amount_fishes}, {amount_sharks}, {breed_time_fishes}, {breed_time_sharks},"
                       f"{hunger_sharks}\n")
            sim.run()
        file.close()
