import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

# =========== Constants  ============
ARRSIZE = 200
FIGSIZE = 8
INIT_RABBITS = 100000
INIT_FOXES = 100
GRASS_RATE = 0.01
OFFSPRING = 4
NUM_GENERATIONS = 1000
"""
COLOR_MAP = {
0: Black (Nothing at that location), 
1: Green (Grass but no animals), 
2: White (Rabbit – but no foxes), 
3: Red (Fox)}
"""
# =========== Animal Section ============


class Animal:
    def __init__(self):
        self.max_offspring = 1
        self.starvation_level = 5
        self.reproduction_level = 1
        self.hunger = 0
        self.alive = True
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)

    def reproduce(self):
        """"""
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, amount: int):
        """"""
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
        self.foxes = []
        self.ate = []

    def add_rabbit(self, rabbit: object):
        """A new rabbit is added to the field"""
        self.rabbits.append(rabbit)

    def add_fox(self, fox: object):
        """Add new fox to the field"""
        self.foxes.append(fox)

    def move(self):
        """Rabbits move"""
        for rabbit in self.rabbits:
            rabbit.move()
        for fox in self.foxes:
            fox.move()

    # def _get_eaten(self, rabbit):
    #     self.rabbits.remove(rabbit)

    def eat(self):
        """Rabbits eat (if they find grass where they are)"""
        for rabbit in self.rabbits:
            grass_amount = self.field[rabbit.x, rabbit.y]
            rabbit.eat(grass_amount)
            self.field[rabbit.x, rabbit.y] = 0  # Grass is eaten, set to 0
            self.ate.append(rabbit)
        for fox in self.foxes:
            for rabbit in self.rabbits:
                if fox.x == rabbit.x & fox.y == rabbit.y:
                    rabbit_to_eat = rabbit
                    self.rabbits.remove(rabbit_to_eat)
                    self.ate.append(fox)

    def survive(self):
        """Rabbits who eat some grass live to eat another day"""
        self.rabbits = [r for r in self.rabbits if r.hunger >= r.starvation_level]
        self.foxes = [f for f in self.foxes if f.hunger >= f.starvation_level]

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
    plt.title(
        f"Generation: {i}, Nrabbits: {len(field.rabbits)}, Nfoxes: {len(field.foxes)}"
    )
    return (im,)


def main():
    # Create a field
    field = Field()

    # Then God created rabbits....
    for _ in range(INIT_RABBITS):
        new_rabbit = Animal()
        field.add_rabbit(new_rabbit)

    print(f"added {len(field.rabbits)} rabbits to the figure")
    for _ in range(INIT_FOXES):
        new_fox = Animal()
        field.add_fox(new_fox)
    print(f"added {len(field.foxes)} foxes to the figure")

    fig, ax = plt.subplots(figsize=(FIGSIZE, FIGSIZE))
    cmap = plt.cm.colors.ListedColormap(["black", "green", "white", "red"])
    img = ax.imshow(field.field, cmap=cmap, vmin=0, vmax=3)

    def update(frame):
        field.generation()
        display = field.field.copy()

        for r in field.rabbits:
            if r.alive:
                display[r.y, r.x] = 2
        for f in field.foxes:
            if f.alive:
                display[f.y, f.x] = 3

        img.set_data(display)
        ax.set_title(
            f"Generation {frame} | Rabbits: {len(field.rabbits)} Foxes: {len(field.foxes)}"
        )
        return [img]

    ani = animation.FuncAnimation(
        fig, update, frames=NUM_GENERATIONS, interval=200, blit=True
    )
    plt.show()


if __name__ == "__main__":
    main()
