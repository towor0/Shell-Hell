import math
import pygame
import random


# some of those functions are not working properly
# changed the code itself instead of the function
def getAngle(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    angle = math.degrees(math.radians(270) - math.atan2(y, x))
    return angle


def directionSpeed(angle, speed):
    vel = pygame.math.Vector2()
    vel.from_polar((speed, angle + 90))
    return vel


def onScreen(rect, sw, sh, bx=0, by=0):
    if rect.left < bx or rect.right > sw - bx:
        return False
    if rect.top < by or rect.bottom > sh - by:
        return False
    return True


def enemySpawn(prect):
    x = random.randint(16, 752)
    y = random.randint(12, 572)
    while prect.centerx - 75 < x < prect.centerx + 75 and prect.centery - 75 < y < prect.centery + 75:
        x = random.randint(16, 752)
        y = random.randint(12, 588)
    return x, y


def getDistance(p1, p2):
    x = pow((p1[0] - p2[0]), 2)
    y = pow((p1[1] - p2[1]), 2)
    return math.sqrt(x + y)
