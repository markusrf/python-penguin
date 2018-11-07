import os
import json
import random
import math
import moveTowardsPowerup as powerups

import suddenDeath

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : RETREAT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : RETREAT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : RETREAT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : RETREAT,"left" : ADVANCE }

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)

def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction =  MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
    return plannedAction

def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

def enemyPosition(body):
    """Returnerer tuppel med x,y-koordinater hvis de eksisterer"""
    try:
        return body["enemies"][0]["x"], body["enemies"][0]["y"]
    except:
        return False

def powerMove(body):
    if powerups.canSeeHearts(body):
        move = powerups.moveTowardHeart(body)
    else:
        move = powerups.moveTowardPowerup(body)
    return moveTowardsPoint(move[0],move[1],move[2])


def chooseAction(body):
    action = PASS
    action = moveTowardsCenterOfMap(body)

    if body["suddenDeath"] < 1:
        action = suddenDeath.suddenDeathMove(body)
    return action

# env = os.environ
# req_params_query = env['REQ_PARAMS_QUERY']
# responseBody = open(env['res'], 'w')
#
# response = {}
# returnObject = {}
# if req_params_query == "info":
#     returnObject["name"] = "PiNgU"
#     returnObject["team"] = "Team Noot Noot"
# elif req_params_query == "command":
#     body = json.loads(open(env["req"], "r").read())
#     returnObject["command"] = chooseAction(body)
#
# response["body"] = returnObject
# responseBody.write(json.dumps(response))
# responseBody.close()
