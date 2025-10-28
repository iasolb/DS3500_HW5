"""

alife.py: An animated Artificial Life Simulation

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


SIZE = 500  # The dimensions of the field
OFFSPRING = 2  # Max offspring when a rabbit reproduces
GRASS_RATE = 0.025  # Probability that grass grows back at any location in the next season.


class Rabbit:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self):
        pass

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        pass

    def eat(self, amount):
        """ Feed the rabbit some grass """
        pass

    def move(self):
        """ Move up, down, left, right randomly """
        pass


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around
    in search of grass """

    def __init__(self):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no rabbits """
        pass

    def add_rabbit(self, rabbit):
        """ A new rabbit is added to the field """
        pass

    def move(self):
        """ Rabbits move """
        pass

    def eat(self):
        """ Rabbits eat (if they find grass where they are) """
        pass

    def survive(self):
        """ Rabbits who eat some grass live to eat another day """
        pass

    def reproduce(self):
        """ Rabbits reproduce like rabbits. """
        pass

    def grow(self):
        """ Grass grows back with some probability """
        pass

    def generation(self):
        """ Run one generation of rabbits """
        pass


def main():

    # Create a field
    field = Field()

    # Then God created rabbits....

    # Animate the world!


if __name__ == '__main__':
    main()
