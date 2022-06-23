from math import sin, cos, sqrt, atan2, radians


def calcDistance(p1, p2):
    return (6371 * 2 * atan2(sqrt((sin(abs(radians(p2[0]) - radians(p1[0])) / 2)**2 + cos(p1[0]) * cos(p2[0]) * sin(abs(radians(p2[1]) - radians(p1[1])) / 2)**2)), sqrt(
        1 - (sin(abs(radians(p2[0]) - radians(p1[0])) / 2)**2 + cos(p1[0]) * cos(p2[0]) * sin(abs(radians(p2[1]) - radians(p1[1])) / 2)**2))))
