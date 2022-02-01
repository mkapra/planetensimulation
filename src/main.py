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


if __name__ == "__main__":
