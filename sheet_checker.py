import math
import cv2

def checkPerpendicular(p1, p2, p3):
    if p2[0] - p1[0] == 0 and p3[0] - p2[0] == 0:
        return False
    elif p2[0] - p1[0] == 0:
        m2 = (p3[1] - p2[1]) / (p3[0] - p2[0])
        degrees = abs(math.degrees(math.atan(m2)) - 90)
    elif p3[0] - p2[0] == 0:
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        degrees = abs(math.degrees(math.atan(m1)) - 90)
    else:
        m1 = (p1[1] - p2[1]) / (p1[0] - p2[0])
        m2 = (p3[1] - p2[1]) / (p3[0] - p2[0])
        degrees = math.degrees(abs(math.atan(m1) - math.atan(m2)))
    perpendicular = degrees > 85 and degrees < 95
    # if perpendicular:
    #     print("Product", degrees)
    return perpendicular


def checkOrthogonal(p1, p2, p3):
    # print("Checking...", p1, p2, p3)
    if checkPerpendicular(p1, p2, p3):
        return (p2, p1, p3)
    elif checkPerpendicular(p1, p3, p2):
        return (p3, p1, p2)
    elif checkPerpendicular(p2, p1, p3):
        return (p1, p2, p3)
    return None


def checkRatio(corner, a, b):
    l1 = int(math.dist(corner, a))
    l2 = int(math.dist(corner, b))
    if l1 < 200 or l2 < 200:
        return False
    r1 = l1 / l2
    r2 = l2 / l1
    ratio = max(r1, r2)
    targetRatio = 297 / 210
    offset = 0.02 #0.05
    print("current ratio", ratio, "target ratio", targetRatio)
    return ratio >= (1 - offset) * targetRatio and ratio <= (1 + offset) * targetRatio


def checkIfIsA4(contour):
    length = len(contour)
    if length < 3:
        return None

    for i in range(length):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                points = checkOrthogonal(contour[i][0], contour[j][0], contour[k][0])
                if points is not None:
                    if checkRatio(*points):
                        print("A4!!!")
                        return points
    return None


def drawA4FromThreeCorners(corners, image):
    if corners is not None and len(corners) == 3:
        cv2.line(image, corners[0], corners[1], (0, 255, 0), 10)
        cv2.line(image, corners[0], corners[2], (0, 255, 0), 10)


def calculateRatio(corners):
    if corners is not None and len(corners) == 3:
        longer_edge = max(
            math.dist(corners[0], corners[1]), math.dist(corners[0], corners[2])
        )  # 297mm



# p1 = (1, 1)
# p2 = (1, 2)
# p3 = (2, 1)
p1 = (1, 1)
# p2 = (595, 1)
# p3 = (1, 421)
# p4 = (44, 44)
# checkIfIsA4([p1, p2, p3, p4])
