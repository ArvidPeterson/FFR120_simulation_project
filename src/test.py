
from Bird import Bird
from Nest import Nest

gridSize = 3

bird = Bird(gridSize, 4, 2)


nest1 = Nest(gridSize, 0, 2)
nest2 = Nest(gridSize, 1, 2)
nest3 = Nest(gridSize, 1, 0)
nest_list = []
nest_list.append(nest1)
nest_list.append(nest2)
nest_list.append(nest3)

new_nest = bird.place_nest(nest_list)

for nest in nest_list:
    print(nest.x)
    print(nest.y)
    print(' ')


print(new_nest.x)
print(new_nest.y)
print('complete')


