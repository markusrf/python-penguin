import math

def eucDistance(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]

    return math.sqrt((penguinPositionX-pointX)**2 + (penguinPositionY-pointY)**2)