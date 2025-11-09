"""
Created on 11/5/25
@Author: Amir Sesay

Description: HW 5 - ecosystem simulation of foxes and rabbits
"""

import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import matplotlib
matplotlib.use('TkAgg')

# ------ SIMULATION PARAMETERS -----
ARRSIZE = 25
FIGSIZE = 8
INIT_RABBITS = 100
INIT_FOXES = 15
GRASS_RATE = 0.03
OFFSPRING = 2
# ---------------------------------


class Animal:
    '''Animal class that tracks the species, position, hunger level,
    reproduction levels, and overall survival'''
    def __init__(self, species="rabbit", max_offspring=1, starvation_level=1, reproduction_level=1):
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)
        self.eaten = 0
        self.hunger = 0
        self.alive = True
        self.species = species
        self.max_offspring = max_offspring
        self.starvation_level = starvation_level
        self.reproduction_level = reproduction_level


    def move(self):
       '''Randomly moves the animal in any direction'''
       self.x = (self.x + rnd.choice([-1, 0, 1])) % ARRSIZE
       self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE

    def eat(self, amount):
        if amount > 0:
            self.eaten += amount
            self.hunger = 0

    def reproduce(self):
        if self.eaten >= self.reproduction_level:
            self.eaten = 0
            return copy.deepcopy(self)
        return None


class Field:
    """ A field is a patch of grass with 0 or more rabbits hopping around """
    def __init__(self):
        self.field = np.ones((ARRSIZE, ARRSIZE), dtype=int)
        self.animals = (
                [Animal("rabbit", max_offspring=2, starvation_level=5, reproduction_level=1)
                 for _ in range(INIT_RABBITS)] +
                [Animal("fox", max_offspring=1, starvation_level=12, reproduction_level=2)
                 for _ in range(INIT_FOXES)])

    def move(self):
        """Randomly moves animals"""
        for animal in self.animals:
            if animal.alive:
                animal.move()

    def eat(self):
        """Animal eats based on their species """
        #  location mapping for rabbits
        rabbit_locations = {}
        for animal in self.animals:
            if animal.alive and animal.species == "rabbit":
                pos = (animal.x, animal.y)
                if pos not in rabbit_locations:
                    rabbit_locations[pos] = []
                rabbit_locations[pos].append(animal)

        # feeding the animals
        for animal in self.animals:
            if not animal.alive:
                continue
            # rabbit eats food (grass)
            if animal.species == "rabbit":
                grass_amount = self.field[animal.x, animal.y]
                animal.eat(grass_amount)
                if grass_amount > 0:
                    self.field[animal.x, animal.y] = 0
            # fox eats food (rabbit) and accounts for a death
            elif animal.species == "fox":
                pos = (animal.x, animal.y)
                if pos in rabbit_locations:
                    rabbits_here = rabbit_locations[pos]
                    for rabbit in rabbits_here:
                        rabbit.alive = False
                    animal.eat(len(rabbits_here))

    def survive(self):
        """Updates hunger level and removes dead animals """
        surviving_animals = []
        for animal in self.animals:
            if animal.alive:
                if animal.eaten == 0:
                    animal.hunger += 1
                if animal.hunger >= animal.starvation_level:
                    animal.alive = False
                else:
                    surviving_animals.append(animal)
        self.animals = surviving_animals

    def grow(self):
        """ Grass grows back with some probability at each location """
        growloc = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def reproduce(self):
        """Animals reproduce and is counted"""
        born = []
        for animal in self.animals:
            if animal.alive:
                for _ in range(rnd.randint(0, animal.max_offspring)):
                    offspring = animal.reproduce()
                    if offspring:
                        born.append(offspring)
        self.animals += born

    def get_display_field(self):
        display_field = self.field.copy()
        # add animals to display
        for animal in self.animals:
            if animal.alive:
                if animal.species == "rabbit":
                    if display_field[animal.x, animal.y] != 3:
                        display_field[animal.x, animal.y] = 2
                elif animal.species == "fox":
                    display_field[animal.x, animal.y] = 3
        return display_field

    def generation(self):
        """ One generation of animals """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

def count_species(animals):
    rabbits = sum(1 for a in animals if a.alive and a.species == "rabbit")
    foxes = sum(1 for a in animals if a.alive and a.species == "fox")
    return rabbits, foxes

def animate(i, field, im):
    field.generation()
    display_field = field.get_display_field()
    im.set_array(display_field)
    # count animals
    rabbits, foxes = count_species(field.animals)
    plt.title(f"Generation: {i} | Rabbits: {rabbits} | Foxes: {foxes}")
    return im,


def time_series():
    """Time Series plot of rabbit and fox life over time"""
    field = Field()
    rabbit_data = []
    fox_data = []

    for i in range(500):
        field.generation()
        rabbits, foxes = count_species(field.animals)
        rabbit_data.append(rabbits)
        fox_data.append(foxes)
    # plot
    plt.figure(figsize=(10, 6))
    plt.plot(rabbit_data, label='Rabbits', color='blue')
    plt.plot(fox_data, label='Foxes', color='red')
    plt.xlabel('Generation')
    plt.ylabel('Population')
    plt.title('Rabbit and Fox Population Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main(run_time_series=True):
        if run_time_series:
            time_series()
        else:
            field = Field()
            fig = plt.figure(figsize=(FIGSIZE, FIGSIZE))
            colors = ['black', 'green', 'white', 'red']
            custom_cmap = ListedColormap(colors)
            display_field = field.get_display_field()
            im = plt.imshow(display_field, cmap=custom_cmap, interpolation='nearest', vmin=0, vmax=3)

            anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=100, interval=500, repeat=False)
            plt.show()
            return anim
if __name__ == '__main__':
    main()