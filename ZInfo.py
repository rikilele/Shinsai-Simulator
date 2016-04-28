from database.Coordinates import Coordinates

class ZInfo(object):
    def __init__(self, name):
        if name == "yokohama.egg":
            myDictClass = Coordinates()
            oldDict = myDictClass.coords
            self.newDict = dict()
            for key in oldDict:
                coordX = key[0]
                coordY = key[1]
                zValue = myDictClass.coords[key]
                coordX = coordX//100*100
                coordY = coordY//100*100
                self.newDict[(coordX, coordY)] = int(zValue)
