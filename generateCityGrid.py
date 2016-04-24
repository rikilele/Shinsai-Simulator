import random

# initialize 2d list representing block of a town
def makeBlock():
    # all blocks in Shinsa-Simulator have this dimension
    (rows, cols) = (6, 9)
    # initialize list
    grid = []
    # generate 2d list with 0s as place holder
    for row in range(rows):
        grid += [[0]*cols]
    # add -1s, which represent the road
    for row in grid:
        row.append(-1)
    grid.append([-1]*(cols+1))
    return grid

# creates a grid map of a residential area
def makeResArea():
    grid = makeBlock() # initialize grid
    for row in grid:
        row[4] = -1 # add road in the middle of grid
    for start in [0,5]: # these have the faces of the houses
        index = 0
        for col in grid[start]:
            if col == 0: # if space is open
                grid[start][index] = random.randint(1,3) # 3 houses available
            index += 1
    print (grid)
    return grid

# creates a grid map of a downtown area
def makeDowntownArea():
    grid = makeBlock() # initialize grid
    for start in [0,5]: # these rows have the faces of the buildings
        if start == 0: index = 0
        elif start == 5: index = 2
        grid[start][index] = random.randint(4,6) # 3 buildings available
        grid[start][index+3] = random.randint(4,6)
        grid[start][index+6] = random.randint(4,6)
    print (grid)
    return grid


makeResArea()
makeDowntownArea()
