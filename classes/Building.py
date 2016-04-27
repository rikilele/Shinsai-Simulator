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
        self.buildInfo = {\
        "house1"   :("models/house/house1/house1.egg", 180),
        "house2"   :("models/house/house2/house2.egg", 180),
        "house3"   :("models/house/house3/house3.egg", 180),
        "build"    :("models/build/build.egg",          80),
        "concrete" :("models/concrete/concrete.egg",   850),
        "r"        :("models/r/r.egg",                 150),
        "cafe"     :("models/cafe/cafe.egg",            40),
        "old"      :("models/oldbuild/oldbuild.egg",    30),
        "tower"    :("models/tower/tower.egg",          90)}
        self.filename = self.buildInfo[name][0]
        self.scale = self.buildInfo[name][1]
        self.build(scene)

    def build(self, scene):
        self.building = scene.loader.loadModel(self.filename)
        self.building.reparentTo(scene.render)
        self.building.setScale(self.scale)
        self.building.setHpr(90,0,0)
        self.building.setPos(self.posX, self.posY, self.posZ)
        self.building.setTwoSided(True)
