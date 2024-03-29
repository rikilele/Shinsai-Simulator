# scene == the app's main window (self)
# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

# import additional modules
import random

# from same directory
from Building import Building
from database.ZInfo import ZInfo

class Terrain(ShowBase):
    def __init__(self, scene, name):
        self.name = name + ".egg"
        self.path = "models/terrains/"+name+"/"+self.name
        self.terrain = scene.loader.loadModel(self.path)
        self.scale = 450
        # Reparent the model to render.
        self.terrain.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.terrain.setScale(self.scale)
        self.terrain.setPos(0, 0, 0)
        # Attributes for making city grid
        self.cityLatt = 9
        self.cityLong = 11
        self.initializeZData()
        self.buildBuildings(scene) # place all the buildings
        self.placeNorth(scene) # places a "North" reference point

    def initializeZData(self):
        data = ZInfo(self.name)
        self.zData = data.newDict

    def placeNorth(self, scene):
        self.north = Building(scene, "tower", -10**5, -10**15, 10**3)

    def buildBuildings(self, scene):
        # set dimensions
        firstPoint = self.terrain.getTightBounds()[0]
        secondPoint = self.terrain.getTightBounds()[1]
        (x1, x2) = firstPoint.getX(), secondPoint.getX()
        (y1, y2) = firstPoint.getY(), secondPoint.getY()
        (z1, z2) = firstPoint.getZ(), secondPoint.getZ()
        # set measurements
        (length, width) = (abs(x1-x2)/self.cityLatt, abs(y1-y2)/self.cityLong)
        (height, self.maxZ, self.minZ) = (abs(z1-z2), max(z1, z2), min(z1, z2))
        origin = (max(x1, x2), max(y1, y2)) # tuple of origin
        self.origin = origin
        self.dimensions = (length*self.cityLatt, width*self.cityLong, height)
        # create town based on measurements
        cityMap = self.createTown()
        self.placeBuilds(scene, cityMap, length, width, origin)

    def placeBuilds(self, scene, cityMap, length, width, origin):
        currX = origin[0]
        for row in cityMap:
            currY = origin[1]
            for cell in row:
                if cell == "tower":
                    self.tower = Building(scene, "tower", currX, currY, 0)
                elif type(cell) == list:
                    self.renderBlocks(scene, cell, length/9, 
                                      width/11, (currX, currY))
                currY -= width
            currX -= length

    def renderBlocks(self, scene, block, length, width, origin):
        buildCode = {1:"house1", 2:"house2", 3:"house3", 4:"build", \
                     5:"concrete", 6:"r", 7:"cafe", 8:"old"}
        currX = origin[0] # resets data so to fit key to ZData
        for row in block:
            currY = origin[1] # resets data to fit key to ZData
            for cell in row:
                try: # try to read z-value from database
                    (x, y) = (int(currX//100*100)-400, int(currY//100*100))
                    currZ = self.zData[(x, y)]
                except: continue
                if cell in buildCode:
                    name = buildCode[cell]
                    cell = Building(scene, name, currX, currY, currZ)
                currY -= width
            currX -= length

    ########################################################
    # algorithm for creating a city map
    ########################################################

    # initialize 2d list representing block of a town
    def makeGrid(self, rows=7, cols=10):
        # initialize list
        grid = []
        # generate 2d list with 0s as place holder
        for row in range(rows):
            grid += [[0]*cols]
        return grid

    #########################################################
    # red house = 1
    # green house = 2
    # blue house = 3
    #########################################################

    # creates a grid map of a residential area
    def makeResArea(self):
        grid = self.makeGrid() # initialize grid
        for start in range(0,7,3): # these have the faces of the houses
            index = 0
            for col in grid[start]:
                if col == 0 and index%2 == 0: # if space is open
                    grid[start][index] = random.randint(1,3) # 3 houses avail.
                index += 1
        return grid

    #########################################################
    # big building = 4
    # concrete building = 5
    # signature building = 6
    # cafe = 7
    # old building = 8
    #########################################################

    # creates a grid map of a downtown area
    def makeDowntownArea(self):
        grid = self.makeGrid() # initialize grid
        for start in [3,6]: # these rows have the faces of the buildings
            index = 0
            grid[start][index] = random.randint(4,8) # 4 buildings available
            grid[start][index+3] = random.randint(4,8)
            grid[start][index+6] = random.randint(4,8)
        return grid

    #########################################################
    # open area = -1
    # special tower (the aim position) = "tower"
    # city area = 1
    # residential area = 2
    #########################################################

    # creates grid consist of open, residential, and downtown area assignment
    def makeTownGrid(self):
        grid = self.makeGrid(self.cityLatt, self.cityLong)
        (numRows, numCols) = (len(grid), len(grid[0]))
        # initialize areas
        rowCount = 0
        for row in grid:
            row[0] = -1
            row[1] = -1
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

    # sets up the whole map with details
    def createTown(self):
        grid = self.makeTownGrid()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                block = grid[row][col]
                if block == 1:
                    grid[row][col] = self.makeDowntownArea()
                elif block == 2:
                    grid[row][col] = self.makeResArea()
        return grid
