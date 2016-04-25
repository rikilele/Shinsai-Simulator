# TP3
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
from Terrain import Terrain
from Water import Water
from Background import Background

""" No LOD for terrain, but buildings and water definitely """

class Glass(ShowBase):
    pass
class Citizen(ShowBase):
    pass

class MyApp(ShowBase):

    paused = False

    def __init__(self):

        self.initializeFunctions()

        # Initialize collision handlers
        self.traverser = CollisionTraverser("main")
        base.cTrav = self.traverser # allows collision to be tested every frame
        # self.traverser.showCollisions(render) # shows collision
        self.pusher = CollisionHandlerPusher()
        self.lifter = CollisionHandlerFloor()
        self.queue = CollisionHandlerQueue()
        self.cameraCollided = False

        # Generate objects
        self.terrain = Terrain(self, "modelMiyagi")
        self.terrainName = self.terrain.name
        self.player = Player(self)
        # self.water = Water(self)

    ################################################################
    # Data Helpers
    ################################################################

    def initializeFunctions(self):
        ShowBase.__init__(self) # initializes Panda window from ShowBase
        self.disableMouse() # disable camera control by mouse
        self.makeMouseRelative()
        self.keyPressed()
        self.timerFired()
        self.mouseActivity()
        # Set the background color to blue
        self.win.setClearColor((0.5, 0.8, 1, 1))
        # self.createLights()

    def makeMouseRelative(self):
        props = WindowProperties() # initates window node
        props.setCursorHidden(True) # hides cursor
        props.setMouseMode(WindowProperties.M_relative) # cursor stays
        self.win.requestProperties(props) # window accepts changes

    def createLights(self):
        # light settings
        # Sun
        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(VBase4(255, 255, 255, 1))
        self.dlnp = self.render.attachNewNode(self.dlight)
        self.dlnp.setHpr(0, -40, 0)
        self.render.setLight(self.dlnp)

        # Ambient
        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(1, 0, 0, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

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

    # debugging purposes
    def playerCollision(self, task):
        self.traverser.showCollisions(self.render)
        return Task.cont

    ################################################################
    # Event handlers
    ################################################################

    # responds to key press
    def keyPressed(self):
        self.accept("p", self.togglePause) # "p" key for pause
    
    # adds task that should be fired every second
    def timerFired(self):
        taskMgr.add(self.playerCollision, "player collision")

    def mouseActivity(self):
        pass

print ("starting app")
app = MyApp()
app.run()