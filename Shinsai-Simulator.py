# TP3
# Riki Singh Khorana + rkhorana + MM

# importing panda3d modules and classes
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import *
from pandac.PandaModules import WindowProperties

# importing modules for convenience
import sys

# import classes written by myself on separate files
from classes.Player import Player
from classes.Terrain import Terrain
from classes.Water import Water

class MyApp(ShowBase):

    paused = False
    inTsunami = False
    isOver = False
    number = 1

    def __init__(self):
        ShowBase.__init__(self) # initializes Panda window from ShowBase
        # change window name from "panda" to app name
        properties = WindowProperties()
        properties.setTitle("Shinsai-Simulator")
        base.win.requestProperties(properties)
        # adds algorithm to render closer objects first
        binManager = CullBinManager.getGlobalPtr()
        binManager.addBin("ftb", CullBinManager.BTFrontToBack, 1)
        base.setFrameRateMeter(True)
        self.tName = None # name of terrain
        self.magnitude = None # magnitude of earthquake
        self.titleScreen()

    ################################################################
    # Menu Screen functions
    ################################################################

    # this is the buffer for all screen in the menu
    def moveScreens(self, name):
            # removes all menu elements
            if name=="start":
                globalClock.reset()
                self.initSimulation()
            elif name=="help":
                self.helpScreen()
            elif name=="title":
                self.titleScreen()
            elif name=="select":
                self.selectScreen()

    # this is the main title screen
    def titleScreen(self):
        def moveOn(name):
            for element in screen:
                element.destroy()
            self.moveScreens(name)
        self.win.setClearColor((0, 0, 0, 1)) # makes background black
        image = OnscreenImage(image="images/title.png", pos=(0, 0, 0), 
                              scale=(1.3,1,1.1))
        start = DirectButton(text = ("Continue to simulation"), command=moveOn,
                             scale=0.08, pos=LVecBase3f(0,0,-0.1), 
                             extraArgs=["select"])
        helper = DirectButton(text = ("Help"), command=moveOn,
                              scale=0.08, pos=LVecBase3f(0,0,-0.3), 
                              extraArgs=["help"])
        screen = [image, start, helper]

    # this screen will allow you to select the situation
    def selectScreen(self):
        def chooseMagnitude(): self.magnitude = slider["value"]*17
        def moveOn(name):
            for element in screen: element.destroy()
            self.moveScreens(name)
        image = OnscreenImage(image="images/select.png", pos=(0, 0, 0), 
                              scale=(1.3,1,1.1))
        menu = DirectOptionMenu(text="Model City", scale=0.08,
                                items=["Yokohama"], command=self.chooseCity, 
                                pos=(-0.2, 0, -0.08))
        startButton = DirectButton(text = ("Start Simulation"), command=moveOn,
                                   scale=0.08, pos=LVecBase3f(0,0,-0.7), 
                                   extraArgs=["start"])
        backButton = DirectButton(text = ("Title"), command=moveOn,
                                  scale=0.08, pos=LVecBase3f(-0.8,0,-0.7), 
                                  extraArgs=["title"])
        helpButton = DirectButton(text = ("Help"), command=moveOn,
                                  scale=0.08, pos=LVecBase3f(0.8,0,-0.7), 
                                  extraArgs=["help"])
        slider = DirectSlider(range=(6,7), value=6.5, pageSize=0.1, scale=0.3,
                              pos=(0, 0, -0.4),command=chooseMagnitude)
        screen = [image, menu, startButton, helpButton, backButton, slider]

    # contains information for help
    def helpScreen(self):
        def moveOn(name):
            for element in screen:
                element.destroy()
            self.moveScreens(name)
        image = OnscreenImage(image="images/help.png", 
                              pos=(0, 0, -0.15), scale=(1.3,1,1.2))
        backButton = DirectButton(text = ("Title"), command=moveOn, scale=0.07, 
                                  pos=LVecBase3f(-0.5,0,-0.93), 
                                  extraArgs=["title"])
        continueButton = DirectButton(text = ("Continue to simulation"), 
                                      command=moveOn, scale=0.07, 
                                      pos=LVecBase3f(0.2,0,-0.93), 
                                      extraArgs=["select"])
        screen = [image, backButton, continueButton]

    def chooseCity(self, arg): 
        self.tName = arg.lower()

    ################################################################
    # Real Init Function
    ################################################################

    def initSimulation(self):
        self.initializeFunctions()
        # Initialize collision handlers
        self.initializeCollision()
        # Generate terrain information
        self.initializeScene()
        # Generate interactive objects
        self.player = Player(self, self.posX, self.posY)
        self.tsunamiTime = 30
        self.tsunami = Water(self)
        # Initialize screen on text
        self.put2D()

    ################################################################
    # Data Helpers
    ################################################################

    def initializeFunctions(self):
        self.disableMouse() # disable camera control by mouse
        self.makeMouseRelative()
        self.keyPressed()
        self.timerFired()
        self.mouseActivity()
        # Set the background color to blue
        self.win.setClearColor((0.45, 0.75, 1, 1))

    def put2D(self):
        # This code was taken and adapted from samples/ball-in-maze.py
        self.instructions = \
            OnscreenText(text="Use WASD keys to move \
                             \nUse mouse to look around\
                             \nPress P to enable mouse outside window",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06)
        # Place compass on screen to navigate
        self.compassCircle = OnscreenImage(image="images/compass.png", 
                                           pos=(-1.05, 0, -0.74), scale=0.17)
        self.compassCircle.setTransparency(TransparencyAttrib.MAlpha)
        self.compassCircle.setAlphaScale(0.5)
        self.compass = self.loader.loadModel("models/compass/pointer.egg")
        self.compass.setScale(0.027)
        self.compass.setPos(-2.8, 10, -2)
        self.compass.reparentTo(self.camera)

    def initializeCollision(self):
        self.traverser = CollisionTraverser("main")
        base.cTrav = self.traverser # allows collision to be tested every frame
        self.queue = CollisionHandlerQueue()

    def initializeScene(self):
        if self.tName == None: self.tName = "yokohama" # initialize
        self.terrain = Terrain(self, self.tName) # insert the filename you want
        self.terrainName = self.terrain.name
        (self.posX, self.posY) = self.terrain.origin
        (self.length, self.width, self.height) = (self.terrain.dimensions)
        (self.maxZ, self.minZ) = self.terrain.maxZ, self.terrain.minZ
        self.scale = self.terrain.scale

    def makeMouseRelative(self):
        props = WindowProperties() # initates window node
        props.setCursorHidden(True) # hides cursor
        props.setMouseMode(WindowProperties.M_relative) # cursor stays
        self.win.requestProperties(props) # window accepts changes

    ################################################################
    # Helpers for keyPressed
    ################################################################

    # press P to enable mouse control outside of window
    def togglePause(self):
        print ("pause pressed")
        if MyApp.paused:
            self.makeMouseRelative()
            MyApp.paused = False
        else:
            props = WindowProperties() # initiates window node
            props.setCursorHidden(False) # cursor shows
            props.setMouseMode(WindowProperties.M_absolute) # cursor moves
            self.win.requestProperties(props) # window accepts changes
            MyApp.paused = True

    ################################################################
    # Helpers for timerFired
    ################################################################

    # debugging purposes
    def playerCollision(self, task):
        # self.traverser.showCollisions(self.render)
        return Task.cont

    # checks for the time of the tsunami
    def checkTime(self, task):
        if (MyApp.isOver): return Task.done # end task if simulations is over
        frameTime = globalClock.getFrameTime()
        if frameTime > self.tsunamiTime:
            MyApp.inTsunami = True
        return Task.cont

    # display timer, health bar, and underwater effect 
    def displayData(self, task):
        if (MyApp.isOver): return Task.done # end task if simulations is over
        time = globalClock.getFrameTime()
        try: 
            self.timeClock.destroy()
            self.healthBar.destroy()
            self.waterEffect.destroy()
        except: pass
        color = (1,1,1,1) if MyApp.inTsunami == False else (1,0,0,1)
        self.timeClock = \
        OnscreenText(text="%d:%d%d" % (time//60, time//1%60//10,time//1%60%10),
                    parent=base.a2dBottomRight, align=TextNode.ARight, fg=color, 
                    pos=(-0.2, 0.22), scale=0.15, shadow=(0, 0, 0, 1))  
        self.healthBar = DirectWaitBar(text="Health", value=self.player.health, 
                                       scale=0.6, pos=(0,.4,-0.74), range=1)
        if self.player.submerged == True:
            self.waterEffect = \
            OnscreenImage(image="images/undersea.jpg", pos=(0, 0, 0), scale=2)
            self.waterEffect.setTransparency(TransparencyAttrib.MAlpha)
            self.waterEffect.setAlphaScale(1-(self.player.health*0.6))
        return Task.cont

    def watchEnd(self, task):
        if self.player.health <= 0:
            MyApp.isOver = True
            self.message = \
                OnscreenText(text="Simulation is done.",
                             pos=(0, 0), fg=(1, 1, 1, 1), scale=0.2)
            self.nextInstructions = \
                OnscreenText(text="Press Escape to exit",
                             pos=(0, -0.3), fg=(1, 1, 1, 1), scale=0.2)
            self.accept("escape", self.moveOut)
            return Task.done
        return Task.cont

    ################################################################
    # Event handlers
    ################################################################

    # responds to key press
    def keyPressed(self):
        self.accept("p", self.togglePause) # "p" key for pause
    
    # adds task that should be fired every second
    def timerFired(self):
        taskMgr.add(self.playerCollision, "player collision")
        taskMgr.add(self.checkTime, "time")
        taskMgr.add(self.displayData, "player data")
        taskMgr.add(self.watchEnd, "simulation end")

    def mouseActivity(self):
        pass

    def moveOut(self):
        sys.exit()

print ("starting app")
app = MyApp()
app.run()
