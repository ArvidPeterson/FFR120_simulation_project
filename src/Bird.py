
from SuperAgent import SuperAgent
import numpy as np

class Bird(SuperAgent):
     def __init__(self, x_nest = None, y_nest = None):
         super().__init__(self)
         all_positions =
         self.is_in_nest
         self.has_nest = False


     def place_nest(self,nest_list,all_positions):
         available_positions = np.delete(all_positions,nest_list)
         pick_position = np.random.randit(0,len(available_positions)-1)
         nest_x = available_positions(pick_position, 1)
         nest_y = available_positions(pick_position, 2)

         return next_x,nest_y

     def check_is_in_nest(self):
         boolean = randint(0,1)

         if boolean == 0:
             is_in_nest = False
         else:
             is_in_nest = True

         return is_in_nest
