import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

# =========== Constants ============

ARRSIZE = 100
FIGSIZE = 8
INIT_RABBITS = 100
INIT_FOXES = 100
GRASS_RATE = 0.08
OFFSPRING = 2
STARVATION_LEVEL = 2
REPRODUCTION_LEVEL = 1

# =========== Animal Section ============


class Animal:
    def __init__(self):
        self.max_offspring = OFFSPRING
        self.starvation_level = STARVATION_LEVEL
        self.reproduction_level = REPRODUCTION_LEVEL
        self.hunger = 0
        self.alive = True
        self.x = rnd.randrange(0, ARRSIZE)
        self.y = rnd.randrange(0, ARRSIZE)

    def reproduce(self, parent: object):
        """
        Reproduce only if hunger level is at or below reproduction_level.
        PDF Requirement: "Animals can only reproduce if the amount they have
        eaten is at least as high as the reproduction level."
        Interpretation: Low hunger = well-fed = can reproduce
        """
        if parent.hunger <= parent.reproduction_level:
            return [
                copy.deepcopy(parent) for i in range(rnd.randint(1, self.max_offspring))
            ]
        return []

    def eat(self, to_eat=None):
        """
        Reset hunger to 0 when eating. Kill eaten object
        PDF Requirement: "If the animal eats something, the hunger level is reset to zero."
        """
        self.hunger = 0
        if to_eat:
            if isinstance(to_eat, object):
                to_eat.alive = False

    def move(self):
        """Move up, down, left, right randomly"""
        self.x = (self.x + rnd.choice([-1, 0, 1])) % ARRSIZE
        self.y = (self.y + rnd.choice([-1, 0, 1])) % ARRSIZE


# =========== Field Section ============


class Field:
    def __init__(self):
        self.field = np.ones((ARRSIZE, ARRSIZE))
        self.rabbits = []
        self.foxes = []

        # Time series tracking
        self.rabbit_history = []
        self.fox_history = []
        self.generation_count = 0

    def add_rabbit(self, rabbit: object):
        self.rabbits.append(rabbit)

    def add_fox(self, fox: object):
        self.foxes.append(fox)

    def move_animals(self):
        for r in self.rabbits:
            if r.alive:
                r.move()
        for f in self.foxes:
            if f.alive:
                f.move()

    def eat(self):
        """
        Handle eating for both rabbits and foxes.
        PDF Requirement: "When an animal goes a generation without eating,
        its hunger level increases by one."

        Uses location mapping for efficient fox feeding as per PDF:
        "If you otherwise try to scan through the list of rabbits looking
        for a location match, your code will run very slowly!"
        """
        # find all rabbits
        rabbit_locations = {}  # tuple position: list of rabbits there
        for r in self.rabbits:
            if r.alive:
                pos = (r.x, r.y)
                if pos not in rabbit_locations:
                    rabbit_locations[pos] = []
                rabbit_locations[pos].append(r)

        # run checks for grass (rabbit eat grass)
        for r in self.rabbits:
            if r.alive:
                if self.field[r.x, r.y] != 0:
                    r.eat()
                    self.field[r.x, r.y] = 0
                else:
                    r.hunger += 1

        # run checks foxes on rabbits (fox eat rabbit)
        for f in self.foxes:
            if f.alive:
                pos = (f.x, f.y)
                if pos in rabbit_locations:
                    rabbits_here = rabbit_locations[pos]
                    if len(rabbits_here) > 0:
                        f.eat(rabbits_here[0])
                else:
                    f.hunger += 1

    def reproduce(self):
        """
        Animals reproduce based on hunger level.
        Returns empty list if hunger is too high.
        """
        new_rabbits = []
        for r in self.rabbits:
            if r.alive:
                babies = r.reproduce(r)
                new_rabbits.extend(babies)

        new_foxes = []
        for f in self.foxes:
            if f.alive:
                babies = f.reproduce(f)
                new_foxes.extend(babies)

        self.rabbits.extend(new_rabbits)
        self.foxes.extend(new_foxes)

    def survive(self):
        """
        PDF Requirement: "If the hunger level reaches the starvation level,
        the animal dies."
        Also: "Mark it dead and remove it from the population as part of
        determining which animals survived to the next generation."
        """
        for animal in self.rabbits + self.foxes:
            if animal.hunger >= animal.starvation_level:
                animal.alive = False

        self.rabbits = [r for r in self.rabbits if r.alive]
        self.foxes = [f for f in self.foxes if f.alive]

    def grow_grass(self):
        """Grass grows back with some probability at each location"""
        new_grass = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, new_grass)

    def generation(self):
        """
        One generation cycle in the correct order:
        1. Move animals
        2. Eat (hunger management happens here)
        3. Reproduce (based on current hunger level)
        4. Survive (remove starved animals)
        5. Grow grass
        """
        self.move_animals()
        self.eat()
        self.reproduce()
        self.survive()
        self.grow_grass()

        self.generation_count += 1
        self.rabbit_history.append(len(self.rabbits))
        self.fox_history.append(len(self.foxes))


