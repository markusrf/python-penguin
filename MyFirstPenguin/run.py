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

TURNS = {
    "top":{
        "top":0,
        "left":-1,
        "right":1,
        "bottom":2
    }, "left":{
        "left":0,
        "bottom":-1,
        "top":1,
        "right":2
    }, "bottom":{
        "bottom":0,
        "left":1,
        "right":-1,
        "top":2
    }, "right":{
        "right":0,
        "top":-1,
        "bottom":1,
        "left":2
    }}

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

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

def enemyDirectionRelative(body, enemyPos):
    """Returnerer fiendens retning relativt til deg"""
    position = body["you"]["x"], body["you"]["y"]
    if enemyPos[0] < position[0]:
        return "left"
    elif enemyPos[0] > position[0]:
        return "right"
    elif enemyPos[1] < position[1]:
        return "top"
    else:
        return "bottom"

def enemyStraightAhead(body):
    """Returnerer true om fienden er rett foran deg"""
    enemyPos = enemyPosition(body)
    position = body["you"]["x"], body["you"]["y"]
    direction = body["you"]["direction"]

    if direction == "top":
        return enemyPos[1] < position[1]
    elif direction == "bottom":
        return enemyPos[1] > position[1]
    elif direction == "left":
        return enemyPos[0] < position[0]
    elif direction == "right":
        return enemyPos[0] > position[0]
    else:
        return False

def ableToWin(body, enemyPos):
    """Returnerer true om du har mulighet for aa vinne en skyteduell"""
    enemyRelDir = enemyDirectionRelative(body, enemyPos)
    enemyHealth = body["enemies"][0]["strength"]
    enemyDamage = body["enemies"][0]["weaponDamage"]
    direction = body["you"]["direction"]
    health = body["you"]["strength"]
    weaponDamage = body["you"]["weaponDamage"]
    turns = TURNS[direction][enemyRelDir]

    return enemyHealth // weaponDamage <= (health - abs(turns)*enemyDamage) // enemyDamage

def turnToShoot(body, enemyPos):
    direction = body["you"]["direction"]
    enemyRelDir = enemyDirectionRelative(body, enemyPos)
    turns = TURNS[direction][enemyRelDir]

    if turns == 0:
        return SHOOT
    elif turns == -1:
        return ROTATE_LEFT
    elif turns == 1 or turns == 2:
        return ROTATE_RIGHT

def powerMove(body):
    if powerups.canSeeHearts(body):
        move = powerups.moveTowardHeart(body)
    else:
        move = powerups.moveTowardPowerup(body)
    return moveTowardsPoint(move[0],move[1],move[2])

def chooseAction(body):
    enemyPos = enemyPosition(body)
    if body["suddenDeath"] < 1:
        action = suddenDeath.suddenDeathMove(body)
    elif enemyStraightAhead(body):
        if ableToWin(body, enemyPos):
            action = turnToShoot(body, enemyPos)
        else:
            action = retreat_from_enemy(body)
    elif body["status"] == "hit" and enemyPos:
        if ableToWin(body, enemyPos):
            action = turnToShoot(body, enemyPos)
        else:
            action = retreat_from_enemy(body)
    else:
        action = moveTowardsCenterOfMap(body)

    return action

  
if __name__=="__main__":
    env = os.environ
    req_params_query = env['REQ_PARAMS_QUERY']
    responseBody = open(env['res'], 'w')

    response = {}
    returnObject = {}
    if req_params_query == "info":
        returnObject["name"] = "PiNgU"
        returnObject["team"] = "Team Noot Noot"
    elif req_params_query == "command":
        body = json.loads(open(env["req"], "r").read())
        returnObject["command"] = chooseAction(body)

    response["body"] = returnObject
    responseBody.write(json.dumps(response))
    responseBody.close()
