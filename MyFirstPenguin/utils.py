def count():
    c = 0
    try:
        with open('count.txt', 'r') as f:
            c = int(f.readline().strip())
    except:
        pass

    with open('count.txt', 'w') as f:
        f.write(str(c + 1))
    return c + 1


ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

def chooseAction(body):
    action = RETREAT
    c = count()
    if c == ROTATE_LEFT:
        return count
    if c % 2 == 1:
        action = ADVANCE
    else:
        action = RETREAT

    # action = moveTowardsCenterOfMap(body)
    return action

chooseAction(4)