# =========== Animation ============
def animate(i, field, img, ax_main, ax_time, line_rabbits, line_foxes):
    """
    Animation function that updates both the field display and time series plot.
    """
    field.generation()

    display = field.field.copy()  # local for display

    for r in field.rabbits:
        if r.alive:
            display[r.y, r.x] = 2

    for f in field.foxes:
        if f.alive:
            display[f.y, f.x] = 3

    img.set_array(display)
    ax_main.set_title(
        f"Generation {field.generation_count} | Rabbits: {len(field.rabbits)} Foxes: {len(field.foxes)}"
    )

    line_rabbits.set_data(range(len(field.rabbit_history)), field.rabbit_history)
    line_foxes.set_data(range(len(field.fox_history)), field.fox_history)

    ax_time.set_xlim(0, max(len(field.rabbit_history), 100))

    max_pop = max(
        max(field.rabbit_history, default=1), max(field.fox_history, default=1)
    )
    ax_time.set_ylim(0, max_pop * 1.1)  # extend the display as populations grow

    return (img,)


def main():
    """
    Main function to initialize and run the simulation.
    """
    field = Field()

    for _ in range(INIT_RABBITS):
        field.add_rabbit(Animal())

    for _ in range(INIT_FOXES):
        field.add_fox(Animal())

    field.rabbit_history.append(len(field.rabbits))
    field.fox_history.append(len(field.foxes))

    fig = plt.figure(figsize=(FIGSIZE * 2, FIGSIZE))
    ax_main = plt.subplot(1, 2, 1)
    ax_time = plt.subplot(1, 2, 2)

    cmap = plt.cm.colors.ListedColormap(["black", "green", "white", "red"])
    img = ax_main.imshow(
        field.field, cmap=cmap, vmin=0, vmax=3, interpolation="hamming"
    )
    ax_main.set_title(
        f"Generation {field.generation_count} | Rabbits: {INIT_RABBITS} Foxes: {INIT_FOXES}"
    )

    ax_time.set_xlabel("Generation")
    ax_time.set_ylabel("Population")
    ax_time.set_title("Population Over Time")
    ax_time.grid(True, alpha=0.3)

    (line_rabbits,) = ax_time.plot([], [], "blue", linewidth=2, label="Rabbits")
    (line_foxes,) = ax_time.plot([], [], "red", linewidth=2, label="Foxes")
    ax_time.legend(loc="upper right")

    plt.tight_layout()

    anim = animation.FuncAnimation(
        fig,
        animate,
        fargs=(field, img, ax_main, ax_time, line_rabbits, line_foxes),
        frames=10**100,
        interval=200,
    )
    plt.show()


if __name__ == "__main__":
    main()
