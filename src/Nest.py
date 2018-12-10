from AgentSuper import AgentSuper


'''Nest Class'''


class Nest(AgentSuper):
    def __init__(self, grid_size, x_start, y_start, topological_map, life_time, parent):
        AgentSuper.__init__(self, grid_size, x_start, y_start, topological_map, life_time)
        self.hatch_time = self.life_time
        self.counter = 0
        self.parent = parent

    def tick(self):
        self.counter += 1

