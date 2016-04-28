"""
This is a terrain tracer for any maps that have been created to be rendered in
to the Shinsai-Simulator app. The purpose of this program is to get all Z-axis 
values for given (x, y) coordinates on the map. While this program is running,
a "laser" will be tracing the height for each coordinate of the map in a panda3d
window. Ideally, the tuple (x, y) will then become a "key" to the dictionary 
that maps the respective z-values obtained.
"""

# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for convenience
import sys

class MyApp(ShowBase):

    coordinates = dict()

    def __init__(self):
        ShowBase.__init__(self) # initializes Panda window from ShowBase
        self.path = "models/terrains/yokohama/yokohama.egg"
        self.terrain = self.loader.loadModel(self.path)
        self.scale = 450
        # Reparent the model to render.
        self.terrain.reparentTo(render)
        # Apply scale and position transforms on the model.
        self.terrain.setScale(self.scale)
        self.terrain.setPos(0, 0, 0)
        self.queue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser("main")
        base.cTrav = self.traverser
        (self.posX, self.posY, self.posZ) = (self.setPos())
        self.setWalkingRay()
        taskMgr.add(self.manageCam, "cam")

    def setPos(self):
        # set dimensions
        firstPoint = self.terrain.getTightBounds()[0]
        secondPoint = self.terrain.getTightBounds()[1]
        (x1, x2) = firstPoint.getX(), secondPoint.getX()
        (y1, y2) = firstPoint.getY(), secondPoint.getY()
        # set measurements
        self.origin = (max(x1, x2), max(y1, y2), 100) # tuple of origin
        self.minX = min(x1, x2)
        self.minY = min(y1, y2)
        return self.origin
    
    def setWalkingRay(self):    
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0, 0, 0)
        self.groundRay.setDirection(0, 0, -1)
        self.groundCol = CollisionNode("groudRay")
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(CollideMask.bit(20))
        self.groundCol.setIntoCollideMask(CollideMask.allOff())
        self.groundNodePath = (self.camera).attachNewNode(self.groundCol)
        (self.traverser).addCollider(self.groundNodePath, self.queue)
        self.groundNodePath.show()

    def trace(self):
        entries = list(self.queue.getEntries()) # set up the information
        # lambda function key to sort by highest displac value
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())
        if len(entries) > 0:
            for collision in entries:
                self.posZ = collision.getSurfacePoint(render).getZ() + 200
                MyApp.coordinates[(self.posX, self.posY)] = self.posZ - 200
                # 200 off-set so that we can check the process

    def manageCam(self, task):
        # update camera position
        self.camera.setPos(self.posX, self.posY, self.posZ)
        self.trace()
        if self.posX >= self.minX:
            self.posX -= 100
        else:
            print ("next")
            self.posX = self.origin[0]
            self.posY -= 100
            if self.posY <= self.minY:
                print MyApp.coordinates
        # Task.cont allows the function to keep running
        return Task.cont


app = MyApp()
app.run()
