# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for calculations
from math import sin, cos, pi
import random

# The player's information
# scene is the app's main window (self)

class Player(ShowBase):
    def __init__(self, scene, posX, posY):
        self.health = 1 # between 0 to 1
        (self.posX, self.posY, self.posZ) = (posX, posY, -100)
        (self.H, self.P, self.R) = (0, 0, 0) # initial HPR
        self.speed = 6000 # depends on gender and age
        self.submerged = False
        self.keyPressed(scene) # initiates functions that runs on key press
        self.timerFired(scene) # initiates functions that runs on timer
        self.mouseActivity(scene) # initiates functions that runs on mouse
        self.initiateCollision(scene)

    # initiates the collision settings so player can walk on map
    def initiateCollision(self, scene):
        self.setCollisionArea(scene)
        self.setWalkingRay(scene)
    
    # adds barrier to collide with buildings
    def setCollisionArea(self, scene):
        self.barrier = CollisionSphere(0, 0, 0, 120)
        self.playerNP = (scene.camera).attachNewNode(CollisionNode('barrier'))
        self.playerNP.node().addSolid(self.barrier)
        self.playerNP.node().setIntoCollideMask(CollideMask.allOff())
        # add to traverser
        (scene.traverser).addCollider(self.playerNP ,scene.queue)

    # adds ray that points up & down to detect collisions with terrain/water
    def setWalkingRay(self, scene):    
        self.groundRay, self.skyRay = CollisionRay(), CollisionRay()
        self.groundRay.setOrigin(0, 0, 0)
        self.skyRay.setOrigin(0, 0, 0)
        self.groundRay.setDirection(0, 0, -1)
        self.skyRay.setDirection(0, 0, 1)
        self.groundCol = CollisionNode("groudRay")
        self.groundCol.addSolid(self.groundRay)
        self.skyCol = CollisionNode("skyRay")
        self.skyCol.addSolid(self.skyRay)
        self.groundCol.setFromCollideMask(CollideMask.bit(20))
        self.groundCol.setIntoCollideMask(CollideMask.allOff())
        self.skyCol.setFromCollideMask(CollideMask.bit(20))
        self.skyCol.setIntoCollideMask(CollideMask.allOff())
        self.groundNodePath = (scene.camera).attachNewNode(self.groundCol)
        self.skyNodePath = (scene.camera).attachNewNode(self.skyCol)
        (scene.traverser).addCollider(self.groundNodePath, scene.queue)
        (scene.traverser).addCollider(self.skyNodePath, scene.queue)

    ################################################################
    # Helpers for timerFired
    ################################################################

    # manages camera settings depending on data
    def manageCam(self, scene):
        # update camera position
        scene.camera.setPos(self.posX, self.posY, self.posZ)
        scene.camera.setHpr(self.H, self.P, self.R)
        scene.compass.lookAt(scene.terrain.north.building)
        # Task.cont allows the function to keep running
        return Task.cont

    def followTerrain(self, scene, collision):
        height = collision.getSurfacePoint(scene.render).getZ()
        self.posZ = height+300

    def caughtInTsunami(self, scene):
        self.health -= 0.001
        # displace player due to water
        jerk = random.randint(1,int(scene.magnitude/10))
        if bool(random.getrandbits(1)): # randomly assign True of False
            self.posY -= jerk
        elif bool(random.getrandbits(1)):
            self.posX += jerk*3
        else:    
            self.posX -= jerk*3

    # iterates through every collision to take care of
    def exploreMap(self, scene):
        entries = list(scene.queue.getEntries()) # set up the information
        # lambda function key to sort by highest displac value
        entries.sort(key=lambda x: x.getSurfacePoint(scene.render).getZ())
        if len(entries) > 0:
            for collision in entries:
                player = str(collision.getFromNodePath())
                into = str(collision.getIntoNodePath())
                if scene.terrainName in into:
                    self.followTerrain(scene, collision)
                    self.submerged = False
                elif (scene.inTsunami == True and 
                      "waves" in into and "skyRay" in player):
                    self.submerged = True
                    self.caughtInTsunami(scene)
        else: self.submerged = False
        return Task.cont

    ################################################################
    # Helpers for keyPressed
    ################################################################
    
    def move(self, scene):
        if scene.paused == False:
            isDown = base.mouseWatcherNode.is_button_down
            # speed depends on health and frame rate
            frameRate = globalClock.getNetFrameRate()
            magnitude = self.speed*self.health*(1/frameRate)
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