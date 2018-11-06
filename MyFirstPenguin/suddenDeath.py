import math

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

# Run to the edge of the map when sudden death mode is on
# TODO: Add safe run, avoid enemy fire when moving
def suddenDeathMode(body):
    action = PASS

    # If no fire is sighted, run to the edge closes to you
    if len(body["fire"]) == 0:
        action = moveToClosestWall(body)
    # If fire is sighted, run away
    else:
        pass 

    return action

def moveToClosestWall(body):
    action = PASS

    x = body["you"]["x"]
    y = body["you"]["y"]

    #find closest wall
    top = eucDistance(body, x, 0)
    bottom = eucDistance(body, x, body["mapHeight"])
    left = eucDistance(body, 0, y)
    right = eucDistance(body, body["mapWidth"], y)

    

    return action


def eucDistance(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]

    return math.sqrt((penguinPositionX-pointX)**2 + (penguinPositionY-pointY)**2)