# scene == the app's main window (self)
# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

class Building(ShowBase):
    def __init__(self, scene, name, posX, posY, posZ):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        if name == "concrete": self.buildConcrete(scene)
        elif name == "R": self.buildRBuilding(scene)
        elif name == "house1": self.buildHouse1(scene)
        elif name == "house2": self.buildHouse2(scene)
        elif name == "house3": self.buildHouse3(scene)
        elif name == "tower": self.buildTower(scene)
        elif name == "build": self.buildBuild(scene)

    def buildConcrete(self, scene):
        building = scene.loader.loadModel("models/concrete/concrete.egg")
        building.reparentTo(scene.render)
        building.setScale(850)
        building.setHpr(0,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()

    def buildRBuilding(self, scene):
        building = scene.loader.loadModel("models/r-building/r-building.egg")
        building.reparentTo(scene.render)
        building.setScale(850)
        building.setHpr(0,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.5, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()

    def buildHouse1(self, scene):
        building = scene.loader.loadModel("models/house/house1/house1.egg")
        building.reparentTo(scene.render)
        building.setScale(130)
        building.setHpr(90,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()

    def buildHouse2(self, scene):
        building = scene.loader.loadModel("models/house/house2/house2.egg")
        building.reparentTo(scene.render)
        building.setScale(130)
        building.setHpr(90,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()

    def buildHouse3(self, scene):
        building = scene.loader.loadModel("models/house/house3/house3.egg")
        building.reparentTo(scene.render)
        building.setScale(130)
        building.setHpr(90,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()
    
    def buildTower(self, scene):
        building = scene.loader.loadModel("models/tower/tower.egg")
        building.reparentTo(scene.render)
        building.setScale(100)
        building.setHpr(0,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()

    def buildBuild(self, scene):
        building = scene.loader.loadModel("models/build/build.egg")
        building.reparentTo(scene.render)
        building.setScale(80)
        building.setHpr(0,0,0)
        building.setPos(self.posX, self.posY, self.posZ)
        # initiate collison settings
        box = CollisionBox(Point3(0.7, 0, 1), 1, 1, 1.25)
        cnodePath = building.attachNewNode(CollisionNode('box'))
        cnodePath.node().addSolid(box)
        cnodePath.show()