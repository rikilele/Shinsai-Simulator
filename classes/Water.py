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
        self.water = scene.loader.loadModel("models/water/water.egg")
        # Reparent the model to render.
        self.water.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.water.setScale(1000)
        self.startPos = (1000, 1000, 100)
        self.water.setPos(Point3(self.startPos))
        self.magnitude = 100 # the size of earthquake
        self.startSimulation(scene, self.magnitude)

    def startSimulation(self, scene, magnitude):
        endPos = (0, 0, self.magnitude)
        animation = self.water.posInterval(15, 
                                            Point3(endPos), 
                                            startPos=Point3(self.startPos))
 
        # Create and play the sequence that coordinates the intervals.
        simulation = Sequence(animation, name="simulation")
        simulation.loop()
        print ("ended Tsunami")