# TP2
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
from Building import Building

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

class Water(ShowBase):
    pass
class Glass(ShowBase):
    pass
class Citizen(ShowBase):
    pass

class MyApp(ShowBase):

    paused = False

    def __init__(self):

        self.initialize()

        # Generate objects
        self.terrain = Terrain(self)
        self.player = Player(self)
        self.building1 = Building(self, "concrete")

        # Initialize list that keeps rendered objects
        self.objects = [self.player]

        # Initialize collision handlers
        self.pusher = CollisionHandlerPusher()
        self.traverser = CollisionTraverser("main")
        self.queue = CollisionHandlerQueue()
        base.cTrav = self.traverser # allows collision to be tested every frame
        self.cameraCollided = False

        self.readObjects()

    ################################################################
    # Data Helpers
    ################################################################

    def initialize(self):
        ShowBase.__init__(self) # initializes Panda window from ShowBase
        self.disableMouse() # disable camera control by mouse
        self.makeMouseRelative()
        self.keyPressed()
        self.timerFired()
        self.mouseActivity()

    # for collision detection
    def readObjects(self):
        # (self.traverser).addCollider(self.camera, self.queue)
        for entity in self.objects:
            try:
                for information in entity.collidable:
                    (fromObject, obj) = information
                    (self.traverser).addCollider(fromObject, self.queue)
                    print ("added collision!")
            except:
                print ("didn't add collision")

    def makeMouseRelative(self):
        props = WindowProperties() # initates window node
        props.setCursorHidden(True) # hides cursor
        props.setMouseMode(WindowProperties.M_relative) # cursor stays
        self.win.requestProperties(props) # window accepts changes

    ################################################################
    # Helpers for keyPressed
    ################################################################

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

    ################################################################
    # Helpers for timerFired
    ################################################################

    def checkCollision(self, task):
        collided = False
        for entry in self.queue.getEntries():
            print ("detected")
            print(entry)
            collided = True
        self.cameraCollided = collided
        return Task.cont

    ################################################################
    # Event handlers
    ################################################################

    # responds to key press
    def keyPressed(self):
        self.accept("p", self.togglePause) # "p" key for pause
    
    # adds task that should be fired every second
    def timerFired(self):
        taskMgr.add(self.checkCollision, "collision")

    def mouseActivity(self):
        pass

print ("starting app")
app = MyApp()
app.run()