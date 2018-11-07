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
    i = -1
    shortestDist = body["bonusTiles"][0]
    for x in body["bonusTiles"]:
        i+=1
        distToPow = eucDist.eucDistance(body, x["x"], x["y"])
        if distToPow < distance:
            distance = distToPow
            shortestDist = body["bonusTiles"][i]
    return shortestDist


def moveTowardPowerup(body):
    closest = findClosestPowerup(body)
    print(closest)
    return (body, closest["x"], closest["y"])

def findNearestHeart(body):
    hearts = [x for x in body["bonusTiles"] if x["type"] == "strength"]
    distance = 99
    i = -1
    closestHeart = hearts[0]
    for x in hearts:
        i += 1
        distToHeart = eucDist.eucDistance(body, x["x"], x["y"])
        if distToHeart < distance:
            distance = distToHeart
            closestHeart = hearts[i]
    return closestHeart

def moveTowardHeart(body):
    closest = findNearestHeart(body)
    return (body, closest["x"], closest["y"])