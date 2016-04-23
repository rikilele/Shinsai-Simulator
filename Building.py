# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# scene == the app's main window (self)

class Building(ShowBase):
    def __init__(self, scene, name):
        if name == "concrete":
            self.buildConcrete(scene)
        elif name == "R":
            self.buildRBuilding(scene)
        elif name == "house":
            self.buildHouse(scene)

    def buildConcrete(self, scene):
        for i in range(4):
            building = scene.loader.loadModel("models/concrete/concrete.egg")
            building.reparentTo(scene.render)
            building.setScale(100)
            building.setHpr(0,0,0)
            building.setPos(i*500, 0, -150)

            # initiate collison settings
            box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
            cnodePath = building.attachNewNode(CollisionNode('box'))
            cnodePath.node().addSolid(box)
            cnodePath.show()

    def buildRBuilding(self, scene):
        for i in range(4):
            building = scene.loader.loadModel("models/r-building/r-building.egg")
            building.reparentTo(scene.render)
            building.setScale(100)
            building.setHpr(0,0,0)
            building.setPos(i*500, -400, -150)

            # initiate collison settings
            box = CollisionBox(Point3(0.5, 0, 1), 1, 1, 1.25)
            cnodePath = building.attachNewNode(CollisionNode('box'))
            cnodePath.node().addSolid(box)
            cnodePath.show()

    def buildHouse(self, scene):
        pass