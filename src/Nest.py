from AgentSuper import AgentSuper
import numpy as np


'''Nest Class'''


class Nest(AgentSuper):
    def __init__(self, grid_size, x_start, y_start, topological_map, life_time, parent_bird):
        AgentSuper.__init__(self, grid_size, x_start, y_start, topological_map, life_time)
        self.hatch_time = self._set_hatch_time()
        self.counter = 0
        self.parent = parent_bird  # reference to a bird object

    def tick(self):
        self.counter += 1

    def hatch(self):
        self.counter = 0

    def _set_hatch_time(self):
        offs = int(0.1 * self.life_time * np.random.randn())  # set a 10 percent random offset

        return self.life_time + offs