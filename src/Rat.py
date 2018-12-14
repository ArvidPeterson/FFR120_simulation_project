import numpy as np
import matplotlib.pyplot as plt
from AgentSuper import AgentSuper


''' Rat class '''


class Rat(AgentSuper):  # inherits AgentSuper

    def __init__(self, grid_size, x_start, y_start, topological_map, life_time, initial_energy):
        AgentSuper.__init__(self, grid_size, x_start, y_start, topological_map, life_time)
        self.last_direction_idx = 0
        self.energy = initial_energy
        self.p_move = 1.0
        self.time_since_last_spawn = 0
        self.time_to_spawn_new_rat = 100
        self.should_spawn_new_rat = False
    ''' Moves the rat one step in pseudo random walk, cannot go back to same position directly'''

    def move(self):
        self.time_since_last_spawn += 1  # increase time since last spawn
        self.set_should_spawn()
        self.life_time += 1  # increase life time

        # use this to modulate activity level in rats
        r = np.random.rand()
        if r > self.p_move:
            return [self.x, self.y]


        x = self.x
        y = self.y

        direction = np.random.randint(0, 4)

        if direction == 0 and self.last_direction_idx != 1:  # go right
            x += 1
            self.last_direction_idx = 0

        elif direction == 1 and self.last_direction_idx != 0:  # go left
            x -= 1
            self.last_direction_idx = 1

        elif direction == 2 and self.last_direction_idx != 3:  # go up
            y += 1
            self.last_direction_idx = 2

        elif direction == 3 and self.last_direction_idx != 2:  # go down
            y -= 1
            self.last_direction_idx = 3

        coord = np.array([x, y])

        coord[coord >= self.grid_size] = 0  # if outside grid
        coord[coord <= 0] = self.grid_size

        while self.topological_map[coord[0], coord[1]] < 1:  # if in water
            [x, y] = self.move()
            coord[0] = x
            coord[1] = y

        self.x = coord[0]
        self.y = coord[1]

        return [self.x, self.y]

    # sets the variable telling to spawn new rat or not
    def set_should_spawn(self):
        should_spawn = self.time_since_last_spawn > self.time_to_spawn_new_rat
        self.should_spawn_new_rat = should_spawn

    # resets spawning variables
    def has_spawned(self):
        self.time_since_last_spawn = 0
        self.should_spawn_new_rat = False






