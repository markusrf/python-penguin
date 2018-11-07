import os
import json
import random
import math
from utils import *
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

ROTATE_LEFT_DIR = {"top": 'left', "bottom": 'right', "right": 'top', "left": 'bottom'}
ROTATE_RIGHT_DIR = {"top": 'right', "bottom": 'left', "right": 'bottom', "left": 'top'}

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def doesCellContainBonus(bonuses, x, y):
    for b in bonuses:
        if b["x"] == x and b["y"] == y:
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

def bonusInFrontOfPenguin(body):
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
    return doesCellContainBonus(body["bonusTiles"], xValueToCheckForWall, yValueToCheckForWall)

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


def retreat_from_enemy(body):
    enemy = body['enemies'][0]
    you = body['you']
    ex, ey, edir = enemy['x'], enemy['y'], enemy['direction']
    px, py, pdir = you['x'], you['y'], you['direction']
    epos = enemyDirectionRelative(body, (ex, ey))
    dir_offset = {'top': (0, -1), 'bottom': (0, 1), 'right': (1, 0), 'left': (-1, 0)}
    rotate_right_dir = ROTATE_RIGHT_DIR[pdir]
    rotate_left_dir = ROTATE_LEFT_DIR[pdir]
    right_offset = dir_offset[rotate_right_dir]
    left_offset = dir_offset[rotate_left_dir]
    if edir == pdir or epos == pdir:
        wall_right = doesCellContainWall(body['walls'], px + right_offset[0], py + right_offset[1])
        wall_left = doesCellContainWall(body['walls'], px + left_offset[0], py + left_offset[1])
        if wall_left and wall_right:
            if edir == pdir:
                return ADVANCE
            else:
                return RETREAT
        elif wall_left and not wall_right:
            return ROTATE_RIGHT
        elif not wall_left and wall_right:
            return ROTATE_LEFT
        else:
            return ROTATE_LEFT
    else:
        pass

def enemyPosition(body):
    """Returnerer tuppel med x,y-koordinater hvis de eksisterer"""
    try:
        return body["enemies"][0]["x"], body["enemies"][0]["y"]
    except:
        return False

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
    else:
        return enemyPos[0] > position[0]

def ableToWin(body):
    """Returnerer true om du har mulighet for aa vinne en skyteduell"""
    enemyHealth = body["enemies"][0]["strength"]
    enemyDamage = body["enemies"][0]["weaponDamage"]
    health = body["you"]["strength"]
    weaponDamage = body["you"]["weaponDamage"]

    return enemyHealth // weaponDamage <= health // enemyDamage

def powerMove(body):
    if powerups.canSeeHearts(body):
        move = powerups.moveTowardHeart(body)
    else:
        move = powerups.moveTowardPowerup(body)
    return moveTowardsPoint(move[0],move[1],move[2])




def chooseAction(body):
    action = moveTowardsCenterOfMap(body)
    px, py = body['you']['x'], body['you']['y']
    if body['bonusTiles']:
        save_bonuses(body['bonusTiles'])
    bonuses = get_bonuses_from_memory()
    if bonuses:
        closest = powerups.findNearestHeart(px, py, bonuses)
        if closest is None:
            closest = get_closest(px, py, bonuses)
        action = moveTowardsPoint(body, closest['x'], closest['y'])
        if bonusInFrontOfPenguin(body):
            delete_bonus_from_memory(closest)

    if body["suddenDeath"] < 1:
        action = suddenDeath.suddenDeathMove(body)
    elif body["status"] == "hit":
        escape()
    elif enemyStraightAhead(body) and ableToWin(body):
        action = SHOOT

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
        setup_data()
        setup_bonuses()
    elif req_params_query == "command":
        body = json.loads(open(env["req"], "r").read())
        returnObject["command"] = chooseAction(body)

    response["body"] = returnObject
    responseBody.write(json.dumps(response))
    responseBody.close()
