import random

# initialize 2d list representing block of a town
def makeGrid(rows=6, cols=9, name="area"):
    # initialize list
    grid = []
    # generate 2d list with 0s as place holder
    for row in range(rows):
        grid += [[0]*cols]
    if name == "area":
        # add -1s, which represent the road
        for row in grid:
            row.append(-1)
        grid.append([-1]*(cols+1))
    return grid

# creates a grid map of a residential area
def makeResArea():
    grid = makeGrid() # initialize grid
    for row in grid:
        row[4] = -1 # add road in the middle of grid
    for start in [0,5]: # these have the faces of the houses
        index = 0
        for col in grid[start]:
            if col == 0: # if space is open
                grid[start][index] = random.randint(1,3) # 3 houses available
            index += 1
    return grid

# creates a grid map of a downtown area
def makeDowntownArea():
    grid = makeGrid() # initialize grid
    for start in [0,5]: # these rows have the faces of the buildings
        if start == 0: index = 0
        elif start == 5: index = 2
        grid[start][index] = random.randint(4,6) # 3 buildings available
        grid[start][index+3] = random.randint(4,6)
        grid[start][index+6] = random.randint(4,6)
    return grid

# creates grid consisting of open, residential, and downtown area assignment
#########################################################
# open area = -1
# special tower (the aim position) = "tower"
# city area = 1
# residential area = 2
#########################################################

def makeTownGrid():
    grid = makeGrid(9, 11, "town")
    (numRows, numCols) = (len(grid), len(grid[0]))
    # initialize areas
    rowCount = 0
    for row in grid:
        row[0] = -1
        for index in range(1,8):
            if index < 4: row[index] = 1
            elif index > 4: row[index] = 2
            else: row[index] = random.randint(1,2)
        for index in range(8,11):
            if rowCount in [0, 1, 7, 8]: row[index] = 2
            else: row[index] = -1
        grid[4][10] = "tower"
        rowCount += 1
    return grid

# sets up the city details
def createTown():
    grid = makeTownGrid()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            block = grid[row][col]
            if block == 1:
                grid[row][col] = makeDowntownArea()
            elif block == 2:
                grid[row][col] = makeResArea()
    return grid