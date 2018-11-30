from AgentSuper import AgentSuper


'''Nest Class'''


class Nest(AgentSuper):
    def __init__(self, grid_size, x, y, life_time):
        AgentSuper.__init__(self, grid_size, x, y, life_time)
        self.x = x
        self.y = y
        '''
        parent, ht, 
        self.parent_id = parent
        self.hatch_time = ht
        self.incubation_time = 0

    def move(self):
        self.incubation_time += 1
        
    def check_hatch(self)
        return self.incubation_time>hatch_time

    def hatch(self):
        if check_hatch():
            lattice.spawn(self)

    '''
