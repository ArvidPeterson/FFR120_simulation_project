from AgentSuper import AgentSuper
from Rat import Rat
import numpy as np


class Bird(AgentSuper):


     def __init__(self, x_nest = None, y_nest = None):
         super().__init__(self)
         #all_positions =
         self.is_in_nest = True
         self.has_nest = False


     def place_nest(self,nest_list,all_positions):
         available_positions = np.delete(all_positions,nest_list)
         pick_position = np.random.randit(0,len(available_positions)-1)
         nest_x = available_positions(pick_position, 1)
         nest_y = available_positions(pick_position, 2)


         return nest_x,nest_y

     def check_is_in_nest(self):
         return self.is_in_nest

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

    def place_nest(self,nest_list,all_positions):
         available_positions = np.delete(all_positions,nest_list)
         pick_position = np.random.randit(0,len(available_positions)-1)
         nest_x = available_positions(pick_position, 1)
         nest_y = available_positions(pick_position, 2)

         return nest_x, nest_y

    def check_is_in_nest(self):
         return self.is_in_nest

    def coordinate_to_index(self, coord):
        x, y = coord
        return x + y * self.grid_size

    def index_to_coordinate(self, index):
        pass

    def place_nest(self, nest_list):
        all_indices = np.linspace(0,self.grid_size, self.grid_size - 1, dtype=int )
        nest_indices = []
        for nest in nest_list:
            nest_index = self.coordinate_to_index((nest.x, nest.y))
            nest_indices.append(nest_index)
        allowed_indices = np.delete(all_indices, nest_indices)



    def is_rat(self, x):
        return isinstance(x, Rat)
