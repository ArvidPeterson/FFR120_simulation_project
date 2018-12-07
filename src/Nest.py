from AgentSuper import AgentSuper


'''Nest Class'''


class Nest(AgentSuper):
    def __init__(self, grid_size, x, y, life_time):
        AgentSuper.__init__(self, grid_size, x, y, life_time)
        self.hatch_time = self.life_time
        self.counter = 0


    def move(self):
        self.counter += 1
