import random
from unittest import TestCase
from main import Container, Statistics, Simulation
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


class TestStatistics(TestCase):
    def setUp(self) -> None:
        self.stats = Statistics()
        self.update = Statistics()

    def test_init(self):
        self.assertIsInstance(self.stats, Statistics)

    def test_get_stats_empty(self):
        stats_dict = self.stats.get_stats()
        self.assertEqual(6, len(stats_dict))
        for item in stats_dict.values():
            self.assertEqual(0, item[0])

    def test_shark_born(self):
        self.stats.shark_born()
        self.assertEqual(1, self.stats.get_stats().get(self.stats.NEW_SHARK)[0])

    def test_shark_dies(self):
        self.stats.shark_died()
        self.assertEqual(1, self.stats.get_stats().get(self.stats.DIED_SHARK)[0])

    def test_fish_born(self):
        self.stats.fish_born()
        self.assertEqual(1, self.stats.get_stats().get(self.stats.NEW_FISH)[0])

    def test_fish_dies(self):
        self.stats.fish_died()
        self.assertEqual(1, self.stats.get_stats().get(self.stats.DIED_FISH)[0])

    def test_stats_empty_reset(self):
        self.stats.reset()
        stats_dict = self.stats.get_stats()
        self.assertEqual(6, len(stats_dict))
        for item in stats_dict.values():
            self.assertEqual(0, item[0])

    def test_stats_get_stats(self):
        self.assertIsInstance(self.stats.get_stats(), dict)

    def test_stats_add_cycle(self):
        for i in range(10):
            ran = random.randint(0, 1000)
            for j in range(ran):
                self.stats.add_cycle()
            self.assertEqual(ran + 1, len(self.stats.get_stats().get(Statistics.TOTAL_SHARK)))
            self.stats.reset()

    def test_stats_update_total(self):
        for fishes, sharks in zip(range(random.randint(10, 1000)), range(random.randint(10, 1000))):
            self.stats.update_total(fishes, sharks)
            stats_dict = self.stats.get_stats()
            self.assertEqual(fishes, stats_dict[Statistics.TOTAL_FISH][0])
            self.assertEqual(sharks, stats_dict[Statistics.TOTAL_SHARK][0])

    def test_stats_update_from_stats_empty(self):
        self.stats.update_from_stats(self.update.get_stats())
        stats_dict = self.stats.get_stats()
        self.assertEqual(6, len(stats_dict))
        for item in stats_dict.values():
            self.assertEqual(0, item[0])

    def test_stats_update_from_stats(self):
        # create random stats in update
        length = random.randint(10, 1000)
        for cycles in range(length):
            for key in Statistics.ALL_KEYS:
                self.update._stats.get(key)[cycles] = random.randint(10, 1000)
            if cycles < length - 1:
                self.update.add_cycle()

        # update statistics from update to stats
        self.stats.update_from_stats(self.update.get_stats())
        stats_dict = self.stats.get_stats()
        for item in stats_dict.values():
            self.assertEqual(length + 1, len(item))

