import numpy as np
import matplotlib.pyplot as pl
from AgentSuper import AgentSuper


''' Rat class '''


class Rat(AgentSuper):  # inherits AgentSuper

    def __init__(self, grid_size, x_start, y_start, life_time):
        AgentSuper.__init__(self, grid_size, x_start, y_start, life_time)
        self.last_direction_idx = 0

    def move(self):

        ''' Moves the rat one step in a pseudo random walk, rat is not allowed to go back to old position'''

        self.life_time += 1

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
            self.last_direction_idx = 3
        elif direction == 3 and self.last_direction_idx != 2:  # go down
            y -= 1
            self.last_direction_idx = 4

        coord = np.array([x, y])

        coord[coord > self.grid_size] = 0
        coord[coord < 0] = self.grid_size

        self.x = coord[0]
        self.y = coord[1]

        return [self.x, self.y]



