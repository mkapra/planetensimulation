#!/usr/bin/python3
import random
from animals import Animal, Fish, Shark


class Container(dict):

    def __init__(self, *args, **kwargs):
        """
        Initialize a new game field
        :param x: Amount of columns in the game field
        :param y: Amount of rows in the game field
        :param amount_fish: Amount of fishes at the start of the simulation
        :param amount_sharks:
        """
        super(Container, self).__init__(*args, **kwargs)

    def __missing__(self, *args, **kwargs):
        """An empty cell returns value zero.

        This is what lets us store a huge board and ignore dead cells.
        An Array based implementation would be very space intensive and
        expensive to iterate over."""
        return 0


class Statistics:
    """
    Class to keep statistics about the simulation
    """

    TOTAL_FISH = 'fishTotal'
    TOTAL_SHARK = 'sharkTotal'
    NEW_FISH = 'fishNew'
    NEW_SHARK = 'sharkNew'
    DIED_FISH = 'fishDied'
    DIED_SHARK = 'sharkDied'
    ALL_KEYS = {TOTAL_FISH, TOTAL_SHARK, NEW_FISH, NEW_SHARK, DIED_FISH, DIED_SHARK}

    def __init__(self):
        self._stats: dict[str, list[int]] = dict()
        self.reset()

    def reset(self):
        self._stats.clear()
        for key in self.ALL_KEYS:
            self._stats[key] = []
        self.add_cycle()

    def get_stats(self):
        return self._stats

    def add_cycle(self):
        for _, item in self._stats.items():
            item.append(0)

    def update_total(self, fish_total: int, shark_total: int):
        self._stats.get(self.TOTAL_FISH)[-1] = fish_total
        self._stats.get(self.TOTAL_SHARK)[-1] = shark_total

    def update_from_stats(self, stats: dict[str, list[int]]):
        for key, item in stats.items():
            self._stats.get(key).extend(stats.get(key))

    def shark_died(self):
        self._stats.get(self.DIED_SHARK)[-1] += 1

    def shark_born(self):
        self._stats.get(self.NEW_SHARK)[-1] += 1

    def fish_died(self):
        self._stats.get(self.DIED_FISH)[-1] += 1

    def fish_born(self):
        self._stats.get(self.NEW_FISH)[-1] += 1


class Simulation:

    def __init__(self, x: int, y: int, amount_fish: int, amount_sharks: int):
        """
        Initialize a new simulation
        :param x: Amount of columns in the simulation
        :param y: Amount of rows in the simulation
        :param amount_fish: Amount of fishes at the start of the simulation
        :param amount_sharks: Amount of sharks at the start of the simulation
        """

        if x < 2 or y < 2:
            raise Exception("The size of the simulation has to be at least 2!")
        if amount_fish == 0 or amount_sharks == 0:
            raise Exception("The simulations need at least one fish and shark!")

        self.size_x = x
        self.size_y = y
        self._fishes = Container()
        self._sharks = Container()
        self._stats = Statistics()
        self._random_init(amount_fish, amount_sharks)

    def _random_init(self, amount_fish: int, amount_sharks: int):
        """
        Initialize this simulation with a given amount of fishes and sharks
        :param amount_fish: Amount of fishes
        :param amount_sharks: Amount of sharks
        """

        self._fishes.clear()
        self._sharks.clear()

        while len(self._fishes) < amount_fish:
            new_pos = self.random_pos()
            if new_pos not in self.get_all_positions():
                self._fishes[new_pos] = Fish()

        while len(self._sharks) < amount_sharks:
            new_pos = self.random_pos()
            if new_pos not in self.get_all_positions():
                self._sharks[new_pos] = Shark()

        # Add initialized fishes and sharks to statistics
        self._stats.update_total(len(self._fishes), len(self._sharks))

    def random_pos(self):
        ran_x = random.randint(0, self.size_x - 1)
        ran_y = random.randint(0, self.size_y - 1)
        return ran_x, ran_y

    def get_all_positions(self):
        """
        Getter for all already taken positions
        :return:
        """
        all_positions = set(self._fishes.keys())
        all_positions.update(set(self._sharks.keys()))
        return all_positions

    def get_unified_dict(self):
        complete_dict = dict()
        complete_dict.update(self._fishes)
        complete_dict.update(self._sharks)
        return complete_dict

    def _get_free_neighbour_space(self, pos: tuple):
        """
        Gets all free places around a specified coordinate
        :param self:
        :param pos: A tuple with the position of the specified coordinates
        :return: A Set of free positions nearby the specified coordinates
        """
        x = pos[0]
        y = pos[1]
        neighbours = set()
        animal_type = self._fishes[(x, y)]
        if animal_type == 0:
            animal_type = self._sharks[(x, y)]

        coordinates = [self._translate_pos(self, (x - 1, y)),
                       self._translate_pos(self, (x + 1, y)),
                       self._translate_pos(self, (x, y - 1)),
                       self._translate_pos(self, (x, y + 1))]

        for coordinate in coordinates:
            if coordinate not in self._sharks.keys() and \
                    (isinstance(animal_type, Shark) or coordinate not in self._fishes.keys()):
                neighbours.add(coordinate)

        return neighbours

    @staticmethod
    def _translate_pos(self, pos: tuple):
        return pos[0] % self.size_x, pos[1] % self.size_y

    def move_creatures(self):
        """
        Moves all the creatures in the simulations and kills creatures if necessary
        """

        # Skip task if there are no more sharks
        if len(self._sharks) == 0:
            return

        self._stats.add_cycle()
        self.move_fishes()
        self.move_sharks()
        self._stats.update_total(len(self._fishes), len(self._sharks))

    def move_fishes(self):
        pos_fishes = set(self._fishes.keys())
        # Update fishes in the simulation
        for position in pos_fishes:
            self._fishes.get(position).lives()

            movable = self._get_free_neighbour_space(position)
            if len(movable) > 0:
                # Move the current fish
                new_pos = random.choice(list(movable))
                self._fishes[new_pos] = self._fishes.pop(position)

                # Breed new fish if possible
                if self._fishes[new_pos].can_breed():
                    self._fishes[position] = Fish()
                    self._stats.fish_born()

    def move_sharks(self):
        # update sharks in the simulation
        pos_sharks = set(self._sharks.keys())
        for position in pos_sharks:
            # Kill shark if it has too much hunger
            if not self._sharks[position].lives():
                self._sharks.pop(position)
                self._stats.shark_died()
                break

            movable = self._get_free_neighbour_space(position)
            if len(movable) > 0:
                # Move the current shark
                new_pos = random.choice(list(movable))
                self._sharks[new_pos] = self._sharks.pop(position)

                # Eat fish if the new position was a fish
                if new_pos in self._fishes.keys():
                    self._fishes.pop(new_pos)
                    self._sharks[new_pos].eats()
                    self._stats.fish_died()

                # Breed new shark if possible
                if self._sharks[new_pos].can_breed():
                    self._sharks[position] = Shark()
                    self._stats.shark_born()

    def run(self, amount: int):
        for i in range(amount):
            self.move_creatures()
        return self._stats.get_stats()


if __name__ == "__main__":
    print("Planetensimulation is starting...")
    sim = Simulation(10, 10, 60, 20)
    print(sim.run(10))
