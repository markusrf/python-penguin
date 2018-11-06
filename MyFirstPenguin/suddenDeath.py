import math

from eucDist import eucDistance as eucDist
from run import moveTowardsPoint

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
def suddenDeathMove(body):
    action = PASS

    # If no fire is sighted, run to the edge closes to you
    if len(body["fire"]) == 0:
        action = moveToClosestWall(body)
    # If fire is sighted, run away
    else:
        action = avoidFire(body)

    return action

def moveToClosestWall(body):
    action = PASS

    x = body["you"]["x"]
    y = body["you"]["y"]

    #Identify which wall is cloesest and move towards it
    closest = eucDist(body, x, 0)
    action = moveTowardsPoint(body, x, 0)

    if eucDist(body, x, body["mapHeight"]) < closest:
        action = moveTowardsPoint(body, x, body["mapHeight"])
        closest = eucDist(body, x, body["mapHeight"])
    if eucDist(body, 0, y) < closest:
        action = moveTowardsPoint(body, 0, y)
        closest = eucDist(body, 0, y)
    if eucDist(body, body["mapWidth"], y) < closest:
        action = moveTowardsPoint(body, body["mapWidth"], y)
        closest = eucDist(body, body["mapWidth"], y)
    
    return action

def avoidFire(body):
    action = PASS

    # identify closest fire
    closestFire = body["fire"][0]
    closestFireDistance = eucDist(body, closestFire["x"], closestFire["y"])
    for fire in body["fire"][1:]:
        closestFireDistance = eucDist(body, fire["x"], fire["y"])
        closestFire = fire
    
    # find distance
    distX = abs(body["you"]["x"] - closestFire["x"])
    distY = abs(body["you"]["y"] - closestFire["y"])

    # use distance to move oposite way
    # if closest in x direction, move away in the x axis
    if distX < distY:
        if body["you"]["x"] < closestFire["x"]:
            action = moveTowardsPoint(body, body["you"]["x"]-1, body["you"]["y"])
        else:
            action = moveTowardsPoint(body, body["you"]["x"]+1, body["you"]["y"])
    else:
        if body["you"]["y"] < closestFire["y"]:
            action = moveTowardsPoint(body, body["you"]["x"], body["you"]["y"]-1)
        else:
            action = moveTowardsPoint(body, body["you"]["x"], body["you"]["y"]+1)
        
    return action