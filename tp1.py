# Initial TP1
# Riki Singh Khorana + rkhorana + MM

from math import sin, cos, pi
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from pandac.PandaModules import WindowProperties

""" No LOD for terrain, but buildings and water definitely """

# The player's information
class Player(ShowBase):

    def __init__(self, scene):
        assert (isinstance(scene, MyApp))
        self.health = 1 # between 0 to 1
        (self.posX, self.posY, self.posZ) = (0, -800, 500) # initial position
        (self.H, self.P, self.R) = (0, 0, 0) # initial HPR
        self.gravity = 1
        self.speed = 3 # depends on gender and age
        self.keyPressed(scene) # initiates function that runs on key press
        self.timerFired(scene) # initiates function that runs on timer
        self.mouseActivity(scene) # initiates function that runs on mouse
        print ("initiated")

    ################################################################
    # Helpers for timerFired
    ################################################################

    # manages camera settings depending on data
    def manageCam(self, scene):
        # update camera position
        scene.camera.setPos(self.posX, self.posY, self.posZ)
        scene.camera.setHpr(self.H, self.P, self.R)
        # Task.cont allows the function to keep running
        return Task.cont

    # applies gravity to player, also camera
    def fall(self, task):
        g = self.gravity
        if (self.posZ > 0):
            self.posZ -= g
            self.gravity += 1.0
        if (self.posZ == 0):
            self.gravity = 1 # the value of the gravitational constant
        return Task.cont

    ################################################################
    # Helpers for keyPressed
    ################################################################

    def move(self, scene, direction):
        if scene.paused == False:
            magnitude = self.speed*self.health # speed depends on health
            angleRadians = self.H * (pi/180)
            if direction == "front":
                self.posX += magnitude*-sin(angleRadians)
                self.posY += magnitude*cos(angleRadians)
            elif direction == "back":
                self.posX += magnitude*sin(angleRadians)
                self.posY += magnitude*-cos(angleRadians)
            elif direction == "left":
                self.posX += magnitude*-cos(angleRadians)
                self.posY += magnitude*-sin(angleRadians)
            elif direction == "right":
                self.posX += magnitude*cos(angleRadians)
                self.posY += magnitude*sin(angleRadians)

    ################################################################
    # Helpers for mouseActivity
    ################################################################

    def lookAround(self, scene):
        # template taken from:
        # http://www.panda3d.org/manual/index.php/Mouse_Support
        if (scene.paused == False) and (scene.mouseWatcherNode.hasMouse()):
            self.mouseX = scene.mouseWatcherNode.getMouseX()
            self.mouseY = scene.mouseWatcherNode.getMouseY()
            self.H = -(self.mouseX*10)
            if abs(self.mouseY*10 < 90): # vision is limited in z-axis
                self.P = self.mouseY*10
        return Task.cont

    ################################################################
    # Event handlers
    ################################################################

    # responds to key press
    def keyPressed(self, scene):
        scene.accept("w", self.move, [scene, "front"])
        scene.accept("w-repeat", self.move, [scene, "front"])
        scene.accept("s", self.move, [scene, "back"])
        scene.accept("s-repeat", self.move, [scene, "back"])
        scene.accept("a", self.move, [scene, "left"])
        scene.accept("a-repeat", self.move, [scene, "left"])
        scene.accept("d", self.move, [scene, "right"])
        scene.accept("d-repeat", self.move, [scene, "right"])
    
    # adds task that should be fired every second
    def timerFired(self, scene):
        taskMgr.add(self.fall, "gravity manipulation")
        taskMgr.add(self.manageCam, "cam", extraArgs=[scene])

    def mouseActivity(self, scene):
        taskMgr.add(self.lookAround, "look Around", extraArgs=[scene])

# used only to load city terrain specified by user
class Terrain(ShowBase):
    def __init__(self, scene):
        self.terrain = scene.loader.loadModel("models/fuji.egg")
        self.terrain.reparentTo(scene.render)
        self.terrain.setScale(0.4)
        self.terrain.setHpr(0,0,0)
        self.terrain.setPos(0, 0, 0)

        self.bamboo = scene.loader.loadModel("environment")
        # Reparent the model to render.
        self.bamboo.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.bamboo.setScale(1)
        self.bamboo.setPos(0, 0, -40)

class Building(ShowBase):
    pass
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
        self.accept("p", self.togglePause)
        
        # Generate objects
        self.terrain = Terrain(self)
        self.player = Player(self)

    def makeMouseRelative(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)

    def togglePause(self):
        print ("pause pressed")
        if MyApp.paused:
            self.makeMouseRelative()
            MyApp.paused = False
        else:
            props = WindowProperties()
            props.setCursorHidden(False)
            props.setMouseMode(WindowProperties.M_absolute)
            self.win.requestProperties(props)
            MyApp.paused = True

print ("starting app")
app = MyApp()
app.run()