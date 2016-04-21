# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import *
from pandac.PandaModules import WindowProperties

class Water(ShowBase):
    def __init__(self, scene):
        # for i in range(100):
        #     for j in range(100):
        #         self.water = scene.loader.loadModel("models/water/water.egg")
        #         # Reparent the model to render.
        #         self.water.reparentTo(scene.render)
        #         # Apply scale and position transforms on the model.
        #         self.water.setScale(2)
        #         self.water.setPos(i*50, j*50, -40)
        self.water = scene.loader.loadModel("models/water/water.egg")
        # Reparent the model to render.
        self.water.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.water.setScale(1000)
        self.startPos = (0, 0, -1000)
        self.water.setPos(Point3(self.startPos))
        self.magnitude = 100 # the size of earthquake
        self.startSimulation(scene, self.magnitude)

    def startSimulation(self, scene, magnitude):
        endPos = (0, 0, self.magnitude)
        animation = self.water.posInterval(6, 
                                            Point3(endPos), 
                                            startPos=Point3(self.startPos))
 
        # Create and play the sequence that coordinates the intervals.
        simulation = Sequence(animation, name="simulation")
        simulation.loop()
        print ("ended Tsunami")