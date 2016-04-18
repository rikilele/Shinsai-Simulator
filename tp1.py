# Initial TP1
# Riki Singh Khorana + rkhorana + MM

# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for calculations
from math import sin, cos, pi

# import classes written by myself on separate files
from Player import Player

""" No LOD for terrain, but buildings and water definitely """

# used only to load city terrain specified by user
class Terrain(ShowBase):
    def __init__(self, scene):

        self.bamboo = scene.loader.loadModel("environment")
        # Reparent the model to render.
        self.bamboo.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.bamboo.setScale(2)
        self.bamboo.setPos(0, 0, -40)

class Building(ShowBase):
    def __init__(self, scene, name):
        if name == "concrete":
            self.buildConcrete(scene)
        if name == "R":
            self.buildRBuilding(scene)

    def buildConcrete(self, scene):
        for i in range(4):
            scene.building = scene.loader.loadModel("models/concrete/concrete.egg")
            scene.building.reparentTo(scene.render)
            scene.building.setScale(100)
            scene.building.setHpr(0,0,0)
            scene.building.setPos(i*200, 0, -50)

    def buildRBuilding(self, scene):
        for i in range(4):
            scene.building = scene.loader.loadModel("models/r-building/r-building.egg")
            scene.building.reparentTo(scene.render)
            scene.building.setScale(100)
            scene.building.setHpr(0,0,0)
            scene.building.setPos(i*200, -400, -50)

class Water(ShowBase):
    pass
class Glass(ShowBase):
    pass
class Citizen(ShowBase):
    pass

class MyApp(ShowBase):

    paused = False

    def __init__(self):
        ShowBase.__init__(self) # initializes Panda window from ShowBase
        self.disableMouse() # disable camera control by mouse
        self.enableParticles() # enables particle calculations for physics
        self.makeMouseRelative()
        self.accept("p", self.togglePause) # "p" key for pause
        
        # Generate objects
        self.terrain = Terrain(self)
        self.player = Player(self)
        self.building1 = Building(self, "concrete")
        self.building2 = Building(self, "R")

    def makeMouseRelative(self):
        props = WindowProperties() # initates window node
        props.setCursorHidden(True) # hides cursor
        props.setMouseMode(WindowProperties.M_relative) # cursor stays
        self.win.requestProperties(props) # window accepts changes

    def togglePause(self):
        print ("pause pressed")
        if MyApp.paused:
            self.makeMouseRelative()
            MyApp.paused = False
        else:
            props = WindowProperties() # initiates window node
            props.setCursorHidden(False) # cursor shows
            props.setMouseMode(WindowProperties.M_absolute) # cursor moves
            self.win.requestProperties(props) # window accepts changes
            MyApp.paused = True

print ("starting app")
app = MyApp()
app.run()