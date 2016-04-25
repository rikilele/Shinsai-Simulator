# scene == the app's main window (self)
# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# import additional modules
import random

# from same directory
from Building import Building

class Terrain(ShowBase):
    def __init__(self, scene, name):
        self.name = name + ".egg"
        self.path = "models/terrains/"+name+"/"+self.name
        self.terrain = scene.loader.loadModel(self.path)
        # Reparent the model to render.
        self.terrain.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.terrain.setScale(600)
        self.terrain.setPos(0, 0, 0)
        # Attributes for making city grid
        self.cityLatt = 9
        self.cityLong = 11
        self.buildBuildings(scene) # place all the buildings

    def buildBuildings(self, scene):
        # set dimensions
        firstPoint = self.terrain.getTightBounds()[0]
        secondPoint = self.terrain.getTightBounds()[1]
        (x1, x2) = firstPoint.getX(), secondPoint.getX()
        (y1, y2) = firstPoint.getY(), secondPoint.getY()
        (length, width) = (abs(x1-x2)/self.cityLong, abs(y1-y2)/self.cityLatt)
        origin = (min(x1, x2), min(y1, y2)) # tuple of origin
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
                elif cell == -1:
                    print ("NOTHING")
                currY -= width
            currX -= length

    def renderBlocks(self, scene, block, length, width, origin):
        # currX = origin[0]
        # for row in block:
        #     currY = origin[1]
        #     for cell in row:
        #         if cell == "tower":
        #             self.tower = Building(scene, "tower", currX, currY, 0)
        #         elif type(cell) == list:
        #             pass
        #         elif cell == -1:
        #             print "NOTHING"
        #         currY -= width
        #     currX -= length
        pass

        self.building = Building(scene, "concrete", 0, 0, 0)
        self.building2 = Building(scene, "R", -1000, 1000, 0)
        self.building3 = Building(scene, "house1", 2000, 2000, 0)
        self.building4 = Building(scene, "tower", 3000, 3000, 0)
        self.building5 = Building(scene, "house2", 4000, 4000, 0)
        self.building6 = Building(scene, "house3", 5000, 5000, 0)
        self.building7 = Building(scene, "build", -10000, 6000, 0)

    ########################################################
    # algorithm for creating a city map
    ########################################################

    # initialize 2d list representing block of a town
    def makeGrid(self, rows=6, cols=9, name="area"):
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

    #########################################################
    # red house = 1
    # green house = 2
    # blue house = 3
    #########################################################

    # creates a grid map of a residential area
    def makeResArea(self):
        grid = self.makeGrid() # initialize grid
        for row in grid:
            row[4] = -1 # add road in the middle of grid
        for start in [0,3]: # these have the faces of the houses
            index = 0
            for col in grid[start]:
                if col == 0: # if space is open
                    grid[start][index] = random.randint(1,3) # 3 houses avail.
                index += 1
        return grid

    #########################################################
    # big building = 4
    # concrete building = 5
    # tower = 6
    # restaurant = 7 (two buildings side by side)
    #########################################################

    # creates a grid map of a downtown area
    def makeDowntownArea(self):
        grid = self.makeGrid() # initialize grid
        for start in [0,3]: # these rows have the faces of the buildings
            index = 2
            grid[start][index] = random.randint(4,7) # 4 buildings available
            grid[start][index+3] = random.randint(4,7)
            grid[start][index+6] = random.randint(4,7)
        return grid

    #########################################################
    # open area = -1
    # special tower (the aim position) = "tower"
    # city area = 1
    # residential area = 2
    #########################################################

    # creates grid consisting of open, residential, and downtown area assignment
    def makeTownGrid(self):
        grid = self.makeGrid(self.cityLatt, self.cityLong, "town")
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
            