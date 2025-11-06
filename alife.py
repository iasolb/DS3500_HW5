import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy

# =========== Constants ============

ARRSIZE = 200
FIGSIZE = 8
INIT_RABBITS = 200
INIT_FOXES = 50
GRASS_RATE = 0.5
OFFSPRING = 4
STARVATION_LEVEL = 5
REPRODUCTION_LEVEL = 1
"""
COLOR_MAP:
0: Black (Nothing at that location)
1: Green (Grass but no animals)
2: White (Rabbit – but no foxes)
3: Red (Fox)
"""

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
        return [
            copy.deepcopy(parent) for i in range(rnd.randint(1, self.max_offspring))
        ]

    def eat(self, to_eat=None):
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

        # REVIEW!!
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
        for r in self.rabbits:
            if r.alive:
                if self.field[r.x, r.y] != 0:
                    r.eat()
                    self.field[r.y, r.x] = 0
                else:
                    r.hunger += 1

        for f in self.foxes:
            if f.alive:
                ate_something = False
                for r in self.rabbits:
                    if r.alive and r.x == f.x and r.y == f.y:
                        f.eat(r)
                        ate_something = True
                        break  # stops the loop
                if not ate_something:
                    f.hunger += 1

    def reproduce(self):
        for r in self.rabbits:
            if r.alive and r.hunger <= r.reproduction_level:
                babies = r.reproduce(r)
                self.rabbits.extend(babies)
        for f in self.foxes:
            if f.alive and f.hunger <= f.reproduction_level:
                babies = f.reproduce(f)
                self.foxes.extend(babies)

    def survive(self):
        for animal in self.rabbits + self.foxes:
            if animal.hunger >= animal.starvation_level:
                animal.alive = False
        self.rabbits = [r for r in self.rabbits if r.alive]
        self.foxes = [f for f in self.foxes if f.alive]

    def grow_grass(self):
        new_grass = (np.random.rand(ARRSIZE, ARRSIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, new_grass)

    # REVIEW!!
    def generation(self):
        self.move_animals()
        self.eat()
        self.reproduce()
        self.survive()
        self.grow_grass()

        # Update generation counter and track populations - REVIEW!!
        self.generation_count += 1
        self.rabbit_history.append(len(self.rabbits))
        self.fox_history.append(len(self.foxes))


# =========== Animation ============
def update(frame, field, img, ax_main, ax_time, line_rabbits, line_foxes):
    field.generation()

    # Update main field display - REVIEW!!
    display = field.field.copy()
    for r in field.rabbits:
        if r.alive:
            display[r.y, r.x] = 2
    for f in field.foxes:
        if f.alive:
            display[f.y, f.x] = 3
    img.set_data(display)
    ax_main.set_title(
        f"Generation {field.generation_count} | Rabbits: {len(field.rabbits)} Foxes: {len(field.foxes)}"
    )
    line_rabbits.set_data(range(len(field.rabbit_history)), field.rabbit_history)
    line_foxes.set_data(range(len(field.fox_history)), field.fox_history)

    ax_time.set_xlim(0, max(len(field.rabbit_history), 100))

    max_pop = max(
        max(field.rabbit_history, default=1), max(field.fox_history, default=1)
    )
    ax_time.set_ylim(0, max_pop * 1.1)

    return [img, line_rabbits, line_foxes]


def main():
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

    # Setup main field display
    cmap = plt.cm.colors.ListedColormap(["black", "green", "white", "red"])
    img = ax_main.imshow(field.field, cmap=cmap, vmin=0, vmax=3)
    ax_main.set_title(
        f"Generation {field.generation_count} | Rabbits: {INIT_RABBITS} Foxes: {INIT_FOXES}"
    )

    # Setup time series plot
    ax_time.set_xlabel("Generation")
    ax_time.set_ylabel("Population")
    ax_time.set_title("Population Over Time")
    ax_time.grid(True, alpha=0.3)

    (line_rabbits,) = ax_time.plot([], [], "w-", linewidth=2, label="Rabbits")
    (line_foxes,) = ax_time.plot([], [], "r-", linewidth=2, label="Foxes")
    ax_time.legend(loc="upper right")

    plt.tight_layout()

    ani = animation.FuncAnimation(
        fig,
        update,
        fargs=(field, img, ax_main, ax_time, line_rabbits, line_foxes),
        frames=10**100,
        interval=200,
        blit=True,
    )
    plt.show()


if __name__ == "__main__":
    main()
