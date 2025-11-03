import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

# =========== Constants  ============
ARRSIZE = 200
FIGSIZE = 8
INIT_RABBITS = 1000
GRASS_RATE = 0.99
OFFSPRING = 2
"""
COLOR_MAP = {
0: Black (Nothing at that location), 
1: Green (Grass but no animals), 
2: White (Rabbit – but no foxes), 
3: Red (Fox)}
"""
# =========== Animal Section ============


class Animal:
    def __init__(self, type: str):
        self.max_hunger = 1
        self.starvation_level = 1
        self.reproduction_level = 1
        self.hunger = 0
        self.alive = True

    def reproduce(self):
        """animal reproduction"""
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount: int):
        """Feed the rabbit some grass"""
        self.eaten += amount

    def move(self):
        """Move up, down, left, right randomly"""
        self.x = (
            self.x + rnd.choice([-1, 0, 1])
        ) % ARRSIZE  # 0 <= x <= 199 because 200 % 200 == 0 - wraps the bunnies around if they walk off the screen
        self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE
        self.eaten = 0


# =========== Field Section ============
class Field:
    """A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass"""

    def __init__(self):
        """Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits"""
        self.field = np.ones((ARRSIZE, ARRSIZE))
        self.rabbits = []
        pass

    def add_rabbit(self, rabbit: object):
        """A new rabbit is added to the field"""
        self.rabbits.append(rabbit)

    def move(self):
        """Rabbits move"""
        for rabbit in self.rabbits:
            rabbit.move()

    def eat(self):
        """Rabbits eat (if they find grass where they are)"""
        for rabbit in self.rabbits:
            grass_amount = self.field[rabbit.x, rabbit.y]
            rabbit.eat(grass_amount)
            self.field[rabbit.x, rabbit.y] = 0  # Grass is eaten, set to 0

    def survive(self):
        """Rabbits who eat some grass live to eat another day"""
        self.rabbits = [r for r in self.rabbits if r.eaten > 0]

    def reproduce(self):
        """Rabbits reproduce like rabbits."""
        born = []
        for r in self.rabbits:
            for _ in range(rnd.randint(0, OFFSPRING)):
                born.append(r.reproduce())
        self.rabbits.extend(born)

    def grow(self):
        """Grass grows back with some probability"""
        growloc = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)
        pass

    def generation(self):
        """Run one generation of rabbits"""
        self.move()
        self.eat()
        self.grow()
        self.reproduce()
        self.survive()  # Check survival from LAST generation


def main():
    pass


if __name__ == "__main__":
    main()
