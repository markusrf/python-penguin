import eucDist

def canSeePowerup(body):
    if  body["bonusTiles"]:
        return True
    return False

def canSeeHearts(body):
    hearts = [x for x in body["bonusTiles"] if x["type"] == "strength"]
    if hearts:
        return True
    return False

def findClosestPowerup(body):
    distance = 999
    shortestDist = body["bonusTiles"][0]
    for x in body["bonusTiles"]:
        distToPow = eucDist.eucDistance(body, x["x"], x["y"])
        if distToPow < distance:
            distance = distToPow
            shortestDist = body["bonusTiles"][x]
    return shortestDist


def moveTowardPowerup(body):
    closest = findClosestPowerup(body)
    return (body, closest["x"], closest["y"])

def findNearestHeart(body):
    hearts = [x for x in body["bonusTiles"] if x["type"] == "strength"]
    distance = 99
    closestHeart = hearts[0]
    for x in hearts:
        distToHeart = eucDist.eucDistance(body, x["x"], x["y"])
        if distToHeart < distance:
            distance = distToHeart
            closestHeart = hearts[x]
    return closestHeart

def moveTowardHeart(body):
    closest = findNearestHeart(body)
    return (body, closest["x"], closest["y"])