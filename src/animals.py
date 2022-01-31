

class Animal:
    """
    Represents an animal
    """

    def __init__(self, id: int, color: str, breed_age: int):
        self.id = id
        self.color = color
        self.age = 0
        self.breed_age = breed_age

    def can_breed(self):
        if self.breed_age == self.age:
            self.age = 0
            return True
        return False

    def lives(self):
        self.age = self.age + 1
        return True


class Fish(Animal):
    """
    Represents a fish
    """

    def __init__(self, color='green', breed_age=5):
        super().__init__(1, color, breed_age)


class Shark(Animal):
    """
    Represents a shark
    """

    def __init__(self, color='red', breed_age=8, max_hunger: int = 5):
        self.hunger = 0
        self.max_hunger = max_hunger
        super().__init__(2, color, breed_age)

    def eats(self):
        self.hunger = 0

    def lives(self):
        super().lives()
        self.hunger = self.hunger + 1
        return self.hunger != self.max_hunger
