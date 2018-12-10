from AgentSuper import AgentSuper
from Rat import Rat
from Nest import Nest
import numpy as np


class Bird(AgentSuper):
    def __init__(self, grid_size, x, y, topological_map, life_time=1):
        AgentSuper.__init__(self, grid_size, x, y, topological_map, life_time)
        self.is_in_nest = True
        self.has_nest = False

    def check_is_in_nest(self):
        return self.is_in_nest

    def move(self):
        r = np.random.randint(0, 3)    # the bird spents 1/3 of the time away from nest in this model
        if r == 0:
            self.is_in_nest = False
        else:
            self.is_in_nest = True

    def coordinate_to_index(self, coord):
        x, y = coord
        return x + y * self.grid_size

    def index_to_coordinate(self, index):
        x = index % self.grid_size
        y = int(np.floor(index/self.grid_size))
        return x, y

    def place_nest(self, nest_list):
        # Creates a temporary grid used to determine where nests can be created.
        all_indices = range(self.grid_size**2)
        nest_indices = []
        for nest in nest_list:
            # The coordinates of the current nest is turned into an index. This index is added to the list of indeces where nests exist.
            nest_indices.append(self.coordinate_to_index((nest.x, nest.y)))
        available_indices = np.delete(all_indices, nest_indices)
        random_index = np.random.randint(0, len(available_indices))
        (x_new_nest, y_new_nest) = self.index_to_coordinate(available_indices[random_index])

        while self.topological_map[x_new_nest, y_new_nest] < 1:
            # if position is spawned in water in topological map, get new random position
            random_index = np.random.randint(0, len(available_indices))
            (x_new_nest, y_new_nest) = self.index_to_coordinate(available_indices[random_index])

        # ==========================================================
        some_life_time = 1  # THIS SHOULD BE SET TO THE PROPER VALUE
        # ==========================================================

        # todo: might want to make nests have a different life time?

        # --- place the new nest --- #
        new_nest = Nest(self.grid_size, x_new_nest, y_new_nest, self.topological_map, self.life_time, self)

        # --- move to the new nest --- #
        self.x = x_new_nest
        self.y = y_new_nest
        self.has_nest = True
        return new_nest

    def is_rat(self, x):  # TODO: Remove?
        return isinstance(x, Rat)
