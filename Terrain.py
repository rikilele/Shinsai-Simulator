# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import *
from pandac.PandaModules import WindowProperties

class Terrain(ShowBase):
    def __init__(self, scene, name):

        self.name = name + ".egg"
        self.terrain = scene.loader.loadModel("models/terrains/"+self.name)
        # Reparent the model to render.
        self.terrain.reparentTo(scene.render)
        # Apply scale and position transforms on the model.
        self.terrain.setScale(200)
        self.terrain.setPos(0, 0, -40)
