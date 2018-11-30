import numpy as np
import matplotlib.pyplot as pl
from AgentSuper import AgentSuper


''' Rat class '''


class Rat(AgentSuper):

    def __init__(self, grid_size, x_start, y_start, life_time):
        AgentSuper.__init__(self, grid_size, x_start, y_start, life_time)

    def move(self):

        direction = np.random.randi(4)

        if direction == 0:  # go right
            self.x += 1
        elif direction == 1:  # go left
            self.x -= 1
        elif direction == 2:  # go up
            self.y += 1
        elif direction == 3:  # go down
            self.y -= 1

        for coordinate in [self.x, self.y]:
            if coordinate > self.grid_size:
                coordinate = 0
            elif coordinate < 0:
                coordinate = self.grid_size



