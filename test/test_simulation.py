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


class TestSimulation(TestCase):
    def test_random_pos_loop(self):
        for i in range(2, 10):
            x = random.randint(0, 1000)
            y = random.randint(0, 1000)
            sim = Simulation(x, y, 2, 2)
            new_pos = sim.random_pos()
            self.assertIsInstance(new_pos, tuple)
            self.assertLess(new_pos[0], x)
            self.assertLess(new_pos[1], y)

    def test_init_simulation_not_none(self):
        new_sim = Simulation(20, 20, 10, 2)
        self.assertIsNotNone(new_sim)

    def test_init_simulation_raises_exception(self):
        with self.assertRaises(Exception):
            Simulation(0, 20, 10, 2)
        with self.assertRaises(Exception):
            Simulation(20, 0, 10, 2)
        with self.assertRaises(Exception):
            Simulation(20, 20, 0, 2)
        with self.assertRaises(Exception):
            Simulation(20, 20, 10, 0)

    def test_init_simulation_random_field(self):
        for i in range(4, 20):
            sim = Simulation(10, 10, i, i)
            self.assertEqual(2 * i, len(sim._fishes) + len(sim._sharks))

    def test_get_all_positions(self):
        for i in range(4, 20):
            sim = Simulation(10, 10, i, i)
            self.assertEqual(2 * i, len(sim.get_all_positions()))

    def test_get_unified_dict(self):
        for i in range(4, 20):
            sim = Simulation(10, 10, i, i)
            all_positions = sim.get_unified_dict()
            self.assertIsInstance(all_positions, dict)
            self.assertEqual(2 * i, len(all_positions))
            item = all_positions.popitem()
            self.assertIsInstance(item[0], tuple)
            self.assertIsInstance(item[1], Animal)

    def test_translate_position(self):
        x = 20
        y = 20
        sim = Simulation(x, y, x, x)

        for i in range(-x, x*2):
            for j in range(-y, y * 2):
                new_pos = sim._translate_pos(sim, (i, j))
                assertion = i % x, j % y
                self.assertIn(new_pos[0], range(0, x))
                self.assertIn(new_pos[1], range(0, y))
                self.assertEqual(assertion, new_pos)

    def test_get_free_neighbour_space(self):
        x = 10
        y = 10
        all_possible_positions = set()

        for i in range(0, x):
            for j in range(0, y):
                all_possible_positions.add((i, j))

        for amount in range(2, 20):
            sim = Simulation(x, y, amount, amount)
            all_taken_positions = sim.get_all_positions()

            # Create a set with all free positions in the simulation
            free_positions = set()
            free_positions.update(all_possible_positions)
            free_positions.difference_update(all_taken_positions)

            for free_pos in free_positions:
                self.assertNotIn(sim._get_free_neighbour_space(free_pos),
                                 all_taken_positions)
