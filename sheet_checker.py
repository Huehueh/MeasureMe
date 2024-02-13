import math
import cv2
import numpy as np
from utils import rescaleImage
from drawing import drawPoints

# p2 as a corner
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
    perpendicular = degrees > 80 and degrees < 100
    return perpendicular


def checkOrthogonal(p1, p2, p3):
    result = None
    if checkPerpendicular(p1, p2, p3):
        result = [p2, p1, p3]
    elif checkPerpendicular(p1, p3, p2):
        result = [p3, p1, p2]
    elif checkPerpendicular(p2, p1, p3):
        result = [p1, p2, p3]
    # if result is not None:
    #     print("checkOrthogonal", result)
    return result


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

    result = ratio >= (1 - offset) * targetRatio and ratio <= (1 + offset) * targetRatio
    # print("checkRatio", result, "current ratio", ratio, "target ratio", targetRatio)
    return result

def checkWhiteSpace(grayImage, corner, a, b) -> bool:
    # draw space that we want to check
    contour = np.array([corner, a, b])
    cimg = np.zeros_like(grayImage)
    cv2.drawContours(cimg, [contour], -1, color=255, thickness=-1)
    # cv2.imshow("kontury do sprawdzenia bialosci", rescaleImage(25, cimg))
    # cv2.waitKey()
    points = np.where(cimg==255)

    white = 0
    black = 0
    for point in zip(points[0], points[1]):
        # print(point)
        pixel = grayImage[point[0], point[1]]
        if pixel == 255:
            white += 1
        else:
            black += 1
    whitness = white/(white+black)
    print("checkWhiteSpace", whitness)
    return whitness

def isCorner(contour, index):
    first = len(contour) - 1 if index == 0 else index - 1
    last = 0 if index == len(contour) - 1 else index + 1
    return checkPerpendicular(contour[first][0], contour[index][0], contour[last][0])

def getAllCorners(contour):
    corners = []
    for i in range(len(contour)):
        if isCorner(contour, i):
            corners.append(contour[i][0])
    return corners

def getA4Candidates(corners):
    cornersCandidates = []
    cornersNum = len(corners)
    for i in range(cornersNum):
        for j in range(i + 1, cornersNum):
            for k in range(j + 1, cornersNum):
                orthogonalPoints = checkOrthogonal(corners[i], corners[j], corners[k])
                if orthogonalPoints is not None and checkRatio(*orthogonalPoints):
                    cornersCandidates.append(orthogonalPoints)
    return cornersCandidates


def checkSize(p1, p2, p3):
    return math.dist(p1, p2) * math.dist(p2, p3)

def checkIfIsA4(contour, originalImage):
    # print("checkIfIsA4")
    if len(contour) < 3:
        return None

    corners = getAllCorners(contour)
    candidates = getA4Candidates(corners)
    if len(candidates) > 1:
        candidates = sorted(candidates, key=lambda x: checkWhiteSpace(originalImage, x[0], x[1], x[2]), reverse=True)
    
    # if len(candidates) > 0:        
    #     for points in candidates:
    #         coloredImage = cv2.cvtColor(originalImage, cv2.COLOR_GRAY2BGR)
    #         drawPoints(points, coloredImage, (255, 200, 100))
    #         cv2.imshow("candidates", rescaleImage(25, coloredImage))
    #         cv2.waitKey()
    if len(candidates) > 0:
        return candidates[0]
    return None




# used?
def calculateRatio(corners):
    if corners is None or len(corners) != 3:
        return
    longer_edge = max(
        math.dist(corners[0], corners[1]), math.dist(corners[0], corners[2])
    )  # 297mm

# def getLastCorner(A, B, C):
#     a = A - B
#     b =

# p1 = (1, 1)
# p2 = (1, 2)
# p3 = (2, 1)
p1 = (1, 1)
# p2 = (595, 1)
# p3 = (1, 421)
# p4 = (44, 44)
# checkIfIsA4([p1, p2, p3, p4])
