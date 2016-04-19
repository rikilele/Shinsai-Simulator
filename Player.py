# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for calculations
from math import sin, cos, pi

# The player's information
class Player(ShowBase):
    def __init__(self, scene):
        self.health = 1 # between 0 to 1
        (self.posX, self.posY, self.posZ) = (0, -800, 500) # initial position
        (self.H, self.P, self.R) = (0, 0, 0) # initial HPR
        self.gravity = 1
        self.speed = 3 # depends on gender and age
        self.keyPressed(scene) # initiates function that runs on key press
        self.timerFired(scene) # initiates function that runs on timer
        self.mouseActivity(scene) # initiates function that runs on mouse
        self.initiateCollision(scene) # initiates collision area around player
        print ("initiated")

    def initiateCollision(self, scene):
        area = CollisionSphere(0, 0, 0, 0.5)
        playerNode = (scene.camera).attachNewNode(CollisionNode("cnode"))
        playerNode.node().addSolid(area)
        playerNode.show()

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