from unittest import TestCase
from animals import Animal, Fish, Shark


class TestAnimals(TestCase):
    def setUp(self):
        self.fish = Fish()
        self.shark = Shark()

    # Fish tests
    def test_fish_lives(self):
        self.assertTrue(self.fish.lives())

    def test_fish_can_breed_false(self):
        self.assertFalse(self.fish.can_breed())

    def test_fish_can_breed_true(self):
        for index in range(self.fish.breed_age - 1):
            self.fish.lives()
        self.assertFalse(self.fish.can_breed())

    # Shark tests
    def test_shark_lives_true(self):
        self.assertTrue(self.shark.lives())

    def test_shark_lives_false(self):
        for index in range(self.shark.max_hunger - 1):
            self.shark.lives()
        self.assertFalse(self.shark.lives())

    def test_shark_can_breed_false_to_soon(self):
        self.assertFalse(self.shark.can_breed())

    def test_shark_can_breed_true(self):
        for index in range(self.shark.breed_age - 1):
            self.shark.eats()
            self.shark.lives()
        self.assertFalse(self.shark.can_breed())

    def test_shark_can_breed_false_dead(self):
        for index in range(self.shark.breed_age - 1):
            self.shark.eats()
            self.shark.lives()
        self.assertFalse(self.shark.can_breed())
