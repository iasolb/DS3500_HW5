"""

alife_A_static.py: An animated Artificial Life Simulation

Completely static,
no rabbit repoduction
no starvation
population state will be fixed


Key concepts:
- Modeling and simulation as a way of understanding complex systems
- Artificial Life: Life as it could be
- Numpy array processing!
- Animation using the matplotlib.animation library

Key life lesson: Let curiosity be your guide.

"""

import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

# import seaborn   # conda install seaborn


ARRSIZE = 200  # The dimensions of the field
FIGSIZE = 8  # 8x8 image rendering
INIT_RABBITS = 1000  # num initial rabbits - static, none will be added
GRASS_RATE = 0.99
OFFSPRING = 2  # max number of baby rabbits per litter


class Rabbit:
    """A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve."""

    def __init__(self):
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)
        self.eaten = 0  # this rabbit is hungry (represents how many blades of grass the rabbit ate)

    def reproduce(self):
        """Make a new rabbit at the same location.
        Reproduction is hard work! Each reproducing
        rabbit's eaten level is reset to zero."""
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount):
        """Feed the rabbit some grass"""
        self.eaten += amount

    def move(self):
        """Move up, down, left, right randomly"""
        self.x = (
            self.x + rnd.choice([-1, 0, 1])
        ) % ARRSIZE  # 0 <= x <= 199 because 200 % 200 == 0 - wraps the bunnies around if they walk off the screen
        self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE
        self.eaten = 0


class Field:
    """A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass"""

    def __init__(self):
        """Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits"""
        self.field = np.ones((ARRSIZE, ARRSIZE))
        self.rabbits = []
        pass

    def add_rabbit(self, rabbit):
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


def animate(i, field, im):
    field.generation()
    # Mark rabbit positions on the field for display
    display_field = field.field.copy()
    for rabbit in field.rabbits:
        display_field[rabbit.x, rabbit.y] = 2
    im.set_array(display_field)  # Inject new field state into the img array
    plt.title(f"Generation: {i}, Nrabbits: {len(field.rabbits)}")
    return (im,)


def main():

    # Create a field
    field = Field()

    # Then God created rabbits....
    for _ in range(INIT_RABBITS):
        new_rabbit = Rabbit()  # Creating a single rabbit at a random location
        field.add_rabbit(new_rabbit)  # adding the rabbit to the field simulation

    # Animate the world!
    array = np.ones(shape=(ARRSIZE, ARRSIZE))
    fig = plt.figure(figsize=(FIGSIZE, FIGSIZE))
    im = plt.imshow(array, cmap="viridis", interpolation="hamming", vmin=0, vmax=1)
    anim = animation.FuncAnimation(
        fig, animate, fargs=(field, im), frames=10**100, interval=1
    )
    plt.show()


if __name__ == "__main__":
    main()
