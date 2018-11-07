from math import *

def count():
    c = 0
    with open('count.txt', 'r') as f:
        c = int(f.readline().strip())
    with open('count.txt', 'w') as f:
        f.write(str(c + 1))
    return c + 1

def euc_dist(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_closest(px, py, points):
    d = [(euc_dist(px, py, points[i]['x'], points[i]['y']), i) for i in range(len(points))]
    return points[min(d)[1]]

def setup_data():
    with open('count.txt', 'w') as f:
        f.write(str(0))

def setup_bonuses():
    with open('bonuses.txt', 'w') as f:
        f.write(str([]))

def save_bonuses(bonuses):
    bonuses = [(bonus['x'], bonus['y'], bonus['type'], bonus['value']) for bonus in bonuses]
    old_bonuses = []
    with open('bonuses.txt', 'r') as f:
        old_bonuses = eval(f.readline().strip())
    for bonus in bonuses:
        if bonus not in old_bonuses:
            old_bonuses.append(bonus)
    with open('bonuses.txt', 'w') as f:
        f.write(str(old_bonuses))

def delete_bonus_from_memory(bonus):
    bonus = (bonus['x'], bonus['y'], bonus['type'], bonus['value'])
    old_bonuses = []
    with open('bonuses.txt', 'r') as f:
        old_bonuses = eval(f.readline().strip())
    new_bonuses = [b for b in old_bonuses if b != bonus]
    with open('bonuses.txt', 'w') as f:
        f.write(str(new_bonuses))

def get_bonuses_from_memory():
    with open('bonuses.txt', 'r') as f:
        bonuses = eval(f.readline().strip())
    return [{'x': b[0], 'y': b[1], 'type': b[2], 'value': b[3]} for b in bonuses]

# def enemy_in_aim(you, enemy):
#     if 'x' not in enemy:
#         return False
#     dir = you['direction']

# def retreat_from_enemy(body):
#     enemy = body['enemies'][0]
#     you = body['you']
#     ex, ey, edir = enemy['x'], enemy['y'], enemy['direction']
#     px, py, pdir = you['x'], you['y'], you['direction']

#%%
# setup_bonuses()
#
# save_bonuses([{'x' : 1, 'y' : 2, 'type' : 'weapon-range', 'value' : 1}, {'x' : 3, 'y' : 4, 'type' : 'strength', 'value' : 1}])
#
# save_bonuses([{'x' : 3, 'y' : 4, 'type' : 'strength', 'value' : 1}, {'x' : 5, 'y' : 6, 'type' : 'weapon-damage', 'value' : 1}])
#
# delete_bonus_from_memory({'x' : 3, 'y' : 4, 'type' : 'strength', 'value' : 1})
#
# get_closest(1, 1, get_bonuses_from_memory())
