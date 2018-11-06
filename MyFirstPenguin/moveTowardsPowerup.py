import MyFirstPenguin.eucDist

def canSeePowerup(body):
    if  body["bonusTiles"]:
        return True
    return False





def findClosestPowerup(body):
    distance = 999
    shortestDist = body["bonusTiles"][0]
    for x in body["bonusTiles"]:
        distToPow = MyFirstPenguin.eucDist.eucDistance(body, x["x"], x["y"])
        if distToPow < distance:
            distance = distToPow
            shortestDist = body["bonusTiles"][x]
    return shortestDist


def moveTowardPowerup(body):
    if canSeePowerup(body):
        closest = findClosestPowerup(body)
        return (body, closest["x"], closest["y"])