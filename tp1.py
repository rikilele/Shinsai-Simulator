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

        # Keep objects in list
        self.objects = [self.player, self.building1, self.building2]

        # list of objects that collide
        self.pusher = CollisionHandlerPusher()
        self.traverser = CollisionTraverser("main")
        base.cTrav = self.traverser # allows collision to be tested every frame
        self.readObjects()
        
        smiley = loader.loadModel('smiley.egg')
        fromObject = smiley.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionSphere(0, 0, 0, 1))
        smiley.reparentTo(self.render)
        smiley.setScale(30)
        smiley.setPos(0, -1000, 0)
         
        # self.pusher.addCollider(fromObject, smiley)
        # self.traverser.addCollider(fromObject, self.pusher)

    # for collision detection
    def readObjects(self):
        for entity in self.objects:
            try:
                for information in entity.collidable:
                    (fromObject, obj) = information
                    (self.pusher).addCollider(fromObject, obj)
                    (self.traverser).addCollider(fromObject, self.pusher)
                    print ("added in pusher!")
            except:
                print ("didn't add pusher")

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