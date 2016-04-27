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
            self.loadWaves(scene)
            self.startSimulation(scene)
            return Task.done
        return Task.cont

    def loadWaves(self, scene):
        self.wave = scene.loader.loadModel("models/water/waves.egg")
        # Reparent the model to render.
        self.wave.reparentTo(scene.render)
        self.wave.setTwoSided(True) # water visible from inside
        # Apply scale and position transforms on the model.
        self.wave.setScale(scene.scale+100) # so Tsunami wraps terrain
        self.wave.setSz(scene.scale-100)

    def startSimulation(self, scene):
        startPos = (0, scene.length*2, scene.minZ-scene.height)
        self.wave.setPos(Point3(startPos))
        middlePos = (0, scene.length*1.5, 
            scene.minZ - scene.height*0.7 + scene.maxZ*(scene.magnitude)/100)
        endPos = (0, 0, 
            scene.minZ - scene.height*0.7 + scene.maxZ*(scene.magnitude)/100)
        bringTsunami = self.wave.posInterval(2,
                                              Point3(middlePos),
                                              Point3(startPos))
        hitTsunami = self.wave.posInterval(2, 
                                            Point3(endPos), 
                                            Point3(middlePos))
        # Create and play the sequence that coordinates the intervals.
        simulation = Sequence(bringTsunami, hitTsunami, name="simulation")
        simulation.start()
        print ("released Tsunami")
