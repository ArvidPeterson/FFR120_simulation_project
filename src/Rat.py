import numpy as np
import matplotlib.pyplot as plt
from AgentSuper import AgentSuper


''' Rat class '''


class Rat(AgentSuper):  # inherits AgentSuper

    def __init__(self, grid_size, x_start, y_start, topological_map, life_time):
        AgentSuper.__init__(self, grid_size, x_start, y_start, life_time)
        self.topological_map = topological_map

    def move(self):

        ''' Moves the rat one step in a random walk, von Neuman neighbourhood '''

        self.life_time += 1

        x = self.x
        y = self.y

        direction = np.random.randint(0, 4)

        if direction == 0:  # go right
            x += 1
        elif direction == 1:  # go left
            x -= 1
        elif direction == 2:  # go up
            y += 1
        elif direction == 3:  # go down
            y -= 1

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



