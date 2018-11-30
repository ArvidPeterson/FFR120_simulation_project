import numpy as np
from SuperAgent import SuperAgent

class Bird(SuperAgent):
    def __init__(self, x, y, grid_size):
        super().__init__(self, x, y)
        self.x_nest
        self.y_nest
        self.is_in_nest
        self.nest
        self.has_nest = False
        self.x = x
        self.y = y
        self.grid_size = grid_size

    def coordinate_to_index(self, coord):
        x, y = coord
        return x + y * self.grid_size

    def index_to_coordinate(self, index):


    def place_nest(self, nest_list):
        all_indices = np.linspace(0,self.grid_size, self.grid_size - 1, dtype=int )
        nest_indices = []
        for nest in nest_list:
            nest_index = self.coordinate_to_index((nest.x, nest.y))
            nest_indices.append(nest_index)
        allowed_indices = np.delete(all_indices, nest_indices)



    def is_rat(self, x):
        return isinstance(x, Rat)


        # nest.x, nest.y