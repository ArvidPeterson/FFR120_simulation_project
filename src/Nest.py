
class Nest:
    def __init__(self, x, y, id1, id2, ht, ct):
        self.x = x
        self.y = y
        self.parent_id = id
        self.hatch_time = ht
        self.count_time = ct

    def move(self):
        self.count_time += 1

    def hatch(self):
        lattice.spawn(self)

    def die(self):
        del self
        lattice.nest_list(self,remove)