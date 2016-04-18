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
        if (self.posZ > 0 or self.gravity < 0):
            self.posZ -= min (g, self.posZ) # to not go underground
            self.gravity += 1.0
        elif (self.posZ == 0):
            self.gravity = 1 # the value of the gravitational constant
        return Task.cont

    ################################################################
    # Helpers for keyPressed
    ################################################################

    def move(self, scene):
        if scene.paused == False:
            isDown = base.mouseWatcherNode.is_button_down
            magnitude = self.speed*self.health # speed depends on health
            radians = self.H * (pi/180)
            if isDown("w"): # forwards
                self.posX += magnitude*-sin(radians)
                self.posY += magnitude*cos(radians)
            elif isDown("s"): # backwards
                self.posX += magnitude*sin(radians)
                self.posY += magnitude*-cos(radians)
            elif isDown("a"): # left
                self.posX += magnitude*-cos(radians)*0.8 # side-step is slower
                self.posY += magnitude*-sin(radians)*0.8
            elif isDown("d"): # right
                self.posX += magnitude*cos(radians)*0.8
                self.posY += magnitude*sin(radians)*0.8
        return Task.cont

    def jump(self):
        # if self.posZ == 0:
        #     self.gravity = -10
        self.gravity = -10

    ################################################################
    # Helpers for mouseActivity
    ################################################################

    """Want to set maximum mouse (x, y)"""
    def lookAround(self, scene):
        # template taken from:
        # http://www.panda3d.org/manual/index.php/Mouse_Support
        if (scene.paused == False) and (scene.mouseWatcherNode.hasMouse()):
            self.mouseX = scene.mouseWatcherNode.getMouseX()
            self.mouseY = scene.mouseWatcherNode.getMouseY()
            modifier = 10 # convert x-unit to angle
            self.H = -(self.mouseX*modifier) # change H vision
            potentialP = self.mouseY*modifier
            if abs(potentialP) < 80: # vision is limited in z-axis
                self.P = potentialP
        return Task.cont

    ################################################################
    # Event handlers
    ################################################################

    # responds to key press
    def keyPressed(self, scene):
        taskMgr.add(self.move, "move with AWSD", extraArgs=[scene])
        scene.accept("space", self.jump)
    
    # adds task that should be fired every second
    def timerFired(self, scene):
        taskMgr.add(self.fall, "gravity manipulation")
        taskMgr.add(self.manageCam, "cam", extraArgs=[scene])

    def mouseActivity(self, scene):
        taskMgr.add(self.lookAround, "look Around", extraArgs=[scene])

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