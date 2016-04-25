# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for calculations
from math import sin, cos, pi

# The player's information
# scene is the app's main window (self)

class Player(ShowBase):
    def __init__(self, scene, posX, posY):
        self.health = 1 # between 0 to 1
        (self.posX, self.posY, self.posZ) = (posX, posY, 100) # initial position
        (self.H, self.P, self.R) = (0, 0, 0) # initial HPR
        self.gravity = 1
        self.speed = 200 # depends on gender and age
        self.keyPressed(scene) # initiates function that runs on key press
        self.timerFired(scene) # initiates function that runs on timer
        self.mouseActivity(scene) # initiates function that runs on mouse
        self.initiateCollision(scene) # initiates collision nodes

    def initiateCollision(self, scene):
        self.setCollisionArea(scene)
        self.setWalkingRay(scene)
        
    def setCollisionArea(self, scene):
        self.barrier = CollisionSphere(0, 0, 0, 120)
        self.playerNodeP = (scene.camera).attachNewNode(CollisionNode('barrier'))
        self.playerNodeP.node().addSolid(self.barrier)
        # add to traverser
        (scene.traverser).addCollider(self.playerNodeP ,scene.queue)

    def setWalkingRay(self, scene):    
        # for walkingon  terrain
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0, 0, 0)
        self.groundRay.setDirection(0, 0, -1)
        self.groundCol = CollisionNode('groundRay')
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(CollideMask.bit(20))
        self.groundCol.setIntoCollideMask(CollideMask.allOff())
        self.groundNodePath = (scene.camera).attachNewNode(self.groundCol)
        (scene.traverser).addCollider(self.groundNodePath, scene.queue)

    ################################################################
    # Helpers for timerFired
    ################################################################

    # manages camera settings depending on data
    def manageCam(self, scene):
        # update camera position
        scene.camera.setPos(self.posX, self.posY, self.posZ)
        scene.camera.setHpr(self.H, self.P, self.R)
        print self.posX, self.posY, self.posZ
        # Task.cont allows the function to keep running
        return Task.cont

    def followTerrain(self, scene, collision):
        height = collision.getSurfacePoint(scene.render).getZ()
        self.posZ = height+50

    def preventBump(self, scene, collision):
        # newX = collision.getSurfacePoint(scene.render).getX()
        # newY = collision.getSurfacePoint(scene.render).getX()
        # self.posX, self.posY = newX, newY
        pass

    # iterates through every collision to take care of
    def exploreMap(self, scene):
        # set up the information
        entries = list(scene.queue.getEntries())
        # lambda function sorts by highest displac value
        entries.sort(key=lambda x: x.getSurfacePoint(scene.render).getZ())
        if len(entries) > 0:
            for collision in entries:
                player = str(collision.getFromNodePath())
                into = str(collision.getIntoNodePath())
                # print (player)
                # print ("colliding with " + into)
                # checks to see if it's colliding with terrain
                if scene.terrainName in into:
                    self.followTerrain(scene, collision)
                elif "box" in into:
                    self.preventBump(scene, collision)
        return Task.cont

    ################################################################
    # Helpers for keyPressed
    ################################################################

    ''' Temporary Solution.
        A Bug exists in being able to bipass the building'''
    
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
    
    # adds task that should be fired every frame
    def timerFired(self, scene):
        taskMgr.add(self.exploreMap, "move in map", extraArgs=[scene])
        taskMgr.add(self.manageCam, "cam", extraArgs=[scene])

    def mouseActivity(self, scene):
        taskMgr.add(self.lookAround, "look Around", extraArgs=[scene])