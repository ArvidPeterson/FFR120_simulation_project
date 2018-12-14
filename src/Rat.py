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
    ''' Moves the rat one step in pseudo random walk, cannot go back to same position directly'''

    def move(self):

        self.life_time += 1

        r = np.random.rand()

        if r > self.p_move:  # finite probability to move use to modulate aggression
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





