import matplotlib.pyplot as plt
import numpy as np


''' Agent superclass. Rats nests and birds inherit this class '''


class AgentSuper:

    def __init__(self, grid_size, x_start, y_start, life_time=1):

        self.grid_size = grid_size
        self.x = x_start
        self.y = y_start
        self.life_time = life_time
        self.age = 0

    def check_age(self):

        return self.age < self.life_time
    # pajskal
