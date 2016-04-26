# scene == the app's main window (self)
# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from pandac.PandaModules import WindowProperties

"""
all objects rendered into the scene as part of the Tsunami must have the name
"water" in it, so that the collision manager can detect the collision
"""

class Water(ShowBase):
    def __init__(self, scene):
        # checks the time so tha the Tsunami can run after a given time
        taskMgr.add(self.checkTime, "checkTime", extraArgs=[scene])

    def checkTime(self, scene):
        if scene.inTsunami == True:
            self.startSimulation(scene)
            return Task.done
        return Task.cont

    def startSimulation(self, scene):
        self.water = scene.loader.loadModel("models/water/waves.egg")
        # Reparent the model to render.
        self.water.reparentTo(scene.render)
        self.water.setTwoSided(True) # water visible from inside
        # Apply scale and position transforms on the model.
        self.water.setScale(scene.scale+100) # so Tsunami wraps
        self.water.setSz(scene.scale-100)
        startPos = (0, scene.length*2, scene.minZ-scene.height)
        self.water.setPos(Point3(startPos))
        middlePos = (0, scene.length*1.5, 
            scene.minZ - scene.height*0.7 + scene.maxZ*(scene.magnitude)/90)
        endPos = (0, 0, 
            scene.minZ - scene.height*0.7 + scene.maxZ*(scene.magnitude)/90)
        bringTsunami = self.water.posInterval(2,
                                              Point3(middlePos),
                                              Point3(startPos))
        hitTsunami = self.water.posInterval(2, 
                                            Point3(endPos), 
                                            Point3(middlePos))
 
        # Create and play the sequence that coordinates the intervals.
        simulation = Sequence(bringTsunami, hitTsunami, name="simulation")
        simulation.start()
        print ("released Tsunami")